#########################################################################
#
# Copyright (C) 2012 OpenPlans
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django.conf import settings
from geonode import get_version
from geonode.catalogue import default_catalogue_backend
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse


def resource_urls(request):
    """Global values to pass to templates"""
    site = Site.objects.get_current()
    defaults = dict(
        STATIC_URL=settings.STATIC_URL,  
        CATALOGUE_BASE_URL=default_catalogue_backend()['URL'],
        REGISTRATION_OPEN=settings.REGISTRATION_OPEN,
        VERSION=get_version(),
        SITE_NAME=site.name,
        SITE_DOMAIN=site.domain,
        GROUPS_APP=True if "geonode.contrib.groups" in settings.INSTALLED_APPS else False,
        DEBUG_STATIC=getattr(settings, "DEBUG_STATIC", False),
        PROXY_URL=getattr(settings, 'PROXY_URL', '/proxy/?url='),
        SOCIAL_BUTTONS=getattr(settings, 'SOCIAL_BUTTONS', True),
        USE_DOCUMENTS='geonode.documents' in settings.INSTALLED_APPS,
        HAYSTACK_SEARCH=getattr(settings, 'HAYSTACK_SEARCH', False),
    )
    
    if any(settings.OGC_SERVER):
        from geonode.utils import ogc_server_settings
        defaults.update(dict(
            GEOSERVER_BASE_URL=ogc_server_settings.public_url,
            UPLOADER_URL=reverse('data_upload') if getattr(settings, 'UPLOADER', dict()).get('BACKEND', 'geonode.rest') == 'geonode.importer' else reverse('layer_upload'),
            MF_PRINT_ENABLED=ogc_server_settings.MAPFISH_PRINT_ENABLED,
            PRINTNG_ENABLED=ogc_server_settings.PRINTNG_ENABLED,
            GS_SECURITY_ENABLED=ogc_server_settings.GEONODE_SECURITY_ENABLED,
            GEOGIT_ENABLED=ogc_server_settings.GEOGIT_ENABLED,
            TIME_ENABLED=getattr(settings, 'UPLOADER', dict()).get('OPTIONS', dict()).get('TIME_ENABLED', False),
            ))
    return defaults
