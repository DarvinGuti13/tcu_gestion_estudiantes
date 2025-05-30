# -*- coding: utf-8 -*-
{
    'name': "TCU Estudiantes",
    'summary': "Gestión de estudiantes para el TCU",
    'description': "Módulo para controlar y registrar estudiantes del TCU",
    'author': "Darvin Gutiérrez",
    'category': 'Educación',
    'version': '0.1',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/tcu_periodo_views.xml',
        'views/tcu_estudiante_views.xml',
        'data/mail_templates.xml',
    ],
    'installable': True,
    'application': True,
}

