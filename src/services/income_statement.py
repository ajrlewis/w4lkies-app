"""
select sum(i.total_price)
from invoice as i
where i.date_issued >= "2024-04-01" and i.date_issued <= "2025-04-01";

select sum(e.price)
from expense as e
where e.date >= "2024-04-01" and e.date <= "2025-04-01";

Period: 2024-04-01 - 2025-03-01
Total Invoice: 27,577.00
Total Expense: 6,231.12
Net: 21,345.88 (+2,500 projected to 2025-04-01, 23,845.88)
"""

"""
On the "Income Statement" tab, you could display a summary of the key financial metrics, including:

    Total Invoices: sum of all invoices over the selected period
    Total Expenses: sum of all expenses over the selected period
    Gross Profit: Total Invoices - Total Expenses (the calculation you mentioned earlier)
    Profit Margin: (Gross Profit / Total Invoices) * 100, to show the percentage of profit

You could also consider adding other relevant metrics, such as:

    Average Invoice Value
    Average Expense Value
    Total Number of Invoices
    Total Number of Expenses
"""

import datetime

from services import expense_service, invoice_service


def get_summary(from_date: datetime.date, to_date: datetime.date):
    expenses = expense_service.get_expenses(from_date=from_date, to_date=to_date)
    expense_total = [expense.price for expense in expenses]
    return {
        "from_date": from_date,
        "to_date": to_date,
        "invoice_total": 0,
        "expense_total": 0,
        "gross_profit": 0,
        "profit_margin": 0,
        "total_number_of_invoices": 0,
        "total_number_of_expenses": 0,
    }
