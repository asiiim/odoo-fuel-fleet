# -*- coding: utf-8 -*-
{
    "name": "Product Realtime Cost",
    "summary": """
        Realtime Cost Register of Products.
    """,
    "description": """
        Features:
        \n- Create a model for terminals.
        \n- Create a model for product costs and updates.
    """,
    "sequence": "1",
    "author": "Aashim Bajracharya",
    "website": "https://www.linkedin.com/in/aashim-bajracharya-860406181/",
    "category": "Product",
    "version": "14.0.0.0.1",
    "depends": ["stock"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/terminal.xml",
        "views/realtime_cost.xml",
        "views/menuitem.xml",
    ],
    "application": True,
}
