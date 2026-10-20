from odoo import api, fields, models


class LibraryAuthor(models.Model):
    _name = "library.author"
    _description = "Book Author"
    _order = "name"

    name = fields.Char(required=True)
    birth_date = fields.Date()
    country_id = fields.Many2one("res.country", string="Country")
    biography = fields.Text()
    book_ids = fields.One2many("library.book", "author_id", string="Books")
    book_count = fields.Integer(compute="_compute_book_count")

    @api.depends("book_ids")
    def _compute_book_count(self):
        for author in self:
            author.book_count = len(author.book_ids)

    def action_view_books(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Books",
            "res_model": "library.book",
            "view_mode": "list,form",
            "domain": [("author_id", "=", self.id)],
            "context": {"default_author_id": self.id},
        }