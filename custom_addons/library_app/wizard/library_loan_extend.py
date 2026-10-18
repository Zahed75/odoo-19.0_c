from datetime import timedelta
from odoo import models, fields, api

class LibraryLoanExtendWizard(models.TransientModel):
    _name = "library.loan.extend.wizard"
    _description = "Extend a Loan"

    loan_id = fields.Many2one("library.loan", string="Loan")
    extra_days = fields.Integer(default=7,required=True)
    reason=fields.Char()

