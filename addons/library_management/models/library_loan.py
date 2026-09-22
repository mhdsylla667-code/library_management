# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Emprunt'
    _order = 'loan_date desc, id desc'

    name = fields.Char(
        string="Référence",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('Nouveau'),
    )
    book_id = fields.Many2one('library.book', string="Livre", required=True)
    borrower_id = fields.Many2one(
        'res.partner',
        string="Emprunteur",
        required=True,
        default=lambda self: self.env.user.partner_id,
    )
    loan_date = fields.Date(
        string="Date d'emprunt",
        default=fields.Date.context_today,
        required=True,
    )
    due_date = fields.Date(
        string="Date de retour prévue",
        compute='_compute_due_date',
        store=True,
        readonly=True,
    )
    return_date = fields.Date(string="Date de retour effective", readonly=True, copy=False)
    state = fields.Selection(
        [
            ('draft', 'Brouillon'),
            ('ongoing', 'En cours'),
            ('returned', 'Rendu'),
            ('late', 'En retard'),
        ],
        string="Statut",
        default='draft',
        copy=False,
        required=True,
    )

    @api.depends('loan_date')
    def _compute_due_date(self):
        for loan in self:
            if loan.loan_date:
                loan.due_date = loan.loan_date + timedelta(days=14)
            else:
                loan.due_date = False

    @api.constrains('state', 'book_id')
    def _check_book_not_already_borrowed(self):
        """Un livre déjà 'borrowed' (emprunté via un autre emprunt en cours
        ou en retard) ne peut pas faire l'objet d'un nouvel emprunt actif."""
        for loan in self:
            if loan.state in ('ongoing', 'late'):
                conflicting = self.search([
                    ('id', '!=', loan.id),
                    ('book_id', '=', loan.book_id.id),
                    ('state', 'in', ('ongoing', 'late')),
                ])
                if conflicting:
                    raise ValidationError(
                        _("Le livre « %s » est déjà emprunté et ne peut pas être "
                          "emprunté à nouveau tant qu'il n'a pas été rendu.")
                        % loan.book_id.name
                    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nouveau')) == _('Nouveau'):
                vals['name'] = self.env['ir.sequence'].next_by_code('library.loan') or _('Nouveau')
        return super().create(vals_list)

    def action_confirm(self):
        self.write({'state': 'ongoing'})

    def action_return(self):
        self.write({
            'state': 'returned',
            'return_date': fields.Date.context_today(self),
        })

    def action_cancel(self):
        self.write({'state': 'draft'})

    @api.model
    def _cron_mark_late_loans(self):
        """À appeler par une action planifiée (ir.cron) : passe en 'late'
        tout emprunt en cours dont la date de retour prévue est dépassée."""
        today = fields.Date.context_today(self)
        late_loans = self.search([
            ('state', '=', 'ongoing'),
            ('due_date', '<', today),
        ])
        late_loans.write({'state': 'late'})