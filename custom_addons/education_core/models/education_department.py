"""
education.department - Academic Department Model
"""

from odoo import api,fields,models

class EducationDepartment(models.Model):
    """ Academic Department (e.g Computer Science,Business Administration) """

    _name="education.department"
    _description="Academic Department"
    _inherit=["mail.thread"]
    _order = "sequence,name"

    # ---- Standard Fields

    name = fields.Char(
        string = "Department Name",
        required=True,
        tracking=True,
        translate=True,
        copy=False,
        help= "Full Name of the acadmic Department(eg. Computer Science, Business Administration)",

    ),
    code = fields.Char(
        string="Department Code/Name",
        required=True,
        size=10,
        tracking=True,
        help="Short Code used in Reports (e.g CSE,MBA,MED)",
        copy=False,
    ),

    sequence=fields.Integer(
        default=10,
        help="Determines the display order of the departments in list and menus Lower numbers appear first",

    ),
    description = fields.Text(
        string="Department Description",
        help="Additional information about the department",
    ),

    active=fields.Boolean(
        string="Active",
        default=True,
        help="Indicates whether the department is currently active or not",
    ),

#   -----------Relations Fields-----------------


head_id =fields.Many2one(
    comodel_name="hr.employee",
    string="Department Head",
    domain= "[('is_faculty', '=', True)]",
    tracking=True,
    copy=False,
    help="Faculty Members responsible for the heading and managing this department",
),

company_id=fields.Many2one(
    comodel_name="res.company",
    string = "Institution",
    default= lambda self :self.env.company,

),

program_ids= fields.One2many(
    comodel_name="education.program",
    inverse_name ="department_id",
    string="Programs",
    help="Programs offered by this department",
)

# ----------SQL Constraints


_code_company=models.Constraint(
    "UNIQUE(code,company_id)",
    "Department Code must be unique within the institution",
)




@api.depends('program_ids')
def _compute_program_count(self):
    """
       Count academic Programs offered by this department
       """
    for rec in self:
        rec.program_count = len(rec.program_ids)










