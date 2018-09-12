from django.conf.urls import include, url

from .models import FooModel
import json
from django.http import HttpResponse, Http404
from .tasks import bulk_api_creator

def jsonresp(jsondict):
    return HttpResponse(json.dumps(jsondict, indent=2).encode("UTF-8"))

def insert_one_item(req):
    data = json.loads(req.body.decode("utf-8"))
    item = FooModel(name=data["name"])
    item.save()
    return jsonresp(item._to_dict())

def insert_many_items(req):
    data = json.loads(req.body.decode("utf-8"))
    items = []
    for d in data:
        items.append(FooModel(name=d["name"]))
    FooModel.objects.bulk_create(items)    
    return jsonresp([x._to_dict() for x in items])

def get_all_items(req):
    return jsonresp([x._to_dict() for x in FooModel.objects.all()])

def async_bulk(req):
    data = json.loads(req.body.decode("utf-8"))
    bulk_api_creator(data)
    return jsonresp({"status": "success"})

urlpatterns = [
    url(r'^submit/', insert_one_item, name='submit'),
    url(r'^bulk/', insert_many_items, name='bulk'),
    url(r'^list/', get_all_items, name='list'),
    url(r'^async/', async_bulk, name='async')
]