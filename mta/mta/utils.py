
import urllib2
import xml.etree.ElementTree as ET

from .models import FavoriteLine


def get_webpage_content( url ):
    
    #request page
    req = urllib2.Request( url )
    response = urllib2.urlopen( req )
    the_page = response.read()
    print 'page len:', str(len(the_page))
    return the_page


"""
def retrieve_favorites(request):
    if request.user.is_authenticated():
        try:
            db_favorites = FavoriteLine.objects.filter(user=request.user).values('line','status')
            return [x for x in db_favorites]
            
        except Exception as e:
            print 'error:', str(e)
            
    return []
"""

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
        print '--deleting favorite!!!:'
        try:
            FavoriteLine.objects.get(user=self.user, code=code).delete()
            return True

        except Exception as e:
            print 'error', str(e)
            return None

    def add_favorite(self, service, name, code, status):
        print '--adding favorite!!:'
        try:
            f = FavoriteLine()
            f.user = self.user
            f.service = service
            f.name = name
            f.code = code
            f.status = status
            f.save()
            return True

        except Exception as e:
            print 'error', str(e)
            return None

    def update_favorite(self, key, status):
        print '--updating favorites'
        try:
            print 'update favorite (%s) with status (%s)' % ( str(key), str(status) )
            f = FavoriteLine.objects.get(user=self.user,line=key)
            f.status = status
            f.save()
            return True

        except Exception as e:
            print 'err', str(e)
            return None


    def get_db(self):
        print '--get_db:'
        if self.is_auth:
            try:
                db_favorites = FavoriteLine.objects.filter(user=self.user).values('name', 'code','status')
                
                print 'fav count:', str(len(db_favorites))
                return [x for x in db_favorites]
                
            except Exception as e:
                print 'error:', str(e)
                
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
    print 'clean_content:'
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
    
    print 'fav_lines:', str(favorite_lines)
    lines = []
    
    for line in root.find( service ).findall('line'):
        row = {}

        line_name = line.find('name').text or ''
        line_code = get_line_code(service=service, line=line_name)
        print '\t-code:', str(line_code)
        row.update( { 
            'name': line_name,
            'code': line_code,
            'status': line.find('status').text or '',
            'text': line.find('text').text or '',
            'Date': line.find('Date').text or '',
            'Time': line.find('Time').text or '', 
        } )
           
        if favorite_lines and line_code in favorite_lines:
            print 'favorite be found!!!, using it!!'
            F.update_favorite( line_code, row['status'] )
            row.update( { 'is_favorite': 1 } )
        else:
            row.update( { 'is_favorite': 0 } )

        data['status'].append( row )
        print 6

    print 7
    print data
    print 8

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
