{
    'name': "Gestion de Bibliothèque",
    'version': '1.0',
    'category': 'Productivity',
    'summary': "Gestion des livres, auteurs, catégories et emprunts",
    'description': """
Module de gestion de bibliothèque d'entreprise
================================================
Permet de gérer :
- les catégories de livres
- les auteurs
- les livres et leur disponibilité
- les emprunts, avec workflow (brouillon / en cours / rendu / en retard)
- un rapport PDF "Fiche de prêt"
""",
    'author': "Mohamed",
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'data/library_sequence.xml',
        'views/library_category_views.xml',
        'views/library_author_views.xml',
        'views/library_book_views.xml',
        'views/library_loan_views.xml',
        'views/library_menus.xml',
        'reports/library_loan_report.xml',
    ],
    'demo': [
        'demo/library_demo.xml',
    ],
    'installable': True,
    'application': True,
}