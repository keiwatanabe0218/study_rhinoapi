import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import System
import json
import rhino3dm
import Newtonsoft.Json
import math

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
    json = []
    # move objects
    for i in range(int(count)):
        trns = rg.Transform.Translation(float(x)*(i+1),float(y)*(i+1),float(z)*(i+1))
        for obj in objs:
            dup = obj.Duplicate()
            dup.Transform(trns)
            moved_objs.append(dup)
    # serialize
    for obj in moved_objs:
        json.append(Newtonsoft.Json.JsonConvert.SerializeObject(obj))
    return json.dumps(json)


def twisted_tower_command(base_curve_json, center_point_json, angle, height):
    """
    ベースのカーブを任意の角度でツイストさせたタワーを10パターン出力
    
    Parameters
    ----------
    base_crv_json: str
        ベースカーブ
    center_point_json: str
        回転中心点
    angle: float
        回転角度
    height: float
        高さ

    Returns
    -------
    loft_json : str
        Twisted TowerのBrep
    """
    # desirialize : stringをjsonに戻してからRhinoオブジェクトに変換
    base_curve = Newtonsoft.Json.JsonConvert.DeserializeObject(json.loads(base_curve_json), rg.Curve)
    center_point = Newtonsoft.Json.JsonConvert.DeserializeObject(json.loads(center_point_json), rg.Point3d)
    # 角度
    rad = math.radians(angle)
    # 回転させるtransform
    print(rad, rg.Vector3d(0.0,0.0,1.0), center_point)
    rotation = rg.Transform.Rotation(rad, rg.Vector3d(0.0,0.0,1.0), center_point)
    # 上に動かすtransform
    move = rg.Transform.Translation(0.0,0.0,height)
    # transformを結合
    trns = rg.Transform.Multiply(rotation, move)
    # 上のカーブを作成
    top_curve = base_curve.Duplicate()
    top_curve.Transform(trns)
    # カーブのリスト
    curvs = System.Collections.Generic.List[rg.Curve]()
    curvs.Add(base_curve)
    curvs.Add(top_curve)
    # ロフト
    loft = rg.Brep.CreateFromLoft(curvs, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal,False)[0]
    # シリアライズして更にstringに変換
    loft_json = json.dumps(Newtonsoft.Json.JsonConvert.SerializeObject(loft))
    return loft_json
    

def desirialize_objects(objs_json, type):
    objs = []
    for obj_js in json.loads(objs_json):
        objs.append(Newtonsoft.Json.JsonConvert.DeserializeObject(obj_js, type))
    return objs


if __name__ == '__main__':
    breps = create_box(100,20,10)
    print(type(breps))
