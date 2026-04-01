class SecondAppRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'n2':
            return 'second_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'n2':
            return 'second_db'
        return None

    def allow_migrate(self, db, app_label, **hints):
        if app_label == 'n2':
            return db == 'second_db'
        return db == 'default'

 
