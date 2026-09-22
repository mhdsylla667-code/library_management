from odoo import models, fields

class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Catégorie de Livre'
    _order = 'name'

    name = fields.Char(string='Nom de la catégorie', required=True)
    description = fields.Text(string='Description')
    book_ids = fields.One2many('library.book', 'category_id', string='Livres')