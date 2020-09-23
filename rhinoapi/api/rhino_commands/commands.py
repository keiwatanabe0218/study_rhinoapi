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


if __name__ == '__main__':
    breps = create_box(100,20,10)
    print(type(breps))
