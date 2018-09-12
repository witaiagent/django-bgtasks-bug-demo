from __future__ import print_function, absolute_import
from background_task import background
import sys
if sys.version_info[0] < 3:
    from urllib2 import URLError, Request, urlopen , HTTPError
    from urllib import urlencode   
else:
    from urllib.error import URLError, HTTPError
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen

import json

def make_http_request(method, target_url, headers={}, get_params={}, post_params={}, default_content_type='application/json'):
    full_path = target_url
    if 'Content-Type' not in headers:
        headers['Content-Type'] = default_content_type    
    http_request = Request(full_path, data=json.dumps(post_params).encode("utf-8"), headers=headers, method=method)
    response = urlopen(http_request).read().decode()    
    return response

@background(schedule=1)
def bulk_api_creator(items):
    resp = make_http_request("POST", "http://127.0.0.1:8000/bulk/", post_params=items)
    print("[TASK]", resp)