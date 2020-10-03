
# -*- coding: utf-8 -*-
import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc
import System
import json
import clr
import urllib
import urllib2

# Rhinoのバージョンを確認
rhino_version = str(Rhino.RhinoApp.Version)[0]
# .Net FrameworkのJsonシリアライザー
if rhino_version == '6':
    clr.AddReference('Newtonsoft.Json')
elif rhino_version == '7':
    clr.AddReference('Newtonsoft.Json.Rhino')
import Newtonsoft.Json


def create_box(x,y,z,width, depth, height):
    pt0 = rg.Point3d(x, y, z)
    pt1 = rg.Point3d(x+float(width), y+float(depth),z+float(height))
    box = rg.BoundingBox(pt0, pt1)
    brep = box.ToBrep()
    return brep
    
objs = []
binary = []
for i in range(5):
    for j in range(5):
        objs.append(create_box(i*10, j*10, 0, 7,5,5))
for obj in objs:
    binary.append(Newtonsoft.Json.JsonConvert.SerializeObject(obj))

mov_x = 0
mov_y = 0
mov_z = 10
mov_count = 5

#url = 'http://127.0.0.1:8000/api/move_objects/move/'
url = 'http://47.74.53.217/api/move_objects/move/'
token = 'Token 25287dd7663f1da9458aeafc055fee67ee80895d'
values = {'title': 'test1',
          'mov_x': mov_x,
          'mov_y': mov_y,
          'mov_z': mov_z,
          'mov_count': mov_count,
          'objects': json.dumps(binary),
          }
headers = {'Authorization': token}

data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
res = response.read()
res_dict = json.loads(res)
title = res_dict['title']
objs_json = json.loads(res_dict['moved_objs'])

objs = []

for obj in objs_json:
    objs.append(Newtonsoft.Json.JsonConvert.DeserializeObject(obj, rg.Brep))

for obj in objs:
    sc.doc.Objects.AddBrep(obj)

sc.doc.Views.Redraw()

