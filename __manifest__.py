# -*- coding: utf-8 -*-
{
    'name': "academia",

    'summary': "Gestión de una academia",

    'description': "Gestión de una academia de clases de refuerzo",

    'author': "Judith Alende Martínez - 4847933",
    'website': "",
    'category': 'Academia',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'demo/demo.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
