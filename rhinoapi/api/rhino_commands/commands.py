import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import System
import json
import rhino3dm
import Newtonsoft.Json

def create_box(width, depth, height):

    breps = {}
    name = 'box1'
    pt0 = rg.Point3d(0.0, 0.0, 0.0)
    pt1 = rg.Point3d(float(width), float(depth),float(height))
    box = rg.BoundingBox(pt0, pt1)
    brep = box.ToBrep()

    breps[name] = Newtonsoft.Json.JsonConvert.SerializeObject(brep)

    return json.dumps(breps)

def move_objects(objs_json, x, y, z, count):
    # desirialize
    objs = desirialize_objects(objs_json, rg.Brep)
    moved_objs = []
    binary = []
    # move objects
    for i in range(int(count)):
        trns = rg.Transform.Translation(float(x)*(i+1),float(y)*(i+1),float(z)*(i+1))
        for obj in objs:
            dup = obj.Duplicate()
            dup.Transform(trns)
            moved_objs.append(dup)
    # serialize
    for obj in moved_objs:
        binary.append(Newtonsoft.Json.JsonConvert.SerializeObject(obj))
    return json.dumps(binary)
    

def desirialize_objects(objs_json, type):
    objs = []
    for obj_js in json.loads(objs_json):
        objs.append(Newtonsoft.Json.JsonConvert.DeserializeObject(obj_js, type))
    return objs


if __name__ == '__main__':
    breps = create_box(100,20,10)
    print(type(breps))
