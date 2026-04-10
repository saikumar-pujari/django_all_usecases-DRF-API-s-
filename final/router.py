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

    def allow_relation(self, obj1, obj2, **hints):
        # if obj1._meta.app_label == 'n2' and obj2._meta.app_label == 'n2':
        #     return True
        # elif obj1._meta.app_label == 'n2' or obj2._meta.app_label == 'n2':
        #     return False
        # db_list = ('default', 'second_db')
        # if obj1._state.db in db_list and obj2._state.db in db_list:
        #     return True
        return True
