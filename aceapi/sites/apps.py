from django.apps import AppConfig


class SitesConfig(AppConfig):
    name = 'sites'
    verbose_name = ' Sites, Pages, Shortcodes'

    def ready(self):
        import sites.signals
