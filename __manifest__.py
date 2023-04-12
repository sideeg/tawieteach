# -*- coding: utf-8 -*-
{
    'name': "Foodics",

    'summary': """
        Foodics API""",

    'description': """
        Link Odoo With Foodics
    """,

    'author': "Ghanem Ibrahim",
    'website': "https://w-ist.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly

    'depends': ['base','sale_management','sale','account','stock','point_of_sale'],



    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_company_views.xml',
        'views/foodics_master_data.xml',
        'views/foodics_discount.xml',
        'views/foodics_delivery_zones.xml',
        'views/foodics_reason.xml',
        'views/foodics_combos.xml',
        'views/foodics_branches.xml',
        'views/foodics_charges.xml',
        'views/foodics_house_account.xml',
        'wizard/foodics_get_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
