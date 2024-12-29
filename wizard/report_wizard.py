from odoo import models, fields, _, api
from odoo.exceptions import ValidationError

JOURNAL_DOMAIN = [('type', 'in', ['bank', 'cash'])]  # Constant for readability and reuse


class ReportWizard(models.TransientModel):
    _name = "journal.transactions.report"
    _description = "Journal Transactions Report"

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date', required=True, default=fields.Date.today())
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, domain=JOURNAL_DOMAIN)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.constrains('start_date', 'end_date')
    def _validate_date_range(self):
        """Ensure the start date is earlier than or equal to the end date."""
        if self.start_date and self.start_date > self.end_date:
            raise ValidationError(_('Start Date must be before End Date'))

    def _build_domain(self):
        """Build and return the domain for querying transaction lines."""
        domain = [
            ('date', '<=', self.end_date),
            ('journal_id', '=', self.journal_id.id),
            ('company_id', '=', self.company_id.id),
        ]
        if self.start_date:
            domain.append(('date', '>=', self.start_date))
        return domain

    def _convert_to_company_currency(self, amount, currency, date):
        """Convert the given amount to the company's currency, if necessary."""
        company_currency = self.company_id.currency_id
        if currency != company_currency:
            return currency._convert(
                amount, company_currency, self.company_id, date or fields.Date.today()
            )
        return amount

    def _get_report_data(self):
        transaction_lines = self.env['account.bank.statement.line'].search(self._build_domain())
        company_currency = self.company_id.currency_id

        # Get the first and last transactions
        first_transaction = transaction_lines[:1]
        last_transaction = transaction_lines[-1:]

        first_transaction_balance = (
            self._convert_to_company_currency(first_transaction.running_balance, first_transaction.currency_id,
                                              first_transaction.date)
            if first_transaction and first_transaction.currency_id != company_currency
            else (first_transaction.running_balance if first_transaction else 0.0)
        )

        last_transaction_balance = (
            self._convert_to_company_currency(last_transaction.running_balance, last_transaction.currency_id,
                                              last_transaction.date)
            if last_transaction and last_transaction.currency_id != company_currency
            else (last_transaction.running_balance if last_transaction else 0.0)
        )

        return {
            'journal': self.journal_id.name,
            'data': [
                {
                    'date': move.date,
                    'label': move.payment_ref,
                    'partner': move.partner_id.name if move.partner_id else '',
                    'amount': self._convert_to_company_currency(move.amount, move.currency_id, move.date),
                    'running_balance': self._convert_to_company_currency(
                        move.running_balance, move.currency_id, move.date
                    ),
                    'currency': company_currency.name,
                }
                for move in transaction_lines
            ],
            'start_date': self.start_date or '',
            'end_date': self.end_date,
            'first_transaction_date': first_transaction.date if first_transaction else None,
            'first_transaction_balance': first_transaction_balance,
            'last_transaction_date': last_transaction.date if last_transaction else None,
            'last_transaction_balance': last_transaction_balance,
            'company_currency': company_currency.symbol,
        }

    def action_print_pdf_report(self):
        report_data = self._get_report_data()
        return self.env.ref(
            'advicts_journal_transactions_report.journal_transactions_report_action'
        ).report_action(self, data=report_data)

    def action_print_xlsx_report(self):
        report_data = self._get_report_data()
        return self.env.ref(
            'advicts_journal_transactions_report.journal_transactions_report_action_xlsx'
        ).report_action(self, data=report_data)
