# """
# education.department - academic Department Model
# """
from odoo import models, fields, api

class EducationDepartment(models.Model):
    # Academic Department ( e.g. Computer Science, Physics, etc.)
    _name = "education.department"
    _description = "Academic Department"
    _inherit = ['mail.thread']
    _order = "sequence, name"

    # ---Standard Fields---
    name = fields.Char(
        string="Department Name",
        required=True,
        tracking=True,
        translate=True,
        copy=False,
        help="Full Name of the academic department (e.g. Computer Science, Physics, etc.)"
    )

    code = fields.Char(
        string="Department Code",
        required=True,
        tracking=True,
        size=12,
        copy=False,
        help="Short Code for the academic department (e.g. CS, PHY, etc.)"
    )

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Determine the display order of the department in the list view"
    )

    description = fields.Text(
        string="Description of Department",
        translate=True,
        help="Description of the academic department"
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, the department will be hidden from the list view"
    )


    # -------Relational Fields-----
    head_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Department Head",
        domain="[('is_faculty', '=', True)]",
        tracking=True,
        copy=False,
        help="Faculty member who is the head of the department"
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
        # required=True,
        # tracking=True,
        # help="Company to which the department belongs"
    )

    program_ids = fields.One2many(
        comodel_name="education.program",
        inverse_name="department_id",
        string="Programs",
        help="List of academic programs offered by the department"
    )

    # ------SQL Constraints------
    _core_company = models.Constraint(
        "Unique"
    )