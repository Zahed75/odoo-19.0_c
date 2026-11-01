from datetime import timedelta

from odoo import fields, models
from odoo.exceptions import UserError


class LibraryLoanExtendWizard(models.TransientModel):
    _name = "library.loan.extend.wizard"
    _description = "Extend a Loan"

    loan_id = fields.Many2one("library.loan", string="Loan", required=True)
    extra_days = fields.Integer(default=7, required=True)
    reason = fields.Char()

    def action_extend(self):
        self.ensure_one()
        if self.extra_days <= 0:
            raise UserError("Extra days must be greater than zero.")
        self.loan_id.due_date += timedelta(days=self.extra_days)
        return {"type": "ir.actions.act_window_close"}

