# -*- coding: utf-8 -*-
{
    'name': "Advicts Journal Transactions Report",
    'summary': """ Report to Calculate the Journal Transactions depend on Date (from - to) """,
    'description': """ Report to Calculate the Journal Transactions depend on Date (from - to) """,
    'author': "GhaithAhmed@Advicts",
    'website': "https://advicts.com",
    'category': 'Accounting',
    'version': '1.0',
    'depends': ['base', 'account', 'account_accountant', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/report_wizard.xml',
        'views/views.xml',
        'reports/reports.xml',
        'reports/report_template.xml',
    ],
}
