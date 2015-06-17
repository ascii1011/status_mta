
import urllib2
import xml.etree.ElementTree as ET

from .models import FavoriteLine


def get_webpage_content( url ):
    #request page
    req = urllib2.Request( url )
    response = urllib2.urlopen( req )
    the_page = response.read()
    return the_page


class Favorites(object):

    my_key = None
    is_auth = False

    def __init__(self, request):
        self.request = request
        if self.request.user.is_authenticated():
            self.user = self.request.user
            self.is_auth = True
        else:
            self.user = None

    def del_favorite(self, service, name, code, status):
        try:
            FavoriteLine.objects.filter(user=self.user, code=code).delete()
            return True

        except Exception as e:
            return None

    def add_favorite(self, service, name, code, status):
        try:
            if not FavoriteLine.objects.filter(user=self.user, code=code):
                f = FavoriteLine()
                f.user = self.user
                f.service = service
                f.name = name
                f.code = code
                f.status = status
                f.save()

                return True

        except Exception as e:
            return None

    def update_favorite(self, key, status):
        try:
            f = FavoriteLine.objects.get(user=self.user,line=key)
            f.status = status
            f.save()
            return True

        except Exception as e:
            return None


    def get_db(self):
        if self.is_auth:
            try:
                db_favorites = FavoriteLine.objects.filter(user=self.user).values('name', 'code','status', 'service')
                
                return [x for x in db_favorites]
                
            except Exception as e:
                pass
                
        return []

def get_line_code(service, line):
    _service = str( service ).replace(' ','-')
    _line = str( line ).replace(' ','-')
    code = "%s-%s" % ( _service, _line )
    return code 

def clean_content( request, content, service ):
    """
    normalize mta status information
    """
    data = {
        'label': service,
        'status': [],
    }
    
    root = ET.fromstring( content )
    
    data.update( {
        'timestamp': root.find('timestamp').text or 'unknown',
    } )
    
    F = Favorites( request )
    favorite_list = F.get_db()
    favorite_lines = [f['code'] for f in favorite_list]
    
    lines = []
    
    for line in root.find( service ).findall('line'):
        row = {}

        line_name = line.find('name').text or ''
        line_code = get_line_code(service=service, line=line_name)
        row.update( { 
            'name': line_name,
            'code': line_code,
            'status': line.find('status').text or '',
            'text': line.find('text').text or '',
            'Date': line.find('Date').text or '',
            'Time': line.find('Time').text or '', 
        } )
           
        if favorite_lines and line_code in favorite_lines:
            F.update_favorite( line_code, row['status'] )
            row.update( { 'is_favorite': 1 } )
        else:
            row.update( { 'is_favorite': 0 } )

        data['status'].append( row )

    return data

def process_mta_status( request, service ):
    """
    MTA data request function
    """

    url = 'http://mta.info/status/serviceStatus.txt'
    page_content = get_webpage_content( url )
    
    return clean_content( request, page_content, service )

def get_services():
    _tmp = [
        ('bt','BT'),
        ('bus','bus'),
        ('LIRR','LIRR'),
        ('MetroNorth','MetroNorth'),
        ('subway','subway'),
        ]
    return _tmp
