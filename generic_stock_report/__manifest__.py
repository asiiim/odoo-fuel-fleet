# -*- coding: utf-8 -*-
{
    'name': "General Stock Report",

    'summary': """
        Set of useful stock reports.""",

    'description': """
        \n-Opening, Inward, Outward and Closing Stock report.
        \n-Stock report on the basis of product category.
        
    """,

    'author': "Ten Orbits Pvt. Ltd.",
    'website': "https://www.10orbits.com/",
    'category': 'Stock',
    'version': '14.0.0.0.1',
    'depends': ['base','report_xlsx','stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/stock_excel_report.xml',
        
    ],
    'sequence': 1,
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'AGPL-3',
}
