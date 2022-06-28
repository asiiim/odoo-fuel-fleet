# -*- coding: utf-8 -*-
{
    'name': "Sales Features",

    'summary': """
        Add features in sales related document.
    """,
    "description": """
        Features:
        \n- Add custom fields: Carrier and Driver in Sales model.
    """,
    'sequence': '1',
    'author': "Aashim Bajracharya",
    'website': "https://www.linkedin.com/in/aashim-bajracharya-860406181/",
    'category': 'Sale',
    'version': '15.0.0.0.1',

    'depends': [
        'stock_features',
        'account',
    ],

    'data': [
        # 'views/res_partner.xml',
        'views/sale.xml',
        # 'views/invoice.xml',
    ],

    'application': True
}