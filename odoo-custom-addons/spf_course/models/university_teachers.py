from odoo import models, api, fields


class Teachers(models.Model):
    _name = 'university.teachers'
    _description = 'Teachers'
    name = fields.Char("Name", required=True)
    surname = fields.Char("Surname", required=True)
    email = fields.Char('Email', copy=False)
    # course they're teaching