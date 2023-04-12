# -*- coding: utf-8 -*-
import base64
import json
import logging
from datetime import datetime, timedelta
import requests
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning, AccessError

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    client_id_foodics = fields.Char('Client Id', copy=False,default="94227ce2-bace-4a11-8d02-8217f35ad058", help="The client ID you obtain from the developer dashboard.")
    client_secret_foodics = fields.Char('Client Secret', copy=False,default="l2Z4AJLQrcYuZ6ZgYN6reKkGx7MAZemzLXoeQnfy",
                                help="The client secret you obtain from the developer dashboard.")

    auth_base_url_foodics = fields.Char('Authorization URL', default="https://console-sandbox.foodics.com/authorize",
                                help="User authenticate uri")
    access_token_url_foodics = fields.Char('Authorization Token URL',
                                   default="https://api-sandbox.foodics.com/oauth/token",
                                   help="Exchange code for refresh and access tokens")
    request_token_url_foodics = fields.Char('Redirect URL', default="http://localhost:8069/web",
                                    help="One of the redirect URIs listed for this project in the developer dashboard.")
    pos_id_foodics = fields.Many2one(
        'pos.config', string='Point of Sale',
        help="The physical point of sale you will use.",
        required=True,
        default=lambda self: self.env.company.pos_id_foodics)
    charges_id_foodics = fields.Many2one(
        'product.product', string='Charges',
        help="The price of shiping the product.",
        required=False,
        default=lambda self: self.env.company.charges_id_foodics)
    url_foodics = fields.Char('API URL', default="http://api-sandbox.foodics.com/v5/",
                      help="Intuit API URIs, use access token to call Intuit API's")

    auth_code_foodics = fields.Char('Auth Code', copy=False, help="An authenticated code", company_dependent=True)
    access_token_foodics = fields.Char('Access Token', copy=False, company_dependent=True,
                               help="The token that must be used to access the QuickBooks API. Access token expires in 3600 seconds.")
    minorversion_foodics = fields.Char('Minor Version', copy=False, default="5",
                               help="QuickBooks minor version information, used in API calls.")
    access_token_expire_in_foodics = fields.Datetime('Access Token Expire In', copy=False, help="Access token expire time.")
    qbo_refresh_token_foodics = fields.Char('Refresh Token', copy=False, company_dependent=True,
                                    help="The token that must be used to access the QuickBooks API. Refresh token expires in 8726400 seconds.")
    refresh_token_expire_in_foodics = fields.Datetime('Refresh Token Expire In', copy=False, help="Refresh token expire time.")

    last_acc_imported_id_foodics = fields.Char('Last Imported Account Id', copy=False, default=0)
    last_imported_tax_id_foodics = fields.Char('Last Imported Tax Id', copy=False, default=0)
    last_imported_tax_agency_id_foodics = fields.Char('Last Imported Tax Agency Id', copy=False, default=0)
    last_imported_product_category_id_foodics = fields.Char('Last Imported Product Category Id', copy=False, default=0)
    last_imported_product_id_foodics = fields.Char('Last Imported Product Id', copy=False, default=0,
                                           help="SKU ID should be Unique in QBO")
    last_imported_customer_id_foodics = fields.Char('Last Imported Customer Id', copy=False, default=0)
    last_imported_vendor_id_foodics = fields.Char('Last Imported Vendor Id', copy=False, default=0)
    last_imported_payment_method_id_foodics = fields.Char('Last Imported Payment Method Id', copy=False, default=0)
    last_imported_payment_id_foodics = fields.Char('Last Imported Payment Id', copy=False, default=0)
    last_imported_bill_payment_id_foodics = fields.Char('Last Imported Bill Payment Id', copy=False, default=0)
    quickbooks_last_employee_imported_id_foodics = fields.Integer('Last Employee Id')
    quickbooks_last_dept_imported_id_foodics = fields.Integer('Last Department Id')
    quickbooks_last_sale_imported_id_foodics = fields.Integer('Last Sale Order Id')
    quickbooks_last_invoice_imported_id_foodics = fields.Integer('Last Invoice Id')
    quickbooks_last_purchase_imported_id_foodics = fields.Integer('Last Purchase Order Id')
    quickbooks_last_vendor_bill_imported_id_foodics = fields.Integer('Last Vendor Bill Id')
    quickbooks_last_credit_note_imported_id_foodics = fields.Integer('Last Credit Note Id')
    quickbooks_last_journal_entry_imported_id_foodics = fields.Integer('Last Journal Entry Id')

    start_foodics = fields.Integer('Start', default=1)
    limit_foodics = fields.Integer('Limit', default=100)
    '''  Tracking Fields for Payment Term'''
    x_quickbooks_last_paymentterm_sync_foodics = fields.Datetime('Last Synced On', copy=False)
    x_quickbooks_last_paymentterm_imported_id_foodics = fields.Integer('Last Imported ID', copy=False)

    # suppress_warning_foodics = fields.Boolean('Suppress Warning', default=False, copy=False,help="If you all Suppress Warnings,all the warnings will be suppressed and logs will be created instead of warnings")
    qbo_domain_foodics = fields.Selection([('sandbox', 'Sandbox'), ('production', 'Production')],
                                  string='QBO Domain', default='sandbox')
    qb_account_recievable_foodics = fields.Many2one('account.account', 'Account Recievable')
    qb_account_payable_foodics = fields.Many2one('account.account', 'Account Payable')
    qb_income_account_foodics = fields.Many2one('account.account', 'Income Account')
    qb_expense_account_foodics = fields.Many2one('account.account', 'Expense Account')
    journal_entry_foodics = fields.Many2one('account.journal', help="Journal Entry")

    def login(self):
        print("\n\n\n\n\n*************************************************")
        if not self.client_id_foodics:
            raise AccessError('Please add your Client Id')
        url = self.auth_base_url_foodics + '?client_id=' + self.client_id_foodics
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new"
        }

    def refresh_token(self):
        """Get new access token from existing refresh token"""
        _logger.info("Current Context is ---> {}".format(self._context))
        company_id = self.env['res.users'].search([('id', '=', 2)]).company_id
        _logger.info("COMPANY ID IS  --------------> {}".format(company_id))

        if not company_id:
            company_id = self.env['res.users'].search([('id', '=', 2)]).company_id

        if company_id:
            client_id = company_id.client_id
            client_secret = company_id.client_secret
            if not client_id:
                raise AccessError("Please Configure Server Details")
            raw_b64 = str(client_id + ":" + client_secret)
            raw_b64 = raw_b64.encode('utf-8')
            converted_b64 = base64.b64encode(raw_b64).decode('utf-8')
            auth_header = 'Basic ' + converted_b64
            headers = {}
            # headers['Authorization'] = str(auth_header)
            headers['accept'] = 'application/json'
            payload = {'grant_type': 'refresh_token', 'refresh_token': company_id.qbo_refresh_token}
            _logger.info("Payload is --------------> {}".format(payload))
            access_token = requests.post(company_id.access_token_url, data=payload, headers=headers)
            _logger.info("Access token is --------------> {}".format(access_token.text))
            if access_token:
                parsed_token_response = json.loads(access_token.text)
                _logger.info("Parsed response is ------------------> {}".format(parsed_token_response))
                if parsed_token_response:
                    company_id.write({
                        'access_token': parsed_token_response.get('access_token'),
                        'qbo_refresh_token': parsed_token_response.get('refresh_token'),
                        'access_token_expire_in': datetime.now() + timedelta(
                            seconds=parsed_token_response.get('expires_in')),
                        'refresh_token_expire_in': datetime.now() + timedelta(
                            seconds=parsed_token_response.get('expires_in'))
                    })
                    _logger.info(_("Token refreshed successfully!"))
