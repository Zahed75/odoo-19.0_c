# -*- coding: utf-8 -*-
###############################################################################
#
#    Zahed Hasan — Engineering Manager at Syscomatic LLC
#
#    Copyright (C) 2026-TODAY Zahed Hasan(
#    <https://thezhasan.com/>).
#    Author: Zahed Hasan(<https://thezhasan.com/>)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (
#    OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the
#    Software or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
###############################################################################


{
    "name": "Education Core",
    "version": "19.0.1.0.0",
    "category": "Education",
    "summary": "Student management,enrollment,attendance,timetable,program,classes",
    "description": """
        
        Sprint1: Departments,Academic Years,Programs,Classes,Timetable,
        Sprint2:Student Applications,Enrollment,Documents,Portal Accounts,Email Temaplate
        Sprint3: Timetable Slots,Attendance(per-period),Leave Requests, 75% Threshold Cron,
        PDF Attendance Report , Faculty Module
        Sprint4:Classroom /Exam Hall management(education.classroom)
        Reporting:menu :Attendance summary Report and Attendance Analysis (List/Pivot/graph)
        
    Part of the Educational ERP system -LMS built in odoo-19.0 community edition by Zahed Hasan
    Version: 19.0.1.0.0 | License-OPL-1
    """,

    "author": "Zahed Hasan",
    "company": "Fair Group",
    "maintainer": "Zahed Hasan",
    "website": "https://thezhasan.com/",
    "live_test_url": "https://thezhasan.com/",
    "depends": [
        "base",
        "web",
        "account",
        "hr",
        "mail",
        "phone_validation",
        "portal"
    ],

    "external_dependencies": {
        "python": ["phonenumbers"],
        "apt": {
            "phonenumbers": "python3-phonenumbers"
        },
    },
    "data": [

    ],
    "demo": [
        # "demo/education_demo.xml"
    ],
    "assets": {
        "web.assets_frontend": [
            # "education_core/static/src/js/education_core.js"
        ],
        "web.assets_backend": [
            # "education_core/static/src/js/education_core.js"
        ]
    },

    "images": [

    ],

    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init",
    "installable": True,
    "application": True,
    "auto-install": False,
    "squence": 1,

}
