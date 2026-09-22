# Module library_management - Odoo

Ce module permet d'administrer le centre de documentation et les prêts de livres au sein d'une entreprise.

## Choix Techniques
1. **Séquence automatique** : Génération des références de prêt au format `LOAN/2026/XXXX` via `ir.sequence`.
2. **Logique Métier** :
   * Date de retour calculée automatiquement à 14 jours via `@api.depends`.
   * Statut `late` déclenché automatiquement si la date d'échéance est dépassée et le livre non rendu.
   * Empêchement des emprunts simultanés d'un même livre via contrainte Python (`@api.constrains`).
3. **Sécurité & Droits d'Accès** :
   * Groupe *Bibliothécaire* : Accès complet (CRUD) à l'ensemble du module.
   * Groupe *Lecteur* : Accès restreint aux emprunts concernant son propre profil (`ir.rule`).
4. **Rapports QWeb** : Impression PDF de la fiche de prêt directement depuis le formulaire d'emprunt._tf_