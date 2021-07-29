from odoo import models, api, fields


class Courses(models.Model):
    _name = 'university.courses'
    _description = 'Courses'
    #_inherits = {'university.student': 'field_of_study'}
   # field_of_study = fields.Many2one('university.student', ondelete='cascade', delegate=True)
   # Teacher(selection, without create_new)
    course_name = fields.Char("Course Name", required=True)
    semester = fields.Selection([
       ('1', 'first'),
       ('2', 'second'),
       ('3', 'third'),
       ('4', 'fourth'),
       ('5', 'fifth'),
       ('6', 'sixth'),
       ('7', 'seventh'),
       ('8', 'eighth'),
   ], 	'Semester', default="draft")

   #State (Draft,Open,Finished)read only field in a status bar
    description = fields.Text('Description')
    description_2 = fields.Html('Description', sanitize=True, strip_style=False)
    beginning_date = fields.Date("Beginning Date")
    end_date = fields.Date('End Date')
   #Attachments button where teacher can add lectures,test etc.
   #Students who are enrolled in the course.

   




