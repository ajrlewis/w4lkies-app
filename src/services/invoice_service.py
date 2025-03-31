import datetime
import hashlib
from typing import Optional

from loguru import logger
from sqlalchemy import asc, desc, func

from app import db
from forms.invoice_form import InvoiceForm
from forms.invoice_generate_form import InvoiceGenerateForm

# from forms.invoice_filter_form import invoiceFilterForm
from models.invoice import Invoice
from services import booking_service, invoice_download_service


def get_invoice_form(
    invoice: Optional[Invoice] = None, ignore_request_data: bool = False
) -> InvoiceForm:
    if ignore_request_data:
        logger.debug(f"{ignore_request_data = }")
        invoice_form = InvoiceForm(formdata=None)
    else:
        invoice_form = InvoiceForm()
    if invoice:
        invoice_form.customer_id.data = invoice.customer_id
        invoice_form.date_start.data = invoice.date_start
        invoice_form.date_end.data = invoice.date_end
    return invoice_form


def get_invoice_generate_form(ignore_request_data: bool = False) -> InvoiceGenerateForm:
    invoice_generate_form = InvoiceGenerateForm()
    return invoice_generate_form


def get_invoices() -> list[Invoice]:
    # Generate query
    query = db.session.query(Invoice)
    query = query.order_by(Invoice.date_issued.desc())
    invoices = query.all()
    logger.debug(f"{invoices = }")
    return invoices


def get_invoice_by_id(invoice_id: int) -> Optional[Invoice]:
    invoice = db.session.get(Invoice, invoice_id)
    logger.debug(f"{invoice = }")
    return invoice


def update_invoice(invoice: Invoice, invoice_data: dict) -> Optional[Invoice]:
    if reference := invoice_data.get("reference"):
        logger.debug(f"{reference = }")
        invoice.reference = reference

    if date_start := invoice_data.get("date_start"):
        logger.debug(f"{date_start = }")
        invoice.date_start = date_start

    if date_end := invoice_data.get("date_end"):
        logger.debug(f"{date_end = }")
        invoice.date_end = date_end

    if date_issued := invoice_data.get("date_issued"):
        logger.debug(f"{date_issued = }")
        invoice.date_issued = date_issued

    if date_due := invoice_data.get("date_due"):
        logger.debug(f"{date_due = }")
        invoice.date_issued = date_due

    if date_paid := invoice_data.get("date_paid"):
        logger.debug(f"{date_paid = }")
        invoice.date_paid = date_paid

    if price_subtotal := invoice_data.get("price_subtotal"):
        logger.debug(f"{price_subtotal = }")
        invoice.price_subtotal = price_subtotal

    if price_discount := invoice_data.get("price_discount"):
        logger.debug(f"{price_discount = }")
        invoice.price_discount = price_discount

    if price_total := invoice_data.get("price_total"):
        logger.debug(f"{price_total = }")
        invoice.price_total = price_total

    if customer_id := invoice_data.get("customer_id"):
        logger.debug(f"{customer_id = }")
        invoice.customer_id = customer_id

    if bookings := invoice_data.get("bookings"):
        logger.debug(f"{bookings = }")
        invoice.bookings = bookings

    if updated_by := invoice_data.get("updated_by"):
        logger.debug(f"{updated_by = }")
        invoice.updated_by = updated_by

    if updated_at := invoice_data.get("updated_at"):
        logger.debug(f"{updated_at = }")
        invoice.updated_at = updated_at

    try:
        db.session.commit()
        return invoice
    except Exception as e:
        logger.error(f"Error updating invoice: {e}")
        db.session.rollback()
        return


def update_invoice_by_id(invoice_id: int, invoice_data: dict) -> Optional[Invoice]:
    logger.debug(f"{invoice_id = } {invoice_data = }")
    invoice = get_invoice_by_id(invoice_id)
    logger.debug(f"{invoice = }")
    if not invoice:
        logger.error(f"Invoice {invoice_id} not found.")
        return
    invoice = update_invoice(invoice, new_invoice_data)
    return invoice


def add_invoice(invoice_data: dict) -> Optional[Invoice]:
    new_invoice = Invoice(
        invoice_id=invoice_data.get("invoice_id"),
        reference=invoice_data.get("reference"),
        date_start=invoice_data.get("date_start"),
        date_end=invoice_data.get("date_end"),
        date_issued=invoice_data.get("date_issued"),
        date_due=invoice_data.get("date_due"),
        date_paid=invoice_data.get("date_paid"),
        price_subtotal=invoice_data.get("price_subtotal"),
        price_discount=invoice_data.get("price_discount"),
        price_total=invoice_data.get("price_total"),
        customer_id=invoice_data.get("customer_id"),
        bookings=invoice_data.get("bookings", []),
        created_at=invoice_data.get("created_at"),
        created_by=invoice_data.get("created_by"),
        updated_at=invoice_data.get("updated_at"),
        updated_by=invoice_data.get("updated_by"),
    )
    try:
        db.session.add(new_invoice)
        db.session.commit()
        logger.debug(f"{new_invoice = }")
        return new_invoice
    except Exception as e:
        logger.error(f"Error adding invoice: {e}")
        db.session.rollback()
        return


def generate_invoice_data(customer_id: int, date_start: str, date_end: str) -> dict:
    reference_start = "W4LKIES"
    days_due = 7

    # Get unique reference for invoice
    reference_hash = (
        hashlib.sha256(f"{customer_id}-{date_start}-{date_end}".encode("UTF-8"))
        .hexdigest()[:8]
        .upper()
    )
    reference = f"{reference_start}-{reference_hash}"
    logger.debug(f"{reference = }")

    # Get the customer bookings.
    bookings = booking_service.get_bookings(
        date_min=date_start, date_max=date_end, customer_id=customer_id
    )
    logger.debug(f"Found {len(bookings)} bookings for invoice")
    logger.debug(f"{bookings = }")

    # Get the total price of the bookings
    price_subtotal = 0.0
    price_discount = 0.0
    for booking in bookings:
        logger.debug(f"{booking.date} {booking.service.name} {booking.service.price}")
        price_subtotal += booking.service.price
    price_total = price_subtotal - price_discount
    logger.debug(f"{price_discount = } {price_total = }")

    invoice_data = {
        "reference": reference,
        "date_start": date_start,
        "date_end": date_end,
        "date_issued": datetime.datetime.now(),
        "date_due": datetime.datetime.now() + datetime.timedelta(days=days_due),
        "price_subtotal": price_subtotal,
        "price_discount": price_discount,
        "price_total": price_total,
        "customer_id": customer_id,
        "bookings": bookings,
    }

    return invoice_data


def generate_invoice(invoice_data: dict) -> Optional[Invoice]:
    customer_id = invoice_data["customer_id"]
    date_start = invoice_data["date_start"]
    date_end = invoice_data["date_end"]

    new_invoice_data = generate_invoice_data(customer_id, date_start, date_end)

    created_by = invoice_data["created_by"]
    new_invoice_data["created_by"] = created_by

    new_invoice = add_invoice(new_invoice_data)
    logger.info(f"{new_invoice = }")
    logger.info(f"{new_invoice.bookings = }")

    return new_invoice


def regenerate_invoice_by_id(invoice_id: int, updated_by: int) -> Optional[Invoice]:
    invoice = get_invoice_by_id(invoice_id)
    if not invoice:
        return

    customer_id = invoice.customer_id
    date_start = invoice.date_start
    date_end = invoice.date_end

    new_invoice_data = generate_invoice_data(customer_id, date_start, date_end)

    new_invoice_data["updated_by"] = updated_by
    new_invoice_data["updated_at"] = datetime.datetime.now()
    # invoice = update_invoice_by_id(invoice_id, new_invoice_data)
    invoice = update_invoice(invoice, new_invoice_data)
    return invoice


def download_invoice_by_id(invoice_id: int) -> Optional[bytes]:
    invoice = get_invoice_by_id(invoice_id)
    logger.debug(f"{invoice = }")
    if invoice is not None:
        try:
            pdf_file, pdf_filepath = invoice_download_service.create(invoice)
            return pdf_file, pdf_filepath
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to download invoice: {e}")
    else:
        logger.error(f"Invoice with ID {invoice_id} does not exist")


def delete_invoice_by_id(invoice_id: int) -> None:
    invoice = get_invoice_by_id(invoice_id)
    logger.debug(f"{invoice = }")
    if invoice is not None:
        try:
            db.session.delete(invoice)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to delete invoice: {e}")
    else:
        logger.error(f"Invoice with ID {invoice_id} does not exist")
