from django.contrib.sitemaps import Sitemap
from rehsponse.models import Rehsponse


class RehsponseSitemap(Sitemap):
    """Sitemap generator for Rehsponse Model"""

    def items(self):
        return Rehsponse.objects.all()
