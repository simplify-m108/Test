from odoo import models, api, fields, _


class Students(models.Model):

    _name = 'university.student'
    _description = 'Students'
    name = fields.Char('First name', required=True)
    surname = fields.Char('Surname name', required=True)
    email = fields.Char('Email', copy=False)
    enrolled_year = fields.Date('Enrolled year')
    birth_date = fields.Date('Birth date')
    field_of_study = fields.Selection([
        ('aeronautics', 'Aeronautics and Aviation Science'),
        ('art', 'Art'),
        ('business', 'Business Administration'),
        ('chemistry',  'Chemistry'),
        ('economics', 'Economics'),
        ('journalism', 'Journalism and Mass Communication'),
        ('music', 'Music'),
        ('nursing', 'Nursing'),
        ('maths', 'Mathematics'),
        ('pharmacy', 'Pharmacy'),
        ('photography', 'Photography'),
        ('political', 'Political Science and International Relations'),
        ('psychology', 'Psychology'),
        ('statistics', 'Statistics')
    ], 	'Field of Study', default="draft")

    # index_number (unique, generated by odoo and not editable) the format should be Sequence number/Year example 123/2018
    # index_number = fields.Integer('Index Number', unique=True)





