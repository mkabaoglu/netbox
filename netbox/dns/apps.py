from django.apps import AppConfig


class DNSConfig(AppConfig):
    name = "dns"
    verbose_name = "DNS"

#   def ready(self):
#        import dcim.signals
