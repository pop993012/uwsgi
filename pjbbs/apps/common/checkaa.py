import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def saveCode(key,value,time=0) :
    mc.set(key=key,val=value,time=time)

def getCode(key):
    return mc.get(key)
def delete(key):
    mc.delete(key)
