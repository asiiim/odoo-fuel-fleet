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
        \n- Update taxes in the product when changing destination value.
        \n- Add a register to collect realtime tax rates.
    """,
    'sequence': '1',
    'author': "Aashim Bajracharya",
    'website': "https://www.linkedin.com/in/aashim-bajracharya-860406181/",
    'category': 'Purchase',
    'version': '14.0.0.0.2',

    'depends': [
        'account',
        'purchase'
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/tax.xml',
        'views/purchase.xml',
        'views/res_partner.xml',
        'views/realtime_tax_rate.xml',
        'views/menuitem.xml'
    ],

    'application': True
}