{
    'name': 'My First App',
    'category': 'myfirst',
    'version': '19.0.1.0.0',
    'summary': 'My first Odoo 19 training module — all basic field types',
    'description': 'Training module: Model → View → Action → Menu wiring with separated XML files (views / actions / menus).',
    'author': 'Zahed Hasan - Engineering Manager at Syscomatic LLC',
    'website': 'https://thezhasan.com/',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv', # ALWAYS FIRST
        'views/myfirst_model_views.xml', # Views Hocche 2nd Load hobe
        'views/myfirst_model_actions.xml',
        'views/myfirst_menus.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
