# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
import requests
from datetime import datetime, timedelta
from odoo.http import request
from odoo import _
from odoo.addons.website.controllers.main import Home
from odoo import http
import json
import logging
logger = logging.getLogger(__name__)

class Website(Home):

    @http.route('/web', type="http", auth="public", website=True)
    def web_client(self, s_action=None, **kwarg):
        logger.info(_("Authenticated ***********************web_client..!! \n You can close this window now"))
        flag = False
        if kwarg.get('code'):

            foodics_id = http.request.env['res.users'].sudo().search([('id', '=', http.request.uid)],
                                                                       limit=1).company_id
            if foodics_id:
                foodics_id.write({
                    'auth_code_foodics': kwarg.get('code'),
                    # 'realm_id': kwarg.get('realmId')
                })
                client_id = foodics_id.client_id_foodics
                client_secret = foodics_id.client_secret_foodics
                redirect_uri = foodics_id.request_token_url_foodics

                headers = {}
                headers['accept'] = 'application/json'
                payload = {
                    'grant_type': 'authorization_code',
                    'code': str(kwarg.get('code')),
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'redirect_uri': redirect_uri,
                }
                response = requests.post(foodics_id.access_token_url_foodics, data=payload, headers=headers).json()
                if response:
                    parsed_token_response = response
                    if parsed_token_response:
                        token = "{} {}".format(parsed_token_response.get('token_type'), parsed_token_response.get('access_token'))
                        print("************************************************************************")
                        print(token)
                        foodics_id.write({
                            'access_token_foodics': token,
                            'qbo_refresh_token_foodics': parsed_token_response.get('refresh_token'),
                            'access_token_expire_in_foodics': datetime.now() + timedelta(
                                seconds=parsed_token_response.get('expires_in')),
                            'refresh_token_expire_in_foodics': datetime.now() + timedelta(
                                seconds=parsed_token_response.get('expires_in'))
                        })
                        logger.info(_("Authorized successfully...!!"))
                        flag = True
            if flag:
                logger.info(_("Authenticated Successfully..!! \n You can close this window now"))
            else:
                logger.info(_("Something went wrong, Authentication was not completed Successfully..!!"))

        return super(Website,self).web_client(s_action=s_action,**kwarg)
     # @http.route('/web', type='http', auth="none")
     # def web_client(self, s_actoin=None, **kw):
     #    if request.params.get('code'):
     #        print("#"*10,request.params.get('code'),"#"*10)
     #        body = {
     #        "grant_type": "authorization_code",
     #        "code": request.params.get('code'),
     #        "client_id": "94227ce2-bace-4a11-8d02-8217f35ad058",
     #        "client_secret": "l2Z4AJLQrcYuZ6ZgYN6reKkGx7MAZemzLXoeQnfy",
     #        "redirect_uri":"http://localhost:8069/web"}
     #        print(body)
     #        # try:
     #        response = request.post(url='https://api-sandbox.foodics.com/oauth/token', data=json.dumps(body),
     #                              headers={'Content-Type': 'application/json'}).json()
     #        token = "{} {}".format(response['token_type'], response['access_token'])
     #        connection_status = 'connecting'

     #        print('/////////////////////////////////////////')
     #        print(token)
     #        print('/////////////////////////////////////////')
     #    return super(Website,self).web_client(s_action=s_actoin,**kw)

     # # @staticmethod
     # def getToken(code):
     #    body = {
     #        "grant_type": "authorization_code",
     #        "code": code,
     #        "client_id": "94227ce2-bace-4a11-8d02-8217f35ad058",
     #        "client_secret": "l2Z4AJLQrcYuZ6ZgYN6reKkGx7MAZemzLXoeQnfy",
     #        "redirect_uri":"http://localhost:8069/web"}
     #    print(body)
     #    # try:
     #    response = request.post(url='https://api-sandbox.foodics.com/oauth/token', data=json.dumps(body),
     #                          headers={'Content-Type': 'application/json'}).json()
     #    token = "{} {}".format(response['token_type'], response['access_token'])
     #    connection_status = 'connecting'

     #    print('/////////////////////////////////////////')
     #    print(token)
     #    print('/////////////////////////////////////////')
     #    # except e:
     #    _logger.error('Error Connection Filer',e)
     #        # raise UserError(_("Connection Filer"))




class Custom_Foodics_controller(http.Controller):

    @http.route('/get_auth_code_foodocs', type="http", auth="public", website=True)
    def get_auth_code_foodocs(self, s_action=None, **kwarg):
        logger.info(_("Authenticated ***********************web_client..!! \n You can close this window now"))
        flag = False
        if kwarg.get('code'):

            foodics_id = http.request.env['res.users'].sudo().search([('id', '=', http.request.uid)],
                                                                       limit=1).company_id
            if foodics_id:
                foodics_id.write({
                    'auth_code_foodics': kwarg.get('code'),
                    # 'realm_id': kwarg.get('realmId')
                })
                client_id = foodics_id.client_id_foodics
                client_secret = foodics_id.client_secret_foodics
                redirect_uri = foodics_id.request_token_url_foodics

                headers = {}
                headers['accept'] = 'application/json'
                payload = {
                    'grant_type': 'authorization_code',
                    'code': str(kwarg.get('code')),
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'redirect_uri': redirect_uri,
                }
                response = requests.post(foodics_id_foodics.access_token_url, data=payload, headers=headers).json()
                if response:
                    parsed_token_response = response
                    if parsed_token_response:
                        token = "{} {}".format(parsed_token_response.get('token_type'), parsed_token_response.get('access_token'))
                        print(token)
                        foodics_id.write({
                            'access_token_foodics': token,
                            'qbo_refresh_token_foodics': parsed_token_response.get('refresh_token'),
                            'access_token_expire_in_foodics': datetime.now() + timedelta(
                                seconds=parsed_token_response.get('expires_in')),
                            'refresh_token_expire_in_foodics': datetime.now() + timedelta(
                                seconds=parsed_token_response.get('expires_in'))
                        })
                        logger.info(_("Authorized successfully...!!"))
                        flag = True
            if flag:
                logger.info(_("Authenticated Successfully..!! \n You can close this window now"))
            else:
                logger.info(_("Something went wrong, Authentication was not completed Successfully..!!"))

        return super(Website,self).web_client(s_action=s_action,**kwarg)
     # @http.route('/web', type='http', auth="none")
     # def web_client(self, s_actoin=None, **kw):
     #    if request.params.get('code'):
     #        print("#"*10,request.params.get('code'),"#"*10)
     #        body = {
     #        "grant_type": "authorization_code",
     #        "code": request.params.get('code'),
     #        "client_id": "94227ce2-bace-4a11-8d02-8217f35ad058",
     #        "client_secret": "l2Z4AJLQrcYuZ6ZgYN6reKkGx7MAZemzLXoeQnfy",
     #        "redirect_uri":"http://localhost:8069/web"}
     #        print(body)
     #        # try:
     #        response = request.post(url='https://api-sandbox.foodics.com/oauth/token', data=json.dumps(body),
     #                              headers={'Content-Type': 'application/json'}).json()
     #        token = "{} {}".format(response['token_type'], response['access_token'])
     #        connection_status = 'connecting'

     #        print('/////////////////////////////////////////')
     #        print(token)
     #        print('/////////////////////////////////////////')
     #    return super(Website,self).web_client(s_action=s_actoin,**kw)

     # # @staticmethod
     # def getToken(code):
     #    body = {
     #        "grant_type": "authorization_code",
     #        "code": code,
     #        "client_id": "94227ce2-bace-4a11-8d02-8217f35ad058",
     #        "client_secret": "l2Z4AJLQrcYuZ6ZgYN6reKkGx7MAZemzLXoeQnfy",
     #        "redirect_uri":"http://localhost:8069/web"}
     #    print(body)
     #    # try:
     #    response = request.post(url='https://api-sandbox.foodics.com/oauth/token', data=json.dumps(body),
     #                          headers={'Content-Type': 'application/json'}).json()
     #    token = "{} {}".format(response['token_type'], response['access_token'])
     #    connection_status = 'connecting'

     #    print('/////////////////////////////////////////')
     #    print(token)
     #    print('/////////////////////////////////////////')
     #    # except e:
     #    _logger.error('Error Connection Filer',e)
     #        # raise UserError(_("Connection Filer"))


