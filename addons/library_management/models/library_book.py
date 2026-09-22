from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Livre de la bibliothèque'

    name = fields.Char(string='Titre', required=True)
    isbn = fields.Char(string='ISBN')
    author_ids = fields.Many2many('library.author', string='Auteurs')
    
    author_id = fields.Many2one('library.author', string='Auteur principal', compute='_compute_author_id', store=True)
    
    category_id = fields.Many2one('library.category', string='Catégorie')
    publication_date = fields.Date(string='Date de publication')  #
    pages = fields.Integer(string='Nombre de pages')
    image = fields.Binary(string='Couverture')
    active = fields.Boolean(string='Actif', default=True)
    
    state = fields.Selection([
        ('available', 'Disponible'),
        ('borrowed', 'Emprunté'),
        ('lost', 'Perdu'),
    ], string='Statut', compute='_compute_state', store=True, readonly=True)

    loan_ids = fields.One2many('library.loan', 'book_id', string='Historique des emprunts')

    @api.depends('author_ids')
    def _compute_author_id(self):
        for record in self:
            record.author_id = record.author_ids[:1].id if record.author_ids else False

    @api.depends('loan_ids.state')
    def _compute_state(self):
        for record in self:
            ongoing_loan = record.loan_ids.filtered(lambda l: l.state in ['ongoing', 'late'])
            if ongoing_loan:
                record.state = 'borrowed'
            else:
                record.state = 'available'