{
    'name': "mytest_api_test",
    'summary': "Manage books easily",
    'description': """
Manage Library
==============
Description related to library.
""",
    'author': "Your name",
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '15.0.13.0.1.0.1',
    'depends': ['base', 'account', 'sale', 'sale_management', 'product', 'mail', 'hr', 'crm', 'purchase',
                'purchase_stock', 'product_matrix', 'test_purchase'],
    'data': ['security/ir.model.access.csv',
             'data/mail_data.xml',
             'views/cron_send_mail.xml',
             ],
    'demo': ['data/demo.xml'],
}
