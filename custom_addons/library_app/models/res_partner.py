from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"   #Extend The model
    is_library_member= fields.Boolean(string="Library Member")
    loan_ids = fields.One2many('library.loan', "member_id",string="Book Loans")

