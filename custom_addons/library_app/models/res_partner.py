from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"          # extend an EXISTING model (no _name)

    is_library_member = fields.Boolean(string="Library Member")
    loan_ids = fields.One2many("library.loan", "member_id", string="Book Loans")

