# Router Classes for managing model mappings to multiple databases
# https://docs.djangoproject.com/en/2.2/topics/db/multi-db/#using-routers

class gd_admin_db:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'wbm_viz':
            return 'default'
        if model.country == 'argentina':
            return 'argentina_01min'
        if model.country == 'peru':
            return 'peru_01min'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'wbm_viz':
            return 'default'
