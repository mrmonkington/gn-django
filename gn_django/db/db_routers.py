from gn_django.exceptions import ImproperlyConfigured

class AppsRouter:
    """
    A router to route DB operations for one or more django apps to a particular 
    database.

    Requires class attributes to be specified:
      - `APPS` - an iterable of django app labels
      - `DB_NAME` - a string for the DB to route operations to
    """
    APPS = []
    DB_NAME = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        no_apps = not self.APPS
        no_db_specified = not self.DB_NAME
        if no_apps or no_db_specified:
            message = "There was no `APPS` attribute specified for the db router '%s'" % (self.__class__.__name__)
            if no_db_specified:
                message = "There was no `DB_NAME` attribute specified for the db router '%s'" % (self.__class__.__name__)
            raise ImproperlyConfigured(message)


    def db_for_read(self, model, **hints):
        """
        Attempts to read app models route to the named DB.
        """
        if model._meta.app_label in self.APPS:
            return self.DB_NAME
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write app models go to the named DB.
        """
        if model._meta.app_label in self.APPS:
            return self.DB_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in any of the apps this router manages is involved.
        """
        if obj1._meta.app_label in self.APPS and \
           obj2._meta.app_label in self.APPS:
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the apps' DB tables are only created in the named database.
        """
        if app_label in self.APPS:
            return db == self.DB_NAME
        return None

