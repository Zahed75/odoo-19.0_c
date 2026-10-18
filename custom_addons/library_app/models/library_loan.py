from datetime import datetime, timedelta
from email.policy import default

from iot_drivers.tools.helpers import require_db
from odoo import models, fields, api

FINES_PER_DAY = 20


class LibraryLoan(models.Model):
    _name = "library.loan"
    _description = "Book Loan"
    _inherit = ["mail.thread"]

    _order = "name"

    name = fields.Char(
        string="Reference",
        default="New",
        readonly=True,
        copy=False
    )
    book_id = fields.Many2one("library.book", string="Book", required=True, copy=False)
    member_id = fields.Many2one("res.partner", string="Member", required=True)
    loan_date = fields.Date(default=fields.Date.context_today, required=True)
    due_date = fields.Date(compute="_compute_due_date", store=True, readonly=True)
    returned_date = fields.Date(readonly=True, copy=False)
    state = fields.Selection(
        [
            ("draft", "Draft"), ("borrowed", "Borrowed"),
            ("late", "Late"), ("returned", "Returned"),
        ],
        default="draft", tracking=True, copy=False

    )
    currency_id = fields.Many2one(related="book_id.currency_id")
    fine_amount = fields.Monetary(compute="_compute_fine_amount", store=True)
    notes = fields.Text()

    @api.depends("loan_date")
    def _compute_due_date(self):
        for loan in self:
            loan.due_date = loan.loan_date and loan.loan_date + timedelta(days=14)

    @api.depends("due_date", "returned_date")
    def _compute_fine_amount(self):
        for loan in self:
            fine = 0.0
            if loan.returned_date and loan.due_date:
                days_late = (loan.returned_date - loan.due_date).days
                fine = max(days_late, 0) * FINES_PER_DAY
                loan.fine_amount = fine
