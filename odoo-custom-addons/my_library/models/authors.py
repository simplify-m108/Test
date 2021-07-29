from odoo import models, fields, api

class Authors(models.Model):
    _name = 'library.book.authors'
    # _inherit = 'library.book'
    _description = 'Authors'