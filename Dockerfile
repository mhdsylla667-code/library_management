FROM odoo:18.0

USER root
COPY addons/library_management /mnt/extra-addons/library_management
USER odoo