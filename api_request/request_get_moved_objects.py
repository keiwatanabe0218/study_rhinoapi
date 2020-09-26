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

title = 'test1'
url = 'http://127.0.0.1:8000/api/move_objects/get/?'
token = 'Token 55902335299b1c34bc240caabe440c57c20b1c41'
values = {'title': title}
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

