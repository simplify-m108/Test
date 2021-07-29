# -*- coding: utf-8 -*-
# from odoo import http


# class SpfCourse/(http.Controller):
#     @http.route('/spf_course//spf_course//', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/spf_course//spf_course//objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('spf_course/.listing', {
#             'root': '/spf_course//spf_course/',
#             'objects': http.request.env['spf_course/.spf_course/'].search([]),
#         })

#     @http.route('/spf_course//spf_course//objects/<model("spf_course/.spf_course/"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('spf_course/.object', {
#             'object': obj
#         })
