from odoo import models, fields


class LibraryTag(models.Model):
    _name = "library.tag"
    _description = "Book Tag"

    _oder = "name"

    name = fields.Char(
        required=True
    )
    color = fields.Integer()

    _name_uniq = models.Constraint("UNIQUE(name)", "Tag must be unique")
