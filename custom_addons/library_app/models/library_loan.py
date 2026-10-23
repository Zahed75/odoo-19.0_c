from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

FINE_PER_DAY = 10.0


class LibraryLoan(models.Model):
    _name = "library.loan"
    _description = "Book Loan"
    _inherit = ["mail.thread"]
    _order = "loan_date desc, id desc"

    name = fields.Char(string="Reference", default="New", readonly=True, copy=False)
    book_id = fields.Many2one("library.book", string="Book", required=True, tracking=True)
    member_id = fields.Many2one("res.partner", string="Member", required=True)
    loan_date = fields.Date(default=fields.Date.context_today, required=True)
    due_date = fields.Date(compute="_compute_due_date", store=True, readonly=False)
    return_date = fields.Date(readonly=True, copy=False)
    state = fields.Selection(
        [("draft", "Draft"), ("borrowed", "Borrowed"),
         ("late", "Late"), ("returned", "Returned")],
        default="draft", tracking=True, copy=False,
    )
    currency_id = fields.Many2one(related="book_id.currency_id")
    fine_amount = fields.Monetary(compute="_compute_fine_amount", store=True)
    notes = fields.Text()


