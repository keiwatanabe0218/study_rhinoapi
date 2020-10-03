# -*- coding: utf-8 -*-
import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc
import System
import json
import clr
import urllib
import urllib2
import rhinoscriptsyntax as rs
import math

# Rhinoのバージョンを確認
rhino_version = str(Rhino.RhinoApp.Version)[0]
# .Net FrameworkのJsonシリアライザー
if rhino_version == '6':
    clr.AddReference('Newtonsoft.Json')
elif rhino_version == '7':
    clr.AddReference('Newtonsoft.Json.Rhino')
import Newtonsoft.Json

def twisted_extrude(crv, pt, ang_st, ang_sd, height):
    """
    ベースのカーブを任意の角度でツイストさせたタワーを10パターン出力
    
    Parameters
    ----------
    crv: Curve
        ベースカーブ
    pt: Point3d
        回転中心点
    ang_st: float
        回転角度１
    ang_ed: float
        回転角度２
    height: float
        高さ

    Returns
    -------
    lofts : list[Brep]
        10パターンのロフトのリスト
    """
    
    lofts = []
    count = 10
    for i in range(count):
        # 角度
        angle = ang_st + (ang_sd-ang_st)/(count-1) * i
        rad = math.radians(angle)
        # 回転させるtransform
        rotation = rg.Transform.Rotation(rad,  rg.Vector3d(0,0,1), pt)
        # 上に動かすtransform
        move = rg.Transform.Translation(0,0,height)
        # transformを結合
        trns = rg.Transform.Multiply(rotation, move)
        # 上のカーブを作成
        crv_tr = crv.Duplicate()
        crv_tr.Transform(trns)
        # ロフト
        loft = rg.Brep.CreateFromLoft([crv, crv_tr], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal,False)[0]
        lofts.append(loft)
    return lofts
    

if __name__ == "__main__":
    # ロフトさせるカーブ
    crv = rs.coercecurve(rs.GetObject(message="select nurbs curve"))
    # 回転させる中心点
    pt = rg.AreaMassProperties.Compute(crv).Centroid
    lofts = twisted_extrude(crv, pt, 10, 100, 100)
    # Rhinoに追加
    for i, loft in enumerate(lofts):
        trns = rg.Transform.Translation(i*75,0,0)
        loft.Transform(trns)
        sc.doc.Objects.AddBrep(loft)
#    print(pt)
#    dp = Newtonsoft.Json.JsonConvert.SerializeObject(crv)
#    ld = Newtonsoft.Json.JsonConvert.DeserializeObject(dp, rg.Curve)
#    print(ld)