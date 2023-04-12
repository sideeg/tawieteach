from odoo import fields, models, api, _
import requests
from odoo.exceptions import UserError


class FoodicsGetDataWizard(models.TransientModel):
    _name = 'foodics.get.data.wizard'

    # Connection & Authentication Info Fields
    code = fields.Text("Code", required=True, default=lambda self: self.env.company.auth_code_foodics)
    token = fields.Char("Token", default=lambda self: self.env.company.access_token_foodics)
    pos_id = fields.Many2one(
        'pos.config', string='Point of Sale',
        help="The physical point of sale you will use.",
        required=True,
        default=lambda self: self.env.company.pos_id_foodics)
    charges_id_foodics = fields.Many2one(
        'product.product', string='Charges',
        help="The price of shiping the product.",
        required=False,
        default=lambda self: self.env.company.charges_id_foodics)

    # To Create Foodics Data In Specific Model
    def create_foodics_data(self, model_name, values):
        self.env[model_name].create(values)

    # To Update Foodics Data In Specific Model
    def update_foodics_data(self, record_id, values):
        record_id.write(values)

    # To Get Data From Foodics
    def get_data(self, parameter):
        api_sand_box_url = "http://api-sandbox.foodics.com/v5/{}".format(parameter)
        # api_sand_box_url = 'https://api-sandbox.foodics.com/v5/orders?page=1'
        sand_box_headers = {'Authorization': self.token,
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'}
        data = requests.get(url=api_sand_box_url, headers=sand_box_headers).json()
        
        if data.get('message', False):
            raise UserError(_("Unauthenticated"))
        return data

    def get_customers_entity(self):
        model_name = 'res.partner'
        data = self.get_data('customers?include=addresses')
        for customer in data['data']:
            customer_address = ''
            for addrese in customer['addresses']:
                customer_address = addrese['name']
            check_phone = self.get_odoo_id_by_foodics_id(customer['id'],model_name)

            if check_phone == False:
                self.create_foodics_data(model_name, {
                    'name': customer['name'],
                    'phone': customer['phone'],
                    'email': customer['email'],
                    'street': customer_address,
                    'foodics_id': customer['id'],
                    'customer_rank': 1
                    }
                )

    ###################################################################################################

    def get_categories_entity(self):
        model_name = 'product.category'
        model_name_pos = 'pos.category'
        data = self.get_data('categories')
        for category in data['data']:
            check_category = self.get_odoo_id_by_foodics_id(category['id'],model_name)
            if not check_category:
                self.create_foodics_data(model_name, {'name': category['name'],
                                                      'foodics_id': category['id']})
            check_category = self.get_odoo_id_by_foodics_id(category['id'],model_name_pos)
            if not check_category:
                self.create_foodics_data(model_name_pos, {'name': category['name'],
                                                          'foodics_id': category['id']})

    ##############################################################################################################################

    def get_charges_entity(self):
        model_name = 'foodics.charges'
        data = self.get_data('charges')
        for charge in data['data']:
            check_charge = self.get_odoo_id_by_foodics_id(charge['name'],model_name)
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

    #############################################################################################################################

    def get_combos_entity(self):
        model_name = 'foodics.combos'
        data = self.get_data('combos')
        for combos in data['data']:
            check_combos = self.get_odoo_id_by_foodics_id(combos['sku'],model_name)
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

    #########################################################################################################################################333333
    def get_sale_order_entity(self):
        model_name = 'sale.order'
        data = self.get_data('orders?include=products.product,customer')
        for sale_order in data['data']:
            check_reference = self.get_odoo_id_by_foodics_id(combos['sku'],model_name)
            customer_id = self.get_odoo_id_by_foodics_id(sale_order['customer']['phone'],'res.partner')
            sale_order_line = []
            for product in sale_order['products']:
                product_id = self.get_odoo_id_by_foodics_id(product['product']['sku'],'product.template')
                sale_order_line.append(
                    (0, 0, {'product_id': product_id, 'product_uom_qty': product['quantity'],
                            'price_unit': sale_order['products'][0]['product']['price']}))
            if check_reference == False:
                self.create_foodics_data(model_name,
                                         {'origin': sale_order['reference'], 'partner_id': customer_id,
                                          'date_order': sale_order['due_at'], 'state': 'sale',
                                          'order_line': sale_order_line})

    ######################################################################################################################################################3
    def get_purchases_order_entity(self):
        model_name = 'purchase.order'
        data = self.get_data('purchase_orders?include=items,supplier')
        for purchase_order in data['data']:
            purchase_order_date = purchase_order['business_date']
            supplier_id = self.get_odoo_id_by_foodics_id(purchase_order['supplier']['phone'],'res.partner')
            supplier_code = purchase_order['supplier']['code']
            for purchase_order_item in purchase_order['items']:
                pass

    ############################################################################################################################################3333333

    def get_products_entity(self):
        model_name = 'product.product'
        data = self.get_data('products?include=category')
        for product in data['data']:
            check_product = self.get_odoo_id_by_foodics_id(product['sku'],model_name)
            if check_product == False:
                self.create_foodics_data(model_name,
                 {
                     'foodics_id': product['id'],
                     'name': product['name'], 'default_code': product['sku'],
                     'list_price': product['price'],
                     'standard_price': product['cost'],
                     'barcode': product['barcode'], 'foodics_id': product['id'],
                     'available_in_pos': product['is_active'],
                     'pos_categ_id': self.get_odoo_id_by_foodics_id(product['category']['id'],
                                                                    'pos.category'),
                     'categ_id': self.get_odoo_id_by_foodics_id(product['category']['id'],
                                                                'product.category'),
                     'barcode': product['barcode']
                 })

    ############################################################################################################################################3333333

    def get_inventory_items_entity(self):
        model_name = 'product.product'
        data = self.get_data('inventory_items')
        for item in data['data']:
            check_product = self.self .get_odoo_id_by_foodics_id(item['id'],model_name)()
            if not check_product:
                self.create_foodics_data(model_name,
                                         {'name': item['name'],
                                          'foodics_id': item['id'],
                                          'barcode': item['barcode'],
                                          'default_code':  item['sku'],
                                          'standard_price': item['cost']
                                          })

    ############################################################################################################################################3333333

    def get_inventory_items_category_entity(self):
        model_name = 'product.category'
        data = self.get_data('inventory_item_categories')
        for item_category in data['data']:
            check_inventory_category = self.get_odoo_id_by_foodics_id(item_category['id'],model_name)
            if not check_inventory_category:
                self.create_foodics_data(model_name, 
                    {
                    'name': item_category['name'],
                    'foodics_id': item_category['id'],
                    })

    ############################################################################################################################################3333333

    def get_taxes_entity(self):
        model_name = 'account.tax'
        data = self.get_data('taxes')
        for tax in data['data']:
            check_tax =self.get_odoo_id_by_foodics_id(tax['id'],model_name)
            if not check_tax:
                self.env[model_name].create({'name': tax['name'] + str(tax['rate']) + "%", 'amount': tax['rate']
                                                , 'type_tax_use': 'sale', 'foodics_id': tax['id']})

    ############################################################################################################################################3333333

    def get_taxes_groups_entity(self):
        model_name = 'account.tax.group'
        data = self.get_data('tax_groups')
        for tax_group in data['data']:
            check_tax_group = self.get_odoo_id_by_foodics_id(tax_group['id'],model_name)
            if not check_tax_group:
                self.create_foodics_data(model_name, {'name': tax_group['name'], 'foodics_id': tax_group['id']})

    ############################################################################################################################################3333333

    def get_suppliers_entity(self):
        model_name = 'res.partner'
        data = self.get_data("suppliers")
        for supplier in data['data']:
            check_phone = self.get_odoo_id_by_foodics_id(supplier['id'],model_name)
            if not check_phone:
                self.create_foodics_data(model_name, 
                    {
                    'name': supplier['name'], 
                    'phone': supplier['phone'],
                    'email': supplier['email'], 
                    'ref': supplier['code'],
                    'foodics_id': supplier['id']
                    })

    ############################################################################################################################################3333333

    def get_discounts_entity(self):
        model_name = 'foodics.discounts'
        data = self.get_data("discounts")
        for discount in data['data']:
            check_discount = self.get_odoo_id_by_foodics_id(discount['id'],model_name)
            if check_discount == False:
                self.create_foodics_data(model_name,
                                         {'name': discount['name'], 'reference': discount['reference'],
                                          'amount': discount['amount'],
                                          'minimum_product_price': discount['minimum_product_price'],
                                          'minimum_order_price': discount['minimum_order_price'],
                                          'maximum_amount': discount['maximum_amount'],
                                          'is_percentage': discount['is_percentage'],
                                          'is_taxable': discount['is_taxable'], 
                                          'foodics_id': discount['id']
                                        })

    ############################################################################################################################################3333333

    def get_delivery_zones_entity(self):
        model_name = 'foodics.delivery.zones'
        data = self.get_data('delivery_zones')
        for delivery_zone in data['data']:
            check_delivery_zone = self.get_odoo_id_by_foodics_id(delivery_zone['id'],model_name)
            if not check_delivery_zone:
                self.create_foodics_data(model_name, {
                    'name': delivery_zone['name'],
                    'reference': delivery_zone['reference'],
                    'foodics_id': delivery_zone['id']
                    })

    ############################################################################################################################################3333333

    def get_reasons_entity(self):
        model_name = 'foodics.reasons'
        data = self.get_data('reasons')
        for reason in data['data']:
            check_reason = self.get_odoo_id_by_foodics_id(reason['id'],model_name)
            if not check_reason:
                self.create_foodics_data(model_name, {
                    'name': reason['name'],
                    'foodics_id': reason['id']
                    })

    ############################################################################################################################################3333333

    def get_payment_method_entity(self):

        model_name = 'pos.payment.method'
        data = self.get_data('payment_methods')
        for payment_method in data['data']:
            check_payment_method = self.get_odoo_id_by_foodics_id(payment_method['id'],model_name)
            if not check_payment_method:
                self.create_foodics_data(model_name,
                                         {'name': payment_method['name'], 'foodics_id': payment_method['id']})

    ############################################################################################################################################3333333

    def get_users_entity(self):
        model_name = 'res.users'
        data = self.get_data('users')
        for user in data['data']:

            check_user = self.get_odoo_id_by_foodics_id(user['id'],model_name)
            if not check_user:
                self.create_foodics_data(model_name, {
                    'name': user['name'],
                    'email': user['email'],
                    'phone': user['phone'],
                    'foodics_id': user['id'],
                    'login': user['email']
                })

    ############################################################################################################################################3333333

    def get_warehouses_entity(self):
        model_name = 'stock.location'
        data = self.get_data('warehouses')
        for warehouse in data['data']:
            check_warehouse = self.get_odoo_id_by_foodics_id(warehouse['id'],model_name)
            if not check_warehouse:
                self.create_foodics_data(model_name, 
                    {
                    'name': warehouse['name'],
                    'foodics_id': warehouse['id']
                    })

    ############################################################################################################################################3333333

    def get_branches_entity(self):
        model_name = 'foodics.branches'
        data = self.get_data('branches')
        for branch in data['data']:
            check_branch = self.get_odoo_id_by_foodics_id(branch['id'],model_name)
            if not check_branch:
                self.create_foodics_data(model_name, {
                    'name': branch['name'], 'latitude': branch['latitude'],
                    'longitude': branch['longitude'],
                    'phone': branch['phone'],
                    'open_from': branch['opening_from'],
                    'open_to': branch['opening_to'],
                    'receives_online_orders': branch[
                    'receives_online_orders'],
                    'reference': branch['reference'],
                    'foodics_id': branch['id']
                    })

    ############################################################################################################################################3333333
    def get_odoo_id_by_foodics_id(self, foodics_id, model_name):
        odoo_id = self.env[model_name].search([('foodics_id', '=', foodics_id)],limit=1).id
        return odoo_id


####################################################################################################################################################
    def get_pos_orders(self):

        session = ''
        current_page = 1
        print("test")
        data = self.get_data(
            'orders?page='+str(current_page)+'&include=products.product,customer,products.taxes,creator,payments,payments.payment_method,charges,charges.taxes')
            # 'https://api-sandbox.foodics.com/v5/orders?page=1')
        print(data)
        if not session :
                session = self.open_session()
        self.process_order_data(data,session)
        while current_page < int(data['meta']['last_page']):
            current_page += 1
            data = self.get_data(
            'orders?page='+str(current_page)+'&include=products.product,customer,products.taxes,creator,payments,payments.payment_method,charges,charges.taxes')
            print(data)
            self.process_order_data(data,session)




        for sess in session:
            for order in sess.order_ids:
                for line in order.lines:
                    line._onchange_qty()
                order._onchange_amount_all()

        if session :
            self.close_session(session)


    def open_session(self):
        pos = self.env['pos.config'].search([('id', '=', self.pos_id.id)])
        pos.open_session_cb()
        return pos.current_session_id

    @staticmethod
    def close_session(current_session_id):
        return current_session_id.action_pos_session_closing_control()

    ############################################################################################################################################3333333
    def process_order_data(self,data,session):
        model_name = 'pos.order'
        for pos_order in data['data'][31:32]:
            check_pos_order_id = self.get_odoo_id_by_foodics_id(pos_order['id'],model_name)
            check_customer_id = pos_order['customer']
            customer_id = ''
            # if check_pos_order_id :
            #     continue

            if check_customer_id is not None:
                customer_id = self.get_odoo_id_by_foodics_id(check_customer_id['id'],'res.partner')

            pos_order_line = []
            pos_paymant = []
            total_amount = 0
            total_paid = 0
            total_discount = 0
            bais = 1
            if pos_order['status'] == 5:

               bais = -1

            for pay in pos_order['payments']:
                pos_paymant.append((0, 0, {
                    'amount': pay['amount'],
                    'payment_method_id': self.get_odoo_id_by_foodics_id(pay['payment_method']['id'],
                                                                        'pos.payment.method'),
                    'payment_date': pay['added_at'],
                    'partner_id': customer_id,
                    'session_id': session.id
                }))
                total_paid += pay['tendered']





            totax_tax_amount =0
            total_discount =pos_order['discount_amount']



            td = total_discount / sum( [product['tax_exclusive_unit_price']*product['quantity'] for product in pos_order['products']]+
                 [charges['tax_exclusive_amount'] for charges in pos_order['charges']])* 100
            for product in pos_order['products']:
                product_id = self.get_odoo_id_by_foodics_id(product['product']['id'],'product.product')
                pro = self.env['product.product'].browse([product_id])
                total_amount += product['total_price']
                dis_p = (product['discount_amount'] / (product['total_price'] + product['discount_amount']) * 100)

                pos_order_line.append(
                    (0, 0, {'product_id': product_id, 'full_product_name': product['product']['name'],
                            'qty': bais * product['quantity'],
                            'discount': dis_p +td ,
                            'price_subtotal':   bais * product['tax_exclusive_total_price'],# total Price Without Tax
                            # 'price_subtotal_incl': bais * product['tax_exclusive_total_price'],
                            'price_subtotal_incl': (sum([bais * x['rate'] for x in product['taxes']])/100)*product['tax_exclusive_total_price'] +product['tax_exclusive_total_price'],
                            'tax_ids_after_fiscal_position': [(6, 0, [self.get_odoo_id_by_foodics_id(x['id'],'account.tax') for x in product['taxes']])],
                            'tax_ids': [(6, 0, [self.get_odoo_id_by_foodics_id(x['id'],'account.tax') for x in product['taxes']])],
                            'price_unit': product['tax_exclusive_unit_price'],}))#pos_order['products'][0]['product']['price']}))

                totax_tax_amount += sum([x['pivot']['amount'] for x in product['taxes']])
            # if total_discount > 0:
            #     discount_product_id = self.pos_id.discount_product_id
                # total_amount -= total_discount

                # pos_order_line.append(
                #     (0, 0, {'product_id': discount_product_id.id, 'full_product_name': discount_product_id.name,
                #             'qty': 1,
                #             'discount': 0,
                #             'price_subtotal': x * -1*total_discount  ,# total Price Without Tax
                #             'price_subtotal_incl': x * -1*total_discount, #(sum([x['rate'] for x in product['taxes']])/100)*product['tax_exclusive_total_price']+product['tax_exclusive_total_price'],  # total price with tax
                #             # 'price_subtotal_incl':5,
                #             # 'tax_ids':[(6,0,[6])],
                #             # 'tax_ids_after_fiscal_position': [(6, 0, [self.get_odoo_id_by_foodics_id(x['id'],'account.tax') for x in product['taxes'] ])],
                #             # 'tax_ids': [(6, 0, [self.get_odoo_id_by_foodics_id(x['id'],'account.tax') for x in product['taxes']])],
                #             'price_unit': total_discount,}))#pos_order['products'][0]['product']['price']}))
            if len(pos_order['charges']) > 0:
              for charge in pos_order['charges']:
                totax_tax_amount += sum([x['pivot']['amount'] for x in charge['taxes']])
                total_amount += charge['tax_exclusive_amount']
                pos_order_line.append(
                    (0, 0, {'product_id': self.charges_id_foodics.id, 'full_product_name': self.charges_id_foodics.name,
                            'qty': bais * 1,
                            'discount': td,
                            'price_subtotal':  bais * charge['tax_exclusive_amount'] ,# total Price Without Tax
                            'price_subtotal_incl': (sum([bais * x['rate'] for x in charge['taxes']])/100)*charge['tax_exclusive_amount'] +charge['tax_exclusive_amount'],  # total price with tax
                            'tax_ids_after_fiscal_position': [(6, 0, [self.get_odoo_id_by_foodics_id(x['id'],'account.tax') for x in charge['taxes']])],
                            'tax_ids': [(6, 0, [self.get_odoo_id_by_foodics_id(x['id'],'account.tax') for x in charge['taxes']])],
                            'price_unit': charge['tax_exclusive_amount'],}))#pos_order['products'][0]['product']['price']}))


            self.create_foodics_data(model_name,
                                     {'name': pos_order['reference'], 'state': 'paid', 'partner_id': customer_id,
                                      'date_order': pos_order['due_at'],
                                      'payment_ids': pos_paymant,
                                      'foodics_id':pos_order['id'],
                                      'lines': pos_order_line, 'session_id': session.id,
                                      'amount_tax': bais * totax_tax_amount,
                                      'amount_total': bais * total_amount + totax_tax_amount,
                                      'amount_paid': total_paid,
                                      'amount_return': total_paid - total_amount,

                                      })

