# -*- coding: utf-8 -*-
{
    "name": "Partner Features",
    "summary": """
        Add features in purchase document.
    """,
    "description": """
        Features:
        \n- Add boolean fields: is_driver and is_carrier
    """,
    "sequence": "1",
    "author": "Aashim Bajracharya",
    "website": "https://www.linkedin.com/in/aashim-bajracharya-860406181/",
    "category": "Partner",
    "version": "14.0.0.0.1",
    "depends": [
        "contacts",
    ],
    "data": [
        "views/res_partner.xml",
    ],
    "application": True,
}
