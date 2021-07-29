from odoo import models, fields, api
#from odoo.exceptions import ValidationError
from odoo import exceptions
#from odoo.exceptions import UserError
#from odoo.tools.translate import _logger
#from odoo.tests.common import Form
from datetime import timedelta

import logging

_logger = logging.getLogger(__name__)

class BaseArchive(models.AbstractModel):
	_name = 'base.archive'
	active = fields.Boolean(default=True)

	def do_archive(self):
		for record in self:
			record.active = not record.active


class LibraryBook(models.Model):
	_name = 'library.book'
	_description = 'Library Book'
	_order = 'date_release desc, name'
	_rec_name = 'short_name'
	_inherit = ['base.archive']
	short_name = fields.Char('Short Title', translate=True, index=True)
	name = fields.Char('Title', required=True)
	isbn = fields.Char('ISBN')
	old_edition = fields.Many2one('library.book', string='Old Edition')
	notes = fields.Text('Internal Notes')
	manager_remarks = fields.Text('Manager Remarks')
	state = fields.Selection(
		[
			('draft', 'Not Available'),
		 	('available', 'Available'),
			('borrowed', 'Borrowed'),
		 	('lost', 'Lost')
		],
		'State', default="draft"
	)
	cost_price = fields.Float('Book Cost', digits='Book Price')
	currency_id = fields.Many2one(
		'res.currency', string='Currency'
	)
	retail_price = fields.Monetary(
		'Retail Price',
		# optional : currency_field='currency_id',
	)
	description = fields.Html('Description', sanitize=True, strip_style=False)
	cover = fields.Binary('Book Cover')
	out_of_print = fields.Boolean('Out of Print?')
	date_release = fields.Date('Release Date')

	def book_rent(self):
		self.ensure_one()
		if self.state != 'available':
			raise exceptions.UserError(_logger('Book is not available for renting'))
		rent_as_superuser = self.env['library.book.rent'].sudo()
		rent_as_superuser.create({
			'book_id': self.id,
			'borrower_id': self.env.user.partner_id.id,
		})

	def find_book(self):
		domain = [
			'|',
				'&', ('name', 'ilike', 'Book Name'), ('category_id.name', 'ilike', 'Category Name'),
				'&', ('name', 'ilike', 'Book Name 2'), ('category_id.name', 'ilike', 'Category Name 2')
		]
		books = self.search(domain)

	def change_release_date(self):
		self.ensure_one()
		self.date_release = fields.Date.today()

	date_updated = fields.Datetime('Last Updated')

	def change_update_date(self):
		self.ensure_one()
		self.update({
			'date_release': fields.Datetime.now(),
			'another_field': 'value'
		})
	pages = fields.Integer(
			'Number of Pages',
			groups='base.group_user',
			states={'lost': [('readonly', True)]},
			help='Total book page count', company_dependent=False
			)
	reader_rating = fields.Float(
		'Reader Average Rating',
		digits=(14, 4),  # Optional precision decimals
	)
	author_ids = fields. Many2many(
		'res.partner',
		string='Authors'
	)
	# will create new table in dbeaver with name library.book + res.partner +relation = "library_book_res_partner_rel"
	#MODIFIKACIJA:
	author_id = fields.Many2one(
		'res.partner',
		string='Author'
	)
	# will not create table, will change author_id in dbeaver directly

	def name_get(self):
		result = []
		for book in self:
			authors = book.author_ids.mapped('name')
			name = '%s (%s)' % (book.name, ', '.join(authors))
			result.append((book.id, name))
			return result

# Search for library.book by book's title, one of the authors or ISBN number:
	@api.model
	def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
		args = [] if args is None else args.copy()
		if not(name == '' and operator == 'ilike'):
			args += ['|', '|',
					('name', operator, name),
					('isbn', operator, name),
					('author_ids.name', operator, name)
					]
		return super(LibraryBook, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


	publisher_id = fields.Many2one(
		'res.partner', string='Publisher',
		# optional:
		ondelete='set null',
		context={},
		domain=[],
	)
	publisher_city = fields.Char(
		'Publisher City', related='publisher_id.city', readonly=True
	)
	age_days = fields.Float(
		string='Days Since Release',
		compute='_compute_age',
		inverse='_inverse_age',
		search='_search_age',
		store=False, # optional
		compute_sudo=True # optional
	)
	# rent_ids = fields.One2many('library.book.rent', 'book_id', string='rent ids')
	@api.depends('date_release')
	def _compute_age(self):
		today = fields.Date.today()
		for book in self:
			if book.date_release:
				delta = today - book.date_release
				book.age_days = delta.days
			else:
				book.age_days = 0
	def _inverse_age(self):
		today = fields.Date.today()
		for book in self.filtered('date_release'):
			d = today - timedelta(days=book.age_days)
			book.date_release = d
	def _search_age(self, operator, value):
		today = fields.Date.today()
		value_days = timedelta(days=value)
		value_date = today - value_days
		# convert the operator:
		# book with age > value have a date < value_date
		operator_map = {
			'>': '<', '>=': '<=',
			'<': '>', '<=': '>=',
		}
		new_op = operator_map.get(operator, operator)
		return [('date_release', new_op, value_date)]


	@api.model
	def _referencable_models(self):
		models = self.env['ir.model'].search([
			('field_id.name', '=', 'message_ids')
		])
		return [(x.model, x.name) for x in models]

	@api.model
	def book_with_multiple_authors(self, all_books):
		def predicate(book):
			if len(book.author_ids) > 1:
				return True
			return False
		return all_books.filter(predicate)
	@api.model
	def get_author_names(self, books):
		return books.mapped('author_ids.name')

	@api.model
	def sort_books_by_date(self, books):
		return books.sorted(key='release_date')


	ref_doc_id = fields.Reference(
		selection='_referencable_models',
		string='Reference Document'
	)

	category_id = fields.Many2one('library.book.category')

	_sql_constraints = [
		('name_uniq', 'UNIQUE (name)', 'Book title must be unique.'),
		('positive_page', 'CHECK(pages>0)', 'No of pages must be positive.')
	]

	@api.constrains('date_release')
	def _check_release_date(self):
		for record in self:
			if record.date_release and record.date_release > fields.Date.today():
				raise models.ValidationError('Release date must be in the past')

	@api.model
	def is_allowed_transition(self, old_state, new_state):
		allowed = [('draft', 'available'), ('available', 'borrowed'), ('borrowed', 'available'),
				   ('available', 'lost'), ('borrowed', 'lost'), ('lost', 'available')]
		return (old_state, new_state) in allowed

	def change_state(self, new_state):
		for book in self:
			if book.is_allowed_transition(book.state, new_state):
				book.state = new_state
			else:
				msg = _logger('Moving from %s is not allowed') % (book.state, new_state)
				raise exceptions.UserError(msg)

	def make_available(self):
		self.change_state('available')

	def make_borrowed(self):
		self.change_state('borrowed')

	def make_lost(self):
		self.ensure_one()
		self.state = 'lost'
		if not self.env.context.get('avoid_deactivate'):
			self.active = False

	def log_all_library_members(self):
		#This is an empty recordset of model library.member
		library_member_model = self.env['library.member']
		all_members = library_member_model.search([])
		print("ALL MEMBERS:", all_members)
		return True

	def average_book_occupation(self):
		self.flush()
		sql_query = """
		SELECT
		lb.name,
		avg((EXTRACT(epoch from age(return_date, rent_date)) / 86400))::int
		FROM
		library_book_rent AS lbr
		JOIN
		library_book as lb ON lb.id = lbr.book_id
		WHERE lbr.state = 'returned'
		GROUP BY lb.name;"""
		self.env.cr.execute(sql_query)
		result = self.env.cr.fetchall()
		_logger.info("Average book occupation: %s", result)

	@api.model
	def _get_average_cost(self):
		grouped_result = self.read_group(
			[('cost_price', "!=", False)],  # Domain
			['category_id', 'cost_price:avg'],  # Fields to access
			['category_id']  # group_by
		)
		return grouped_result

	@api.model
	def _update_book_price(self):
		all_books = self.search([])
		for book in all_books:
			book.cost_price += 10

	def return_all_books(self):
		self.ensure_one()
		wizard = self.env['library.return.wizard']
		with BaseArchive(wizard) as return_form:
			return_form.borrower.id = self.env.user.partner_id
			record = return_form.save()
			record.books_return()


class ResPartner(models.Model):
	_inherit = 'res.partner'
	_order = 'name'

	published_book_ids = fields.One2many(
		'library.book', 'publisher_id',
		string='Published Books'
	)
	authored_book_ids = fields.Many2many(
		'library.book',
		string='Authored Books',
			# relation = 'library_book_res_partner_rel' # optional
	)
	count_books = fields.Integer(
		'Number of Authored Books', compute='_compute_count_books'
	)
	@api.depends('authored_book_ids')
	def _compute_count_books(self):
		for r in self:
			r.count_books = len(r.authored_book_ids)




class LibraryMember(models.Model):
	_name = 'library.member'
	_inherits = {'res.partner': 'partner_id'}
	# _description = 'Library Member'
	partner_id = fields.Many2one('res.partner', ondelete='cascade', delegate=True)
	date_start = fields.Date('Member Since')
	date_end = fields.Date('Termination Date')
	member_number = fields.Char()
	date_of_birth = fields.Date('Date of birth')


class BookCategory(models.Model):
	_name = 'library.book.category'

	name = fields.Char('Category')
	description = fields.Text('Description')

