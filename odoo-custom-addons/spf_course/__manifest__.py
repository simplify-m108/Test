# -*- coding: utf-8 -*-
{
    'name': "Courses",
    'summary': "University module",
    'description': """
      Manage university work
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '13.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/university_student.xml',
        'views/university_teachers.xml',
        'views/university_courses.xml',
        'data/index_number.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

}
