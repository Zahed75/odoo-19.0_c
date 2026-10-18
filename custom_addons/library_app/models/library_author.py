from auth_passkey._vendor.webauthn.registration.formats import apple
from odoo import api, models, fields


class LibraryAuthor(models.Model):
    _name = "library.author"
    _description = "Book Author"

    _order = "name"

    name = fields.Char(required=True)
    birth_date=fields.Date()
    country_id=fields.Many2one("res.country",string="Books")
    biography=fields.Text()
    books_ids= fields.One2many("library.book","authors_id",string="Books")
    book_count=fields.Integer(compute="_compute_book_count")

    @api.depends("books_ids")
    def _compute_book_count(self):
        for author in self:
            author.book_count = len(author.books_ids)



