import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.shortcuts import render

from .utils import (process_mta_status, get_services, Favorites, get_redis_value)
from cache_handlers import ServiceLines
from .models import FavoriteLine


def JSONHttpResponse(content):
    return HttpResponse(
        json.dumps(content),
        content_type="application/json"
    )


def remove_favorite( request ):
    
    if request.method == "GET":
        service = request.GET.get('service')
        name = request.GET.get('name')
        code = request.GET.get('code')
        status = request.GET.get('status')
        F = Favorites( request )
        if F.del_favorite( service, name, code, status ):
            res = {'result':1}
        else:
            res = {'result':0}

    return JSONHttpResponse(res)


def add_favorite( request ):
    
    if request.method == "GET":
        service = request.GET.get('service')
        name = request.GET.get('name')
        code = request.GET.get('code')
        status = request.GET.get('status')
        F = Favorites( request )
        if F.add_favorite( service, name, code, status ):
            res = {'result':1}
        else:
            res = {'result':0}

    return JSONHttpResponse( res )

def get_favorites( request ):
    """
    1. grabs the request for user's favorites
    2. grabs the users favorites
    3. hooks into Redis and loops through updating the statuses
    4. and returns
    """

    F = Favorites( request )
    tmp_favorites = F.get_db()
    sl = ServiceLines()

    favorites = []
    for f in tmp_favorites:
        f['status'] = sl.get_service_line( f['code'] )['status']
        favorites.append( f )

    res = {
        'favorites': favorites,
    }

    return JSONHttpResponse( res )


def get_service_status( request ):
    if request.method == "GET":
        service = request.GET.get('service')
        
        #update mta details
        res = process_mta_status( request, service )

    else:
        res = {"nothing to see": "move along!"}

    return JSONHttpResponse( res )


@csrf_protect
def home( request ):
    context = { 'services': get_services(), }
    return render( request, "home.html", context )


def about( request ):
    return render( request, "about.html", {} )
