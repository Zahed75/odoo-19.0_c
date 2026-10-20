from odoo import fields, models


class LibraryTag(models.Model):
    _name = "library.tag"
    _description = "Book Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _name_uniq = models.Constraint("UNIQUE(name)", "Tag name must be unique.")