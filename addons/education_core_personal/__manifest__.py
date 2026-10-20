{
    "name": "Education Core",
    "version": "1.0",
    "category": "Education",
    "summary": "Student managment, enrollment, attandence, programe, classes",
    "description": """
    Sprint1: Department, Academic Year, Programs, Classes, Timetable,
    Sprint2: Student Application, Enrollment, Document, Portal Account, Email Template,
    Sprint3: Timetable Slots, Attandance(per-period), Leave Request, 75% Threshold Cron, PDf Attandance Report, Faculty Module,
    Sprint4: Classroom /Exam Hall management(education.classroom)

    Part of the Educational ERP system -LWS build in odoo-19.0 community edition by shohan joarder 19.0.1.0.0 | License DPL-1

    """,
    "author": "Shohan Joarder",
    "company": "GDN",
    "maintainer": "Shohan Joarder",
    "website": "https://www.linkedin.com/in/shohan-joarder",
    "live_test_url": "https://www.linkedin.com/in/shohan-joarder",
    "depends": ["base","web","account","hr","mail","portal","phone_validation","website"],
    "external_dependencies": {
        "python": [
            "phonenumbers"
        ],
        "apt": {
            "phonenumbers":"python3-phonenumbers"
        },
        "bin": []
    },
    "demo": [
        # 'data/demo.xml',
    ],
    "assets": {
        "web.assets_backend": [
            # "addons/education_core/static/src/css/education_core.css",
            # "addons/education_core/static/src/js/education_core.js",
        ],
        "web.assets_frontend": [
            # 
        ],
    },
    "images": [
        # "static/description/banner.png",
    ],
    "pre_init_hook": "pre_init_check",
    "post_init_hook": "post_init_check",
    "data": [
        "security/ir.model.access.csv",
        "views/education_views.xml",
        "views/templates.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 1,
}