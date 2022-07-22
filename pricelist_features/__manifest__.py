# -*- coding: utf-8 -*-
{
    "name": "Pricelist Features",
    "summary": """
        Features added to the pricelist document.
    """,
    "description": """
        Features:
        \n- Add options 'Supplier Cost' and 'Reference' in pricelist price rule record.
    """,
    "sequence": "1",
    "author": "Aashim Bajracharya",
    "website": "https://www.linkedin.com/in/aashim-bajracharya-860406181/",
    "category": "Product",
    "version": "15.0.0.0.1",
    "depends": ["product", "product_realtime_cost"],
    "data": [
        # "security/ir.model.access.csv",
        "views/product_pricelist_views.xml",
    ],
    "application": True,
}
