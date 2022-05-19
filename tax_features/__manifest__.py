# -*- coding: utf-8 -*-
{
    'name': "Tax Features",

    'summary': """
        Add features related to tax population in sales and purchase workflow.
    """,
    "description": """
        Features:
        \n- Override tax model and add needed fields.
        \n- Get applicable taxes in the orderline while selecting product.
    """,
    'sequence': '1',
    'author': "Aashim Bajracharya",
    'website': "https://www.linkedin.com/in/aashim-bajracharya-860406181/",
    'category': 'Purchase',
    'version': '15.0.0.0.1',

    'depends': [
        'account',
        'purchase'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/tax.xml',
        'views/purchase.xml',
        'views/res_partner.xml'
    ],

    'application': True
}