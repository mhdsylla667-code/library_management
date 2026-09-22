from odoo import models, fields

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Auteur de livre'

    name = fields.Char(string='Nom complet', required=True)
    bio = fields.Text(string='Biographie')
    birth_date = fields.Date(string='Date de naissance')
    book_ids = fields.Many2many(
        'library.book',
        string='Livres écrits'
    )