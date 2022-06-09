# -*- coding: utf-8 -*-
{
    'name': "Purchase Features",

    'summary': """
        Add features in purchase document.
    """,
    "description": """
        Features:
        \n- Create a model for terminals.
        \n- Create a model for product costs and updates.
        \n- Get a realtime price while selecting the product in the purchase order line.
        \n- Add the field BOL (Bill of Lading) in Purchase orderline and Receipt Line.
        \n- Set default bill date in Vendor Bill as of Lift Datetime of the Purchase Order.
    """,
    'sequence': '1',
    'author': "Aashim Bajracharya",
    'website': "https://www.linkedin.com/in/aashim-bajracharya-860406181/",
    'category': 'Purchase',
    'version': '14.0.0.0.2',

    'depends': [
        'purchase_stock'
    ],

    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/terminal.xml',
        'views/realtime_cost.xml',
        'views/res_partner.xml',
        'views/purchase.xml',
        'views/stock_picking.xml',
        'views/menuitem.xml',
    ],

    'application': True
}