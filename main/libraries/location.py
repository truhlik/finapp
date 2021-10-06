import logging
import json
import ssl

from django.utils.encoding import smart_str
from urllib.request import urlopen, Request
from urllib.parse import quote_plus
from django.conf import settings


logger = logging.getLogger(__name__)


def get_lat_lng(location):

    # http://djangosnippets.org/snippets/293/
    # http://code.google.com/p/gmaps-samples/source/browse/trunk/geocoder/python/SimpleParser.py?r=2476
    # http://stackoverflow.com/questions/2846321/best-and-simple-way-to-handle-json-in-django
    # http://djangosnippets.org/snippets/2399/

    api_key = settings.GOOGLE_MAPS_API_KEY
    if not api_key:
        logger.warning('GOOGLE MAPS API KEY is not set')
        return None, None

    location = quote_plus(smart_str(location.replace(".", "").replace(" ", "+").replace("\n", "")))
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (location,
                                                                                   api_key)

    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        context = ssl._create_unverified_context()
        response = urlopen(req, context=context).read()
        result = json.loads(response.decode('utf-8'))

        if result['status'] == 'OK':
            lat = str(result['results'][0]['geometry']['location']['lat'])
            lng = str(result['results'][0]['geometry']['location']['lng'])
            return lat, lng
        else:
            return None, None
    except Exception as e:
        logger.error('unable to get location', extra={'location': location, 'error': str(e)})
    return None, None
