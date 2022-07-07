# -*- coding: utf-8 -*-
{
    "name": "Sales Stock Picking",
    "summary": """
        Have stock picking type selection in Sales Order.
    """,
    "description": """
        Features:
        \n- Add option to select stock picking type in sale order and reflect that picking type in 
            related delivery orders picking type.
    """,
    "sequence": "1",
    "author": "Aashim Bajracharya",
    "website": "https://www.linkedin.com/in/aashim-bajracharya-860406181/",
    "category": "Sale",
    "version": "15.0.0.0.1",
    "depends": ["sale_stock"],
    "data": [
        "views/sale.xml",
    ],
    "application": True,
}
