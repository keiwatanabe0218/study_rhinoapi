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


pt = rg.Point3d(0,10,3)

pt_dump = Newtonsoft.Json.JsonConvert.SerializeObject(pt)
print(pt_dump)
pt_load = Newtonsoft.Json.JsonConvert.DeserializeObject(pt_dump, rg.Point3d)
print(pt_load)