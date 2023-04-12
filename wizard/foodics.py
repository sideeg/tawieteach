import json
from odoo import fields, models, api, _
import requests
from odoo.exceptions import UserError


class FoodicsGetDataWizard(models.Model):
    _name = 'foodics.get.data.wizard'

    # Connection & Authentication Info Fields
    code = fields.Text("Code", required=True ,default=lambda self: self.env.company.auth_code)
    token = fields.Char("Token" ,default=lambda self: self.env.company.access_token)
    # authentication_id = fields.Many2one(comodel_name='foodics.authentication', string='Authentication', required=True)
    client_id = fields.Char("Client ID", readonly=True, store=True)
    client_secret = fields.Char("Client Secret", readonly=True, store=True)
    redirect_uri = fields.Char("Redirect Url", readonly=True, store=True)
    connection_status = fields.Selection(string='Connection Status',
                                         selection=[('connecting', 'Connecting Successfully'),
                                                    ('not_connecting', 'Not Connecting'), ],
                                         default='not_connecting', readonly=True)
    # Master Data Fields
    is_categories = fields.Boolean("Categories")
    is_products = fields.Boolean("Products")
    is_inventory_category = fields.Boolean("Inventory Category")
    is_inventory_items = fields.Boolean("Inventory Items")
    is_customers = fields.Boolean("Customers")
    is_users = fields.Boolean("Users")
    is_suppliers = fields.Boolean("Suppliers")
    is_taxes = fields.Boolean("Taxes")
    is_taxes_groups = fields.Boolean("Taxes Groups")
    is_discounts = fields.Boolean("Discounts")
    is_delivery_zones = fields.Boolean("Delivery Zones")
    is_warehouses = fields.Boolean("Warehouses")
    is_branches = fields.Boolean("Branches")
    is_reasons = fields.Boolean("Reasons")
    is_payment_method = fields.Boolean("Payment Method")
    is_charges = fields.Boolean("Charges")
    is_combos = fields.Boolean("Combos")

    # Foodics Data Fields
    is_sales_orders = fields.Boolean("Sales Orders")
    is_purchase_orders = fields.Boolean("Purchase Orders")
    is_transfers_order = fields.Boolean("Transfers Order")
    is_transfers_receiving = fields.Boolean("Transfers Receiving")
    is_transfers_sending = fields.Boolean("Transfers Sending")
    is_cost_adjustment = fields.Boolean("Cost Adjustment")
    is_house_account = fields.Boolean("House Account")

    # To Get Data From Foodics
    def get_data(self, parameter):
        api_sand_box_url = "http://api-sandbox.foodics.com/v5/{}".format(parameter)
        sand_box_headers = {'Authorization': self.token,
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'}
        data = requests.get(url=api_sand_box_url, headers=sand_box_headers).json()
        return data

    # To Validate Field
    def check_to_validate(self, model_name, list_field):
        check_data = self.env[model_name].search(list_field).id
        return check_data

    # To Create Foodics Data In Specific Model
    def create_foodics_data(self, model_name, values):
        self.env[model_name].create(values)

    # To Update Foodics Data In Specific Model
    def update_foodics_data(self, record_id, values):
        record_id.write(values)

    # To Get Token
    def get_token(self):
        body = {
            "grant_type": "authorization_code",
            "code": self.code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri
        }
        try:
            token = requests.post(url='https://api-sandbox.foodics.com/oauth/token', data=json.dumps(body),
                                  headers={'Content-Type': 'application/json'}).json()
            self.token = "{} {}".format(token['token_type'], token['access_token'])
            self.connection_status = 'connecting'
            print('/////////////////////////////////////////////////////////////')
            print(self.token)
            print('/////////////////////////////////////////////////////////////')
        except:
            raise UserError(_("Connection Filer"))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Get Data From Foodics',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'foodics.get.data.wizard',
            'res_id': self.id,
            'target': 'new',
        }

    # To Show Success Notification
    def show_success_notification(self, title):
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': (title),
                'message': 'Fetched Successfully',
                'type': 'success',  # types: success,warning,danger,info
                'sticky': False,  # True/False will display for few seconds if false
            },
        }
        return notification

    # To Show Warning Notification
    def show_warning_notification(self, title):
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': (title),
                'message': 'Fetch Error',
                'type': 'warning',  # types: success,warning,danger,info
                'sticky': False,  # True/False will display for few seconds if false
            },
        }
        return notification

    # To Check If Field Is True Get Data From Specific Entity To Model
    def get_data_list(self):
        selection_entity = []
        customers_entity = 'customers?include=addresses'
        if self.is_customers:
            selection_entity.append(customers_entity)
        categories_entity = 'categories'
        if self.is_categories:
            selection_entity.append(categories_entity)
        charges_entity = 'charges'
        if self.is_charges:
            selection_entity.append(charges_entity)
        combos_entity = 'combos'
        if self.is_combos:
            selection_entity.append(combos_entity)
        sale_order_entity = 'orders?include=products.product,customer'
        if self.is_sales_orders:
            selection_entity.append(sale_order_entity)
        purchases_order_entity = 'purchase_orders?include=items,supplier'
        if self.is_purchase_orders:
            selection_entity.append(purchases_order_entity)
        products_entity = 'products'
        if self.is_products:
            selection_entity.append(products_entity)
        inventory_items_entity = 'inventory_items'
        if self.is_inventory_items:
            selection_entity.append(inventory_items_entity)
        inventory_items_category_entity = 'inventory_item_categories'
        if self.is_inventory_category:
            selection_entity.append(inventory_items_category_entity)
        taxes_entity = 'taxes'
        if self.is_taxes:
            selection_entity.append(taxes_entity)
        taxes_groups_entity = 'tax_groups'
        if self.is_taxes_groups:
            selection_entity.append(taxes_groups_entity)
        suppliers_entity = 'suppliers'
        if self.is_suppliers:
            selection_entity.append(suppliers_entity)
        discounts_entity = 'discounts'
        if self.is_discounts:
            selection_entity.append(discounts_entity)
        delivery_zones_entity = 'delivery_zones'
        if self.is_delivery_zones:
            selection_entity.append(delivery_zones_entity)
        reasons_entity = 'reasons'
        if self.is_reasons:
            selection_entity.append(reasons_entity)
        payment_method_entity = 'payment_methods'
        if self.is_payment_method:
            selection_entity.append(payment_method_entity)
        users_entity = 'users'
        if self.is_users:
            selection_entity.append(users_entity)
        warehouses_entity = 'warehouses'
        if self.is_warehouses:
            selection_entity.append(warehouses_entity)
        branches_entity = 'branches'
        if self.is_branches:
            selection_entity.append(branches_entity)
        transfer_orders_entity = 'transfer_orders'
        if self.is_transfers_order:
            selection_entity.append(transfer_orders_entity)
        cost_adjustments_entity = 'cost_adjustments'
        if self.is_cost_adjustment:
            selection_entity.append(cost_adjustments_entity)

        # try:
        # Customer Entity
        if customers_entity in selection_entity:
            model_name = 'res.partner'
            data = self.get_data(customers_entity)
            for customer in data['data']:
                customer_address = ''
                for addrese in customer['addresses']:
                    customer_address = addrese['name']
                check_phone = self.check_to_validate(model_name, [('phone', '=', customer['phone'])])
                if check_phone == False:
                    self.create_foodics_data(model_name, {'name': customer['name'], 'phone': customer['phone'],
                                                          'email': customer['email'], 'street': customer_address})
        # Categories Entity
        if categories_entity in selection_entity:
            model_name = 'product.category'
            data = self.get_data(categories_entity)
            for category in data['data']:
                check_category = self.env[model_name].search([('name', '=', category['name'])]).id
                if check_category == False:
                    self.create_foodics_data(model_name, {'name': category['name']})
        # Charges
        if charges_entity in selection_entity:
            model_name = 'foodics.charges'
            data = self.get_data(charges_entity)
            for charge in data['data']:
                check_charge = self.check_to_validate(model_name, [('name', '=', charge['name'])])
                if check_charge == False:
                    self.create_foodics_data(model_name,
                                             {'name': charge['name'], 'name_localized': charge['name_localized'],
                                              'is_auto_applied': charge['is_auto_applied'], 'value': charge['value'],
                                              'is_open_charge': charge['is_open_charge']})
                else:
                    charge_id = self.env[model_name].browse(check_charge)
                    self.update_foodics_data(charge_id,
                                             {'name': charge['name'], 'name_localized': charge['name_localized'],
                                              'is_auto_applied': charge['is_auto_applied'], 'value': charge['value'],
                                              'is_open_charge': charge['is_open_charge']})

        # Combos
        if combos_entity in selection_entity:
            model_name = 'foodics.combos'
            data = self.get_data(combos_entity)
            for combos in data['data']:
                check_combos = self.check_to_validate(model_name, [('sku', '=', combos['sku'])])
                if check_combos == False:
                    self.create_foodics_data(model_name,
                                             {'name': combos['name'], 'sku': combos['sku'],
                                              'name_localized': combos['name_localized'], 'barcode': combos['barcode'],
                                              'description': combos['description'],
                                              'description_localized': combos['description_localized'],
                                              'image': combos['image'],
                                              'is_active': combos['is_active'],
                                              'is_ready': combos['is_ready'],
                                              })
                else:
                    combos_id = self.env[model_name].browse(check_combos)
                    self.update_foodics_data(combos_id,
                                             {'name': combos['name'], 'sku': combos['sku'],
                                              'name_localized': combos['name_localized'], 'barcode': combos['barcode'],
                                              'description': combos['description'],
                                              'description_localized': combos['description_localized'],
                                              'image': combos['image'],
                                              'is_active': combos['is_active'],
                                              'is_ready': combos['is_ready'],
                                              })
        # Sales Orders Entity
        if sale_order_entity in selection_entity:
            model_name = 'sale.order'
            data = self.get_data(sale_order_entity)
            for sale_order in data['data']:
                check_reference = self.check_to_validate(model_name, [('origin', '=', sale_order['reference'])])
                customer_id = self.check_to_validate('res.partner',
                                                     [('phone', '=', sale_order['customer']['phone'])])
                sale_order_line = []
                for product in sale_order['products']:
                    product_id = self.check_to_validate('product.template',
                                                        [('default_code', '=', product['product']['sku'])])
                    sale_order_line.append(
                        (0, 0, {'product_id': product_id, 'product_uom_qty': product['quantity'],
                                'price_unit': sale_order['products'][0]['product']['price']}))
                if check_reference == False:
                    self.create_foodics_data(model_name,
                                             {'origin': sale_order['reference'], 'partner_id': customer_id,
                                              'date_order': sale_order['due_at'], 'state': 'sale',
                                              'order_line': sale_order_line})
        # Purchase Order Entity
        if purchases_order_entity in selection_entity:
            model_name = 'purchase.order'
            data = self.get_data(purchases_order_entity)
            for purchase_order in data['data']:
                print(purchase_order)
                purchase_order_date = purchase_order['business_date']
                supplier_id = self.check_to_validate('res.partner',
                                                     [('phone', '=', purchase_order['supplier']['phone'])])
                supplier_code = purchase_order['supplier']['code']
                print(purchase_order_date)
                print(supplier_code)
                print(supplier_id)
                for purchase_order_item in purchase_order['items']:
                    print(purchase_order_item)
                #     print('777777777777777777777777777777777777777777777777777')
                #     print(purchase_order_item)
                #     print(purchase_order_item['pivot'])
                #     item_id = self.check_to_validate('product.product',[('default_code','=','inv-'+purchase_order_item['sku'])])
                #     print(item_id)
                #     print('777777777777777777777777777777777777777777777777777')
                # for item in purchase_order['items']:
                #     print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
                #     print(item)
                #     print('------------------------------')
                #     print(item['pivot']['quantity'])
                #     print(item['pivot']['cost'])
                #     print(item['pivot']['unit_to_storage_factor'])
                #     print(item['pivot']['quantity_received'])

        # Product Entity
        if products_entity in selection_entity:
            model_name = 'product.product'
            data = self.get_data(products_entity)
            for product in data['data']:
                print(product)
                check_product = self.env[model_name].search([('default_code', '=', product['sku'])]).id
                if check_product == False:
                    self.create_foodics_data(model_name,
                                             {'name': product['name'], 'default_code': product['sku'],
                                              'list_price': product['price'],
                                              'standard_price': product['cost'],
                                              'barcode': product['barcode']})
        # Inventory Items Entity
        if inventory_items_entity in selection_entity:
            model_name = 'product.product'
            data = self.get_data(inventory_items_entity)
            for item in data['data']:
                check_product = self.env[model_name].search([('default_code', '=', 'inv-' + item['sku'])]).id
                if check_product == False:
                    self.create_foodics_data(model_name,
                                             {'name': item['name'], 'barcode': item['barcode'],
                                              'default_code': 'inv-' + item['sku'],
                                              'standard_price': item['cost']})
        # Inventory Category Entity
        if inventory_items_category_entity in selection_entity:
            model_name = 'product.category'
            data = self.get_data(inventory_items_category_entity)
            for item_category in data['data']:
                check_inventory_category = self.check_to_validate(model_name,
                                                                  [('name', '=', item_category['name'])])
                if check_inventory_category == False:
                    self.create_foodics_data(model_name, {'name': item_category['name']})
        # Taxes Entity
        if taxes_entity in selection_entity:
            model_name = 'account.tax'
            data = self.get_data(taxes_entity)
            for tax in data['data']:
                print(tax['rate'])
                check_tax = self.env[model_name].search([('amount', '=', tax['rate'])]).id
                if check_tax == False:
                    self.env[model_name].create({'name': tax['name'], 'amount': tax['rate']})
        # Taxes Groups Entity
        if taxes_groups_entity in selection_entity:
            model_name = 'account.tax.group'
            data = self.get_data(taxes_groups_entity)
            for tax_group in data['data']:
                check_tax_group = self.check_to_validate(model_name, [('name', '=', tax_group['name'])])
                if check_tax_group == False:
                    self.create_foodics_data(model_name, {'name': tax_group['name']})
        # Suppliers Entity
        if suppliers_entity in selection_entity:
            model_name = 'res.partner'
            data = self.get_data(suppliers_entity)
            for supplier in data['data']:
                check_phone = self.check_to_validate(model_name, [('phone', '=', supplier['phone'])])
                if check_phone == False:
                    self.create_foodics_data(model_name, {'name': supplier['name'], 'phone': supplier['phone'],
                                                          'email': supplier['email'], 'ref': supplier['code']})
        # Discount Entity
        if discounts_entity in selection_entity:
            model_name = 'foodics.discounts'
            data = self.get_data(discounts_entity)
            for discount in data['data']:
                print(discount)
                check_discount = self.check_to_validate(model_name, [('reference', '=', discount['reference'])])
                if check_discount == False:
                    self.create_foodics_data(model_name,
                                             {'name': discount['name'], 'reference': discount['reference'],
                                              'amount': discount['amount'],
                                              'minimum_product_price': discount['minimum_product_price'],
                                              'minimum_order_price': discount['minimum_order_price'],
                                              'maximum_amount': discount['maximum_amount'],
                                              'is_percentage': discount['is_percentage'],
                                              'is_taxable': discount['is_taxable'], })

        # Delivery Zones Entity
        if delivery_zones_entity in selection_entity:
            model_name = 'foodics.delivery.zones'
            data = self.get_data(delivery_zones_entity)
            for delivery_zone in data['data']:
                check_delivery_zone = self.check_to_validate(model_name,
                                                             [('reference', '=', delivery_zone['reference'])])
                if check_delivery_zone == False:
                    self.create_foodics_data(model_name, {
                        'name': delivery_zone['name'], 'reference': delivery_zone['reference']})
        # Reason Entity
        if reasons_entity in selection_entity:
            model_name = 'foodics.reasons'
            data = self.get_data(reasons_entity)
            for reason in data['data']:
                check_reason = self.check_to_validate(model_name, [('name', '=', reason['name'])])
                if check_reason == False:
                    self.create_foodics_data(model_name, {'name': reason['name']})
        # Payment Methods Entity
        if payment_method_entity in selection_entity:
            model_name = 'pos.payment.method'
            data = self.get_data(payment_method_entity)
            for payment_method in data['data']:
                check_payment_method = self.check_to_validate(model_name,
                                                              [('name', '=', payment_method['name'])])
                if check_payment_method == False:
                    self.create_foodics_data(model_name, {'name': payment_method['name']})
        # User Entity
        if users_entity in selection_entity:
            model_name = 'foodics.users'
            data = self.get_data(users_entity)
            for user in data['data']:
                check_user = self.check_to_validate(model_name, [('email', '=', user['email'])])
                if check_user == False:
                    self.create_foodics_data(model_name, {'name': user['name'], 'email': user['email'],
                                                          'phone': user['phone'], 'pin': user['pin'], })

        # Warehouses Entity
        if warehouses_entity in selection_entity:
            model_name = 'stock.location'
            data = self.get_data(warehouses_entity)
            for warehouse in data['data']:
                check_warehouse = self.check_to_validate(model_name, [('name', '=', warehouse['name'])])
                if check_warehouse == False:
                    self.create_foodics_data(model_name, {'name': warehouse['name']})

        # Branches Entity
        if branches_entity in selection_entity:
            model_name = 'foodics.branches'
            data = self.get_data(branches_entity)
            for branch in data['data']:
                check_branch = self.check_to_validate(model_name, [('phone', '=', branch['phone'])])
                if check_branch == False:
                    self.create_foodics_data(model_name, {'name': branch['name'], 'latitude': branch['latitude'],
                                                          'longitude': branch['longitude'],
                                                          'phone': branch['phone'],
                                                          'open_from': branch['opening_from'],
                                                          'open_to': branch['opening_to'],
                                                          'receives_online_orders': branch[
                                                              'receives_online_orders'],
                                                          'reference': branch['reference']})

        # Transfer Orders Entity
        if transfer_orders_entity in selection_entity:
            pass

            # model_name = 'stock.picking'
            # data = self.get_data(transfer_orders_entity)
            # print(data)

        # except:
        #     raise UserError(_("Get Data Filer"))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Get Data From Foodics',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'foodics.get.data.wizard',
            'res_id': self.id,
            'target': 'new',
        }
