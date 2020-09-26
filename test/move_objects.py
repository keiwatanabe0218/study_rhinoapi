import Rhino.Geometry as rg
import System
import json
import clr
clr.AddReference('Newtonsoft.Json')
import Newtonsoft.Json
import scriptcontext as sc

def create_box(x,y,z,width, depth, height):
    pt0 = rg.Point3d(x, y, z)
    pt1 = rg.Point3d(x+float(width), y+float(depth),z+float(height))
    box = rg.BoundingBox(pt0, pt1)
    brep = box.ToBrep()
    return brep

def move_objects(objs, x, y, z, count):
    moved_objs = []
    for i in range(count):
        trns = rg.Transform.Translation(x*(i+1),y*(i+1),z*(i+1))
        for obj in objs:
            dup = obj.Duplicate()
            dup.Transform(trns)
            moved_objs.append(dup)
    return moved_objs
    
if __name__ == '__main__':
    objs = []
    binary = []
    for i in range(5):
        for j in range(5):
            objs.append(create_box(i*10, j*10, 0, 5,5,5))
    
    moved_objs = move_objects(objs, 0,0,10,5)
    
    for obj in moved_objs:
        binary.append(Newtonsoft.Json.JsonConvert.SerializeObject(obj))
        sc.doc.Objects.AddBrep(obj)
    
#    sc.doc.Views.Redraw()
    
    print(json.dumps(binary))