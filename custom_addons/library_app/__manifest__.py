{
    "name": "Libro",
    "version": "19.0.1.0.0",
    "summary": "Books, authors, loans, reports and a dashboard",
    "author": "Library Shop Management",
    "category": "Services",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    # ORDER MATTERS: a file can only reference records loaded before it.
    "data": [
        "security/library_security.xml",
        "security/ir.model.access.csv",
        "views/library_tag_views.xml",
        "views/library_author_views.xml",
        "views/library_books_views.xml",
        "views/library_menus.xml",
    ],
    "demo": [
        # "demo/library_demo.xml",
    ],
    "assets": {
        "web.assets_backend": [
            # "library_app/static/src/dashboard/**/*",
        ],
    },
    'icon': 'library_app/static/description/icon.png',
    "application": True,
    "installable": True,
}
