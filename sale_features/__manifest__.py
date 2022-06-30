# -*- coding: utf-8 -*-
{
    'name': "Sales Features",

    'summary': """
        Add features in sales related document.
    """,
    "description": """
        Features:
        \n- Add custom fields: Carrier and Driver in Sales model.
        \n- Add model Fuel Asset to have unique asset ID in the sale, stock and invoice lines.
    """,
    'sequence': '1',
    'author': "Aashim Bajracharya",
    'website': "https://www.linkedin.com/in/aashim-bajracharya-860406181/",
    'category': 'Sale',
    'version': '15.0.0.0.2',

    'depends': [
        'sale_management',
        'stock_features',
        'account',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/fuel_asset.xml',
        'views/sale.xml',
        'views/invoice.xml',
        'views/menuitem.xml'
    ],

    'application': True
}