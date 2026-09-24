FROM odoo:18.0

USER root
COPY addons/ /mnt/extra-addons/
USER odoo