# -*- coding: utf-8 -*-
{
    'name': "Sales Price",

    'summary': """
        Get computed price for sales order lines.
    """,
    "description": """
        Features:
        \n- Get price from the product realtime cost register for dropshipping.
    """,
    'sequence': '1',
    'author': "Aashim Bajracharya",
    'website': "https://www.linkedin.com/in/aashim-bajracharya-860406181/",
    'category': 'Sale',
    'version': '15.0.0.0.1',

    'depends': [
        'sale_features',
    ],

    'data': [
        'views/sale.xml',
    ],

    'application': True
}