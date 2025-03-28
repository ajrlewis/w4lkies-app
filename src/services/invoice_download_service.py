from datetime import datetime
from io import BytesIO
import sys
import tempfile
from typing import Dict

from loguru import logger
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

x_0 = 0.5 * inch
y_0 = 8.25 * inch

font_skip = 0.12 * inch
small_skip = 0.25 * inch
medium_skip = 0.5 * inch
big_skip = 1.0 * inch

currency = "£"
server_name = "w4lkies"
server_url = "https://w4lkies.com"
server_logo = "src/static/img/logo-white-background.png"
server_email = "hello@w4lkies.com"
server_bank_name = "Sophia Lewis"
server_bank_sort_code = "04-29-09"
server_bank_account_number = "65204158"
invoice_due_days = 7
invoice_currency = "£"
invoice_payment_request = ""
theme_color_1 = "#fd8927"
theme_color_2 = "#f4e2cc"
theme_color_3 = "#8bb4a6"
theme_font_1 = ""


def _add_header(pdf, invoice, width, height):
    # Invoice logo
    logo_width = 150
    logo_aspect_ratio = 1.1
    logo_height = logo_aspect_ratio * logo_width
    w, h = pdf.drawInlineImage(
        server_logo,
        x_0,
        y_0,
        width=logo_width,
        height=logo_height,
    )
    pdf.linkURL(
        server_url,
        (x_0, y_0, x_0 + w, y_0 + h),
        thickness=0,
        relative=1,
    )

    # Invoice title
    pdf.setFont("Helvetica-Bold", 20)
    pdf.setFillColor(colors.black)
    x = width / 2
    y = 0.9 * height
    text = "Invoice"
    pdf.drawCentredString(x, y, text.upper())

    # Invoice IDs
    pdf.setFont("Helvetica", 12)
    pdf.setFillColor(colors.black)
    x = x_0 + 4.25 * inch
    y -= medium_skip
    pdf.drawString(x, y, f"Reference: #{invoice.reference}")
    y -= small_skip
    pdf.drawString(x, y, f"Issued Date: {invoice.date_issued}")
    y -= small_skip
    text = f"Due Date: {invoice.date_due}"
    pdf.drawString(x, y, text)

    # Email contact for invoice help
    y -= medium_skip
    text = "Need help? "
    pdf.drawString(x, y, text)
    w = pdf.stringWidth(text)
    x += w
    text = server_email
    pdf.drawString(x, y, text)
    w = pdf.stringWidth(text)
    h = pdf._leading
    text = f"mailto:{server_email}?subject=Invoice #{invoice.reference}"
    pdf.linkURL(
        text,
        (x, y, x + w, y + h),
        thickness=0,
        relative=1,
    )
    x = x_0 + medium_skip
    y -= big_skip
    return x, y


def _add_page_break(pdf, invoice, width, height):
    pdf.showPage()
    x, y = _add_header(pdf, invoice, width, height)
    return x, y


def _create(invoice):
    # Create document
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Invoice header
    x, y = _add_header(pdf, invoice, width, height)

    # Invoice to
    pdf.setFont("Helvetica-Bold", 12)
    text = f"Bill To: {invoice.customer.name}"
    pdf.drawString(x, y, text)

    # Table of booking
    booking_chunks = chunk_bookings(invoice.bookings)
    logger.debug(f"{booking_chunks = }")
    number_of_chunks = len(booking_chunks)
    for i, bookings in enumerate(booking_chunks):
        table_header = ["Date", "Service", f"Price / {currency}"]
        table_style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), theme_color_1),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), theme_color_2),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                ("ALIGN", (0, 1), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 11),
                ("RIGHTPADDING", (2, 1), (2, -1), 5),
                ("RIGHTPADDING", (3, 1), (3, -1), 5),
                ("RIGHTPADDING", (4, 1), (4, -1), 5),
            ]
        )
        table_data = [table_header]
        for booking in bookings:
            table_data.append(
                [
                    f"{booking.date} {booking.time}",
                    booking.service.name,
                    f"{booking.service.price:.2f}",
                ]
            )
        table = Table(table_data, colWidths=[2.16 * inch, 2.16 * inch, 2.16 * inch])
        table.setStyle(table_style)
        w, h = table.wrapOn(pdf, 400, 400)
        x = (width - w) / 2
        if i == 0:
            y -= medium_skip
        else:
            y += font_skip
        y -= h
        table.drawOn(pdf, x, y)
        # Add the subtotal and total on the last chunk of services.
        if i == number_of_chunks - 1:
            pdf.setFillColor(colors.black)
            x -= 0.75 * inch
            x += 4.8 * inch
            dx = 1.5 * inch
            y -= small_skip
            y -= 0.175 * inch
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.setLineWidth(7)
            pdf.line(x, y, x + dx, y)
            pdf.setStrokeColor(theme_color_3)
            pdf.setLineWidth(6)
            pdf.line(x, y, x + dx, y)
            y -= small_skip
            y -= 0.175 * inch
            text = f"Subtotal: {currency}{invoice.price_subtotal:.2f}"
            pdf.drawString(x, y, text)

            if invoice.price_discount > 0.0:
                y -= small_skip
                text = f"Discount: {currency}{invoice.price_discount:.2f}"
                pdf.drawString(x, y, text)
            y -= 0.175 * inch
            y -= small_skip
            text = f"Total: {currency}{invoice.price_total:.2f}"
            pdf.drawString(x, y, text)
        # Page break
        x, y = _add_page_break(pdf, invoice, width, height)

    # Payment Details
    x_payment = x
    y_payment = y
    # Bank payment details
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "Bank Details:")
    pdf.setFont("Helvetica", 12)
    y -= small_skip
    y -= 0.125 * inch
    pdf.drawString(x, y, server_bank_name)
    y -= small_skip
    pdf.drawString(x, y, "Sort Code: " + server_bank_sort_code)
    y -= small_skip
    text = "Account Number: " + str(server_bank_account_number)
    pdf.drawString(x, y, text)

    x = x_payment + 3 * inch
    y = y_payment
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "Other Payment Methods:")

    y -= small_skip
    y -= 0.125 * inch
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "Want to pay by PayPal? (debit/credit)")
    pdf.setFont("Helvetica", 12)
    y -= small_skip
    pdf.drawString(x, y, "Request a PayPal invoice.")
    y -= small_skip
    pdf.drawString(x, y, "Note a 7% fee will be added to the total.")

    y -= medium_skip
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "Want to pay by Bitcoin?")
    pdf.setFont("Helvetica", 12)
    y -= small_skip
    pdf.drawString(x, y, "Request a Bitcoin Lightning invoice.")
    y -= small_skip
    pdf.drawString(x, y, "Or send Bitcoin to pay@w4lkies.com")

    y -= medium_skip
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "Want to pay by Cash?")
    pdf.setFont("Helvetica", 12)
    pdf.setFont("Helvetica", 12)
    y -= small_skip
    pdf.drawString(x, y, "Pay in Person")

    #  Footer
    x = width / 2.0

    # TODO (ajrl) small_skip and big_skip, y += small_skip
    y -= big_skip
    y -= big_skip

    text = "Thank you for your business!".upper()
    pdf.setFillColor(colors.black)
    # pdf.setFont("theme_font_1", 12)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(x, y, text)

    # Save and create PDF file and filename
    pdf.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    pdf_file = BytesIO()
    pdf_file.write(pdf_bytes)
    pdf_file.seek(0)
    customer_name = invoice.customer.name
    year_issued = invoice.date_issued.strftime("%Y")
    month_issued = invoice.date_issued.strftime("%B")
    pdf_filepath = f"{customer_name} {year_issued} {month_issued}.pdf"

    return pdf_file, pdf_filepath


def chunk_bookings(bookings: list) -> list:
    maximum_number_of_services_on_first_page = 21
    maximum_number_of_services_for_aggregate = 0
    maximum_number_of_services_on_page = (
        maximum_number_of_services_on_first_page
        + maximum_number_of_services_for_aggregate
    )
    service_chunks = []
    page_number = 0
    while len(bookings) > 0:
        page_number += 1
        number_of_services_remaining = len(bookings)
        if page_number == 1:
            number_of_services_on_page = maximum_number_of_services_on_first_page
        else:
            if number_of_services_remaining > maximum_number_of_services_on_page:
                number_of_services_on_page = maximum_number_of_services_on_page
            else:
                number_of_services_on_page = number_of_services_remaining
        service_chunks.append(bookings[:number_of_services_on_page])
        bookings = bookings[number_of_services_on_page:]
    return service_chunks


def create(invoice):
    pdf_file, pdf_filepath = _create(invoice)
    return pdf_file, pdf_filepath
