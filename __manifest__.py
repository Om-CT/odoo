{
    'name': 'Employee Management',
    'version': '1.0',
    'summary': 'Manage Employee Information',
    'category': 'Human Resources',
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/sample_employees.xml',  
        'views/employee_form_view.xml',
        'security/ir_rules.xml',
        'views/create_method.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
