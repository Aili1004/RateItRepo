#!/usr/bin/env python
#

# Python utility classes and functions.

CACHE_TIME = 60 * 10 	# 5 minutes

def make_memcache_key(req, *args):
  return '_'.join(
    [req.__class__.__module__, req.__class__.__name__] + [str(arg) for arg in args])
    

def is_route_id_valid(route_id):
    #TODO Fix this by querying the route id table.
    return True
    
def is_stop_id_valid(stop_id):
    #TODO Fix this by querying the route id table.
    return True