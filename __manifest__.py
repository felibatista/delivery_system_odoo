{
    'name' : 'Delivery Management',
    'author': 'Felipe Batista',
    'version': '1.0.0',
    'sequence': 1,
    'description': """
        for bootcamp challenge, this module will manage the delivery system.
    """,
    'category': 'Sales',
    'icon': '/delivery_system/static/icon.png',
    'depends' : ['base'],
    'data': [
        'data/ir_sequences_data.xml',
        'views/order_view.xml',
        'views/carrier_view.xml',
        'views/customer_view.xml',
        'views/delivery_menus_view.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
