
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

width = 450.34
depth = 600
height = 800

url = 'http://127.0.0.1:8000/api/objects/box/'
token = 'Token 55902335299b1c34bc240caabe440c57c20b1c41'
values = {'title': 'test3',
          'width': width,
          'depth': depth,
          'height': height}
headers = {'Authorization': token}

data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
res = response.read()
res_dict = json.loads(res)
title = res_dict['title']
objs_json = json.loads(res_dict['objs'])

objs = {}

for key,val in objs_json.items():
    objs[res_dict['title']] = Newtonsoft.Json.JsonConvert.DeserializeObject(val, rg.Brep)

for name,obj in objs.items():
    sc.doc.Objects.AddBrep(obj)

sc.doc.Views.Redraw()

