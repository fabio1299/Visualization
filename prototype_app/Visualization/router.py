class gd_admin_db:

    non_app_attribute_tables = ['auth',
                                'admin',
                                'contenttypes',
                                'sessions',
                                'messages',
                                'staticfiles',
                                'migrations',
                                'world']
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.non_app_attribute_tables:
            return 'default'
        return 'argentina'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.non_app_attribute_tables:
            return 'default'
        return 'argentina'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.non_app_attribute_tables or obj1._meta.app_label in self.non_app_attribute_tables:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.non_app_attribute_tables:
            return db=='default'
        return 'argentina'