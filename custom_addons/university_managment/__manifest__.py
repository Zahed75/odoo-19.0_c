{

    'name': 'University Managment',
    'version': '1.0',
    'category': 'University',
    'summary': 'University Managment',
    'description': """ This is University Education Management """,
    'author': 'Zahed Hasan - Engineering Manager at Syscomatic LLC',
    'website': 'https://thezhasan.com/',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/university_students_views.xml',
        'views/university_education_actions.xml',
        'views/university_education_menu.xml'
    ],
    'icon': 'university_managment/static/description/icon.png',
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'sequence': -1

}
