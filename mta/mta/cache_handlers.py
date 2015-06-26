import redis

class RedisHandler(object):

    def __init__(self):
        self.config()

    def config(self):
        pool = redis.ConnectionPool( host='54.173.229.225', port=6379, db=0 )
        self.r = redis.StrictRedis( connection_pool=pool )

    def get_dict(self, key):
        return self.r.hgetall( key )

    def set_dict(self, key, value):
        return self.r.hmset( key, value )

    def set_list(self, key, value):
        return self.r.lpush( key, value )

    def get_list(self, key):
        return self.r.lrange( key, 0, -1 )

    def del_key(self, key):
        return self.r.delete( key )
    

class ServiceLines( RedisHandler ):
    """
    set_service_line, get_service_line, init_services, push_service
    """
    
    def set_service_line(self, code, service_line={}):
        self.del_key( code )
        self.set_dict( code, service_line )

    def get_service_line(self, code):
        return self.get_dict( code )

    def init_services(self, key="mta-services"):
        self.del_key( key )

    def push_service(self, key="mta-services", name=""):
        self.set_list( key, name )
    
