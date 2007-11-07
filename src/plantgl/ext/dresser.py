#! /usr/bin/env python
# -*- python -*-
#
#       OpenAlea.Fractalysis : OpenAlea fractal analysis library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


"""
:Authors:
  - Da SILVA David
:Organization: Virtual Plants
:Contact: david.da_silva:cirad.fr
:Version: 1.0
:Date: August 2007
:requires:
  - plantgl
  - random
  - math
  - pgl_utils

Module for generating stands of tree according to mesure.

"""

__docformat__ = "restructuredtext en"


import openalea.plantgl.all as pgl
from openalea.plantgl.ext.pgl_utils import sphere, arrow, color, createSwung
from openalea.core import *

houppier_material = pgl.Material("houppier_mat",pgl.Color3(20,100,60))
trunk_material = pgl.Material("trunk_material",pgl.Color3(50,28,6),2)

from math import pi, cos, sin, radians
  
def makeScene( trees, midCr = 0.5, wood=True, random=False):
  #treeList = treesFromFile(file)
  treeList = trees
  scene=pgl.Scene()
  x = [t.x for t in treeList]
  y = [t.y for t in treeList]
  for i in range(len(treeList)):
    t=treeList[i]
    if random:
      h,tr = t.geometry(midCrown = midCr, rdm_x=(min(x),max(x)), rdm_y=(min(y),max(y)))
    else:
      h,tr = t.geometry(midCrown = midCr)
    scene.add(h)
    if(wood):
      scene.add(tr)
  return (scene,)

def viewMesures( file):
  treeList = treesFromFile(file)
  scene = pgl.Scene()
  for i in range(len(treeList)):
    t=treeList[i]
    mes = t.mesures(i)
    for sh in mes:
      scene.add(sh)
  pgl.Viewer.display(scene)


#treeList=makeScene('/home/ddasilva/dev/fractalysis/PlantDB/stands/placette1.csv')
#treeList=makeScene('/home/ddasilva/dev/fractalysis/PlantDB/stands/placette3.csv')
def asymetric_swung( obj , **kwds ):
  X_attr = kwds.get('X', 'X')
  Y_attr = kwds.get('Y', 'Y')
  pos_dist = kwds.get('dist', 'Distance')
  pos_az = kwds.get('az', 'Azimuth')
  circ_attr = kwds.get('circ_attr', 'Circonference')
  height_attr = kwds.get('height_attr', 'Haut')
  botHoup_attr = kwds.get('botHoup', 'BaseHoup')
  radiusHoup_prefix = kwds.get('radiusHoup_prefix', 'r_houp')
  azimuthHoup_prefix = kwds.get('azimuthHoup_prefix', 'a_houp')
  midCrown = kwds.get('midCrown', 0.8)
  wood = kwds.get( 'wood', True )

  rd_kz = [ k for k in obj.__dict__.keys() if radiusHoup_prefix in k]
  rd_kz.sort()
  az_kz = [ k for k in obj.__dict__.keys() if azimuthHoup_prefix in k]
  az_kz.sort()
  assert( len(rd_kz) == len(az_kz) and "directional canopy length and azimuth are not the same size" )

  houppier=[ ( obj.__dict__[rd_kz[i]], houppier2geomAZ(obj.__dict__[az_kz[i]]) ) for i in range( len(rd_kz) ) ]
  houppier.sort(cmp = lambda x,y : cmp(x[1],y[1]))
  
  if not obj.__dict__.has_key("posX") and not obj.__dict__.has_key("posY"):
    try :
      r = obj.__dict__[pos_dist]
      a = obj.__dict__[pos_az]
      obj.posX = r*cos( radians(forest2geomAZ(a)) )
      obj.posY = r*sin( radians(forest2geomAZ(a)) )
    except KeyError: 
      obj.posX = obj.__dict__[X_attr]
      obj.posY = obj.__dict__[Y_attr]

    
  mc = float(midCrown)
  radii = list(houppier)
  ht = 100* (obj.__dict__[height_attr] - obj.__dict__[botHoup_attr])
  h = pgl.Translated( pgl.Vector3(obj.posX, obj.posY, obj.__dict__[botHoup_attr]*100), createSwung(ht*mc,ht,radii) )
  tr = pgl.Translated(pgl.Vector3(obj.posX, obj.posY, 0), pgl.Cylinder( obj.__dict__[circ_attr]/(2*pi), obj.__dict__[botHoup_attr]*100 + ht*0.1) )
  
  s_h = pgl.Shape(h, houppier_material, obj.pid)
  s_tr = pgl.Shape(tr, trunk_material, obj.pid+100000)
  if wood:
    return ( s_h, s_tr )
  else :
    return ( s_h, )

def true_azimuth(az):
  return 90 - ( ( az+200 )%400 )*0.9

def forest2geomAZ(az):
  return -az*0.9

def houppier2geomAZ(az):
  return  - ( ( az+200 )%400 )*0.9

def spheres( obj , **kwds ):
  X_attr = kwds.get('X_attr', 'X')
  Y_attr = kwds.get('Y_attr', 'Y')
  pos_dist = kwds.get('dist', 'Distance')
  pos_az = kwds.get('az', 'Azimuth')
  circ_attr = kwds.get('circ_attr', 'Circonference')
  height_attr = kwds.get('height_attr', 'Haut')
  botHoup_attr = kwds.get('botHoup', 'BaseHoup')
  radiusHoup = kwds.get('radiusHoup', None)
  wood = kwds.get( 'wood', True )

  if not obj.__dict__.has_key("posX") and not obj.__dict__.has_key("posY"):
    try :
      r = obj.__dict__[pos_dist]
      a = obj.__dict__[pos_az]
      obj.posX = r*cos( radians(forest2geomAZ(a)) )
      obj.posY = r*sin( radians(forest2geomAZ(a)) )
    except AttributeError: 
      obj.posX = obj.__dict__[X_attr]
      obj.posY = obj.__dict__[Y_attr]


  ht = 100* (obj.__dict__[height_attr] - obj.__dict__[botHoup_attr])
  if radiusHoup :
    sph_radius = obj.__dict__[radiusHoup]
  else :
    sph_radius = ht/2.
  h = pgl.Translated( pgl.Vector3(obj.posX, obj.posY, obj.__dict__[botHoup_attr]*100 + sph_radius), pgl.Sphere(sph_radius,10,5) )
  tr = pgl.Translated(pgl.Vector3(obj.posX, obj.posY, 0), pgl.Cylinder( obj.__dict__[circ_attr]/(2*pi), obj.__dict__[botHoup_attr]*100 + ht*0.1) )
  
  s_h = pgl.Shape(h, houppier_material, obj.pid)
  s_tr = pgl.Shape(tr, trunk_material, obj.pid+100000)
  if wood:
    return ( s_h, s_tr )
  else :
    return ( s_h, )

def cones( obj , **kwds ):
  X_attr = kwds.get('X_attr', 'X')
  Y_attr = kwds.get('Y_attr', 'Y')
  pos_dist = kwds.get('dist', 'Distance')
  pos_az = kwds.get('az', 'Azimuth')
  circ_attr = kwds.get('circ_attr', 'Circonference')
  height_attr = kwds.get('height_attr', 'Haut')
  botHoup_attr = kwds.get('botHoup', 'BaseHoup')
  radiusHoup = kwds.get('radiusHoup', None)
  wood = kwds.get( 'wood', True )

  if not obj.__dict__.has_key("posX") and not obj.__dict__.has_key("posY"):
    try :
      r = obj.__dict__[pos_dist]
      a = obj.__dict__[pos_az]
      obj.posX = r*cos( radians(forest2geomAZ(a)) )
      obj.posY = r*sin( radians(forest2geomAZ(a)) )
    except AttributeError: 
      obj.posX = obj.__dict__[X_attr]
      obj.posY = obj.__dict__[Y_attr]


  ht = 100* (obj.__dict__[height_attr] - obj.__dict__[botHoup_attr])
  if radiusHoup :
    cone_radius = obj.__dict__[radiusHoup]
  else :
    cone_radius = ht/2.
  h = pgl.Translated( pgl.Vector3(obj.posX, obj.posY, obj.__dict__[botHoup_attr]*100 ), pgl.Cone(cone_radius,ht,1,12) )
  tr = pgl.Translated(pgl.Vector3(obj.posX, obj.posY, 0), pgl.Cylinder( obj.__dict__[circ_attr]/(2*pi), obj.__dict__[botHoup_attr]*100 + ht*0.1) )
  
  s_h = pgl.Shape(h, houppier_material, obj.pid)
  s_tr = pgl.Shape(tr, trunk_material, obj.pid+100000)
  if wood:
    return ( s_h, s_tr )
  else :
    return ( s_h, )


class dresser( Node ):
    """
    Dresser (type) -> func
    Input:
        Type of the function.
    Output:
        function that generates geometry.
    """
    
    geom_func= { "AsymetricSwung" : asymetric_swung,
                  "Sheres" : spheres,
                  "Cones" : cones,
              } 
    
    def __init__(self):
    
        Node.__init__(self)

        funs= self.geom_func.keys()
        funs.sort()
        self.add_input( name = "Type", interface = IEnumStr(funs), value = funs[0]) 
        self.add_output( name = "Geometry function", interface = None)

    def __call__(self, inputs):
        func_name= self.get_input("Type")
        f = self.geom_func[func_name]
        self.set_caption(func_name)

        return f

