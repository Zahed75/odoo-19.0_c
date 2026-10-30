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

    #compute loan
    @api.depends("loan_date")
    def _compute_due_date(self):
        for loan in self:
            loan.due_date=loan.loan_date and loan.loan_date + timedelta(days=14)

    @api.depends("due_date","return_date")
    def _compute_fine_amount(self):
        for loan in self:
            fine=0.0
            if loan.return_date and loan.due_date:
                days_late=(loan.return_date - loan.due_date).days
                fine=max(days_late,0)*FINE_PER_DAY
                loan.fine_amount=fine
    #Button
    def action_borrow(self):
        for loan in self:
            if loan.book_id.copies_available <=0:
                raise UserError(f"No Copy of '{loan.book_id.name}' is available ")
            self.write({"sate": "borrowed"})

    def action_return(self):
        self.write({
            "state": "returned",
            "return_date": fields.Date.context_today(self)
        })
     #-- called every day schedule action corn job
    @api.model
    def _corn_make_late(self):
        overdue=self.search(
            [
                ("state", "=", "borrowed"),
                ("due_date", "<=", fields.Date.context_today(self)),
            ]
        )
        overdue.write({"state": "late"})
