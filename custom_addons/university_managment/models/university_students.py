from odoo import models,fields


class UniversityStudents(models.Model):
    _name ='university.students'
    _description ='University Students'

    name=fields.Char(string='Student Name',required=True)
    student_id=fields.Char(string='Student ID',required=True)
    email=fields.Char(string='Student Email')
    phone=fields.Char(string='Student Phone Number')
    date_of_birth=fields.Date(string='Date of Birth',required=True)
    gender=fields.Selection(
        selection=[('male','Male'),('female','Female'),('other','Other')],
        string='Gender'
    )
    active=fields.Boolean(default=False)