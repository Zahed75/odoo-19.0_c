from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):

    _name = "library.book"
    _description = "Library Book"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    _order = "name"

    #  Basic Fields
    name = fields.Char(string="Title", required=True, tracking=True)
    isbn = fields.Char(string="ISBN", copy=False)
    active = fields.Boolean(default=True)
    cover = fields.Image(max_width=512, max_height=512)
    description = fields.Html(string="Description")
    publish_date = fields.Date()
    pages = fields.Integer()
    category = fields.Selection(
        [
            ("fiction", "Fiction"), ("science", "Science"),
            ("history", "History"), ("tech", "Tech"),
            ("children", "Children"), ("fantasy", "Fantasy"),
            ("art", "Art")
        ],
        default="fiction", required=True
    )

    state = fields.Selection(
        [
            ("draft", "Draft"), ("available", "Available"),
            ("borrowed", "Borrowed"), ("lost", "Lost"),
            ("stock_out", "Stock Out")
        ],
        default="draft", required=True
    )

# Money Currency Set for Books

    currency_id= fields.Many2one(
        "res.currency",default = lambda self: self.env.currency_id
    )
    price=fields.Monetary(currency_id="currency_id")

#     relations

    author_id = fields.Many2one("library.author",ondelete="restrict",tracking=True)
    tags_ids= fields.Many2many("library.tag",string="Tags")


# ---- Computed-----
    copies_total = fields.Integer(default=1)
    copies_available = fields.Integer(compute="_compute_copies_available",store=True)


# --------SQL Constraint -------------

    _isbn_uniq = models.Constraint("UNIQUE(ISBN)","ISBN Must be Unique")







