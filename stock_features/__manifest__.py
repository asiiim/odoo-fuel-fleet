# -*- coding: utf-8 -*-
{
    "name": "Stock Features",
    "summary": """
        Add features in stock related documents.
    """,
    "description": """
        Features:
        \n- Add bill of lading reference in stock picking and stock moves records.
    """,
    "sequence": "1",
    "author": "Aashim Bajracharya",
    "website": "https://www.linkedin.com/in/aashim-bajracharya-860406181/",
    "category": "Stock",
    "version": "14.0.0.0.1",
    "depends": [
        "purchase_features",
    ],
    "data": [
        "views/stock_picking.xml",
        # 'views/stock_move_line.xml',
    ],
    "application": True,
}
