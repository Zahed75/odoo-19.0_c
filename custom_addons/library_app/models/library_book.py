from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Book"
    _inherit = ["mail.thread", "mail.activity.mixin"]   # chatter + activities
    _order = "name"

    # --- basic fields -------------------------------------------------
    name = fields.Char(string="Title", required=True, tracking=True)
    isbn = fields.Char(string="ISBN", copy=False)
    active = fields.Boolean(default=True)               # enables Archive
    cover = fields.Image(max_width=512, max_height=512)
    description = fields.Html()
    published_date = fields.Date()
    pages = fields.Integer()
    category = fields.Selection(
        [("fiction", "Fiction"), ("science", "Science"),
         ("history", "History"), ("tech", "Technology")],
        default="fiction", required=True,
    )
    state = fields.Selection(
        [("draft", "Draft"), ("available", "Available"), ("lost", "Lost")],
        default="draft", tracking=True,
    )

    # --- money ---------------------------------------------------------
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id,
    )
    price = fields.Monetary(currency_field="currency_id")

    # --- relations -----------------------------------------------------
    author_id = fields.Many2one("library.author", ondelete="restrict", tracking=True)
    tag_ids = fields.Many2many("library.tag", string="Tags")
    loan_ids = fields.One2many("library.loan", "book_id", string="Loans")

    # --- computed ------------------------------------------------------
    copies_total = fields.Integer(default=1)
    copies_available = fields.Integer(compute="_compute_copies_available", store=True)
    loan_count = fields.Integer(compute="_compute_loan_count")

    # --- SQL constraint (Odoo 19 syntax) --------------------------------
    _isbn_uniq = models.Constraint("UNIQUE(isbn)", "ISBN must be unique!")
