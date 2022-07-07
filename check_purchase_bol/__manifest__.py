# -*- coding: utf-8 -*-
{
    "name": "Purchase Orders By Bill of Lading",
    "summary": """
        Check and view purchase order by entered Bill of Lading reference.
    """,
    "sequence": "1",
    "author": "Aashim Bajracharya",
    "website": "https://www.linkedin.com/in/aashim-bajracharya-860406181/",
    "category": "Purchase",
    "version": "14.0.0.0.1",
    "depends": ["purchase_features"],
    "data": [
        # 'security/security.xml',
        "security/ir.model.access.csv",
        "wizards/purchase_bol.xml",
    ],
    "application": True,
}
