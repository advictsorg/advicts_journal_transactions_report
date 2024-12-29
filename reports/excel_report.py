from odoo import models


class JournalTransactionsXlsx(models.AbstractModel):
    _name = 'report.advicts_journal_transactions_report.transactions_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, report):
        style = workbook.add_format({
            'bold': True,
            'bg_color': '#c9c5c5',
            'border': 1,  # 1 is for a thin border
            'valign': 'vcenter',
            'align': 'center'
        })
        style_data = workbook.add_format({
            'border': 1,  # 1 is for a thin border
            'valign': 'vcenter',
            'align': 'center',
        })
        style_data_row = workbook.add_format({
            'border': 1,  # 1 is for a thin border
            'valign': 'vcenter',
            'bg_color': '#EEEEEE',
            'align': 'center'
        })

        title = 'Journal Transactions Report'

        report_name = title
        sheet = workbook.add_worksheet(report_name[:31])
        sheet.merge_range("A1:F1", title, style)
        sheet.merge_range("A2:C2", data['journal'], style)
        sheet.write(1, 3, data['start_date'], style)
        sheet.write(1, 4, '-', style)
        sheet.write(1, 5, data['end_date'], style)
        sheet.merge_range("A4:B4", 'Starting Balance', style)
        sheet.merge_range("C4:D4", data['first_transaction_date'], style)
        sheet.merge_range("E4:F4", data['first_transaction_balance'], style)
        sheet.merge_range("A5:B5", 'Ending Balance', style)
        sheet.merge_range("C5:D5", data['last_transaction_date'], style)
        sheet.merge_range("E5:F5", data['last_transaction_balance'], style)
        sheet.write(7, 0, '#', style)
        sheet.write(7, 1, 'Date', style)
        sheet.write(7, 2, 'Partner', style)
        sheet.write(7, 3, 'Label', style)
        sheet.write(7, 4, 'Amount', style)
        sheet.write(7, 5, 'Running Balance', style)
        row = 8
        count = 0
        for line in data['data']:
            row += 1
            count += 1
            sheet.write(row, 0, count, style_data)
            sheet.write(row, 1, line['date'], style_data)
            sheet.write(row, 2, line['partner'], style_data)
            sheet.write(row, 3, line['label'], style_data)
            sheet.write(row, 4, line['amount'], style_data)
            sheet.write(row, 5, line['running_balance'], style_data)
