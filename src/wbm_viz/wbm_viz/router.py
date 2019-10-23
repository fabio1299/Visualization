# Router Classes for managing model mappings to multiple databases
# https://docs.djangoproject.com/en/2.2/topics/db/multi-db/#using-routers

class gd_admin_db:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'wbm_viz':
            return 'default'
        if model._meta.app_label == 'hydrostn':
            return 'argentina_01min'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'wbm_viz':
            return 'default'
        if model._meta.app_label == 'hydrostn':
            return 'argentina_01min'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        db_list = ('default', 'argentina_01min')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, **hints):
        if app_label == 'wbm_viz':
            return db == 'default'
        if app_label == 'hydrostn':
            return db == 'argentina_01min'
        return None
