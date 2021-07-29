{
'name': "My Library",
'summary': "Manage books easily",
'description': """
Manage Library
==============
Description related to library.
""",
'author':"Your name",
'website': "http://www.example.com",
'category': 'Uncategorized',
'version': '13.0.1',
'depends': ['base'],
'data': [
    'security/groups.xml',
    'security/ir.model.access.csv',
    'views/library_book.xml',
    'views/library_book_categ.xml',
    'views/library_book_rent.xml',
    'wizard/library_book_rent_wizard.xml',
    'data/data.xml',
    'wizard/library_book_return_wizard.xml',
],
'demo' : [
    'data/demo.xml',
],
}

