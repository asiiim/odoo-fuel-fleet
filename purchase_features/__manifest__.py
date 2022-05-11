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
    """,
    'sequence': '1',
    'author': "Aashim Bajracharya",
    'website': "https://www.linkedin.com/in/aashim-bajracharya-860406181/",
    'category': 'Purchase',
    'version': '15.0.0.0.1',

    'depends': [
        'purchase',
        'stock'
    ],

    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/terminal.xml',
        'views/realtime_cost.xml',
        'views/menuitem.xml',
    ],

    'application': True
}