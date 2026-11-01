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
    loan_date = fields.Datetime(default=fields.Datetime.now, required=True)
    due_date = fields.Datetime(compute="_compute_due_date", store=True, readonly=False)
    return_date = fields.Date(readonly=True, copy=False)
    state = fields.Selection(
        [("draft", "Draft"), ("borrowed", "Borrowed"),
         ("late", "Late"), ("returned", "Returned")],
        default="draft", tracking=True, copy=False,
    )
    currency_id = fields.Many2one(related="book_id.currency_id")
    fine_amount = fields.Monetary(compute="_compute_fine_amount", store=True)
    notes = fields.Text()

    # --- override create to assign a sequence number --------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                seq = self.env["ir.sequence"].next_by_code("library.loan")
                vals["name"] = seq or "New"
        return super().create(vals_list)

    # --- an extended loan that is no longer overdue goes back to borrowed ---
    def write(self, vals):
        res = super().write(vals)
        if "due_date" in vals:
            now = fields.Datetime.now()
            self.filtered(
                lambda l: l.state == "late" and l.due_date and l.due_date >= now
            ).write({"state": "borrowed"})
        return res

    # --- one timezone per loan: the fine must not change with who computes it ---
    def _library_date(self, timestamp=None):
        self.ensure_one()
        tz = self.env.company.partner_id.tz or self.create_uid.tz or "UTC"
        return fields.Date.context_today(self.with_context(tz=tz), timestamp=timestamp)

    # --- computes --------------------------------------------------------
    @api.depends("loan_date")
    def _compute_due_date(self):
        for loan in self:
            loan.due_date = loan.loan_date and loan.loan_date + timedelta(days=14)

    @api.depends("due_date", "return_date", "state")
    def _compute_fine_amount(self):
        for loan in self:
            fine = 0.0
            # a book still out keeps accruing until today; the cron keeps this current
            end_date = loan.return_date or (
                loan.state in ("borrowed", "late") and loan._library_date()
            )
            if end_date and loan.due_date:
                days_late = (end_date - loan._library_date(loan.due_date)).days
                fine = max(days_late, 0) * FINE_PER_DAY
            loan.fine_amount = fine

    # --- onchange: UI-only helper, runs while the user edits the form --------
    @api.onchange("book_id")
    def _onchange_book_id(self):
        if self.book_id and self.book_id.copies_available <= 0:
            return {"warning": {
                "title": "Not available",
                "message": "All copies of this book are currently borrowed.",
            }}

    # --- buttons -----------------------------------------------------------
    def action_borrow(self):
        for loan in self:
            if loan.book_id.copies_available <= 0:
                raise UserError(f"No copy of '{loan.book_id.name}' is available.")
        self.write({"state": "borrowed"})

    def action_return(self):
        for loan in self:
            loan.write({
                "state": "returned",
                "return_date": loan._library_date(),
            })

    # --- called every day by the scheduled action (cron) ---------------------
    @api.model
    def _cron_mark_late(self):
        overdue = self.search([
            ("state", "=", "borrowed"),
            ("due_date", "<", fields.Datetime.now()),
        ])
        overdue.write({"state": "late"})
        # the stored fine depends on today's date, which no field change can trigger
        self.search([("state", "=", "late")])._compute_fine_amount()
