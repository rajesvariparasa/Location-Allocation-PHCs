# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 07:53:25 2018

@author: Rajesvari Parasa
"""

#importing libraries
from osgeo import ogr, gdal
from shapely.geometry import Polygon, Point, MultiPolygon
from osgeo import osr
#Reading input shapefiles

shapefile1= 'E:/Projects/final/Data/test2/GVMC_HealthCentres_32644/GVMC_HCs_32644.shp'
shapefile2= 'E:/Projects/final/Data/test2/Voronoi/Voronoi_clip.shp'
shapefile3= 'E:/Projects/final/Data/test2/WARD_BOUNDARY_32644/Wards_32644.shp'

driver1= ogr.GetDriverByName('ESRI Shapefile')
driver2= ogr.GetDriverByName('ESRI Shapefile')
driver3= ogr.GetDriverByName('ESRI Shapefile')

source1 = driver1.Open(shapefile1, 0)
source2 = driver2.Open(shapefile2, 0)
source3 = driver3.Open (shapefile3, 0)

layer1 = source1.GetLayer()
voronoi_layer = source2.GetLayer()
wards = source3.GetLayer()
#%%

#create new attribute - demand field for PHCs and voronoi polygons
new_field1 = ogr.FieldDefn('demand', ogr.OFTReal)
new_field1.SetWidth(32)
new_field1.SetPrecision(2)

layer1.CreateField(new_field1)
layer2.CreateField(new_field1)

#%%

#Method to calculate area of intersection

def area_of_intersec(intersection_collection):
    count = intersection_collection.GetGeometryCount()
    area=0.0
    for i in range(count):
        
        geometry= intersection_collection.GetGeometryRef(i)
        area = area + geometry.GetArea()
    return area
    

for voronoi in voronoi_layer:

    geometry_f2 = voronoi.GetGeometryRef()
    geomname= geometry_f2.GetGeometryName()
    print geomname
    voronoi_no = voronoi.GetField('ID')
    print "Voronoi Polygon Number", voronoi_no

    demand=0
    feature3 = wards.GetNextFeature()
    while feature3 :
        geometry_f3 = feature3.GetGeometryRef()
        attribute_f3 = feature3.GetField('WARD_NO')
        
        if geometry_f3.Intersects(geometry_f2):
            print "Ward Number", attribute_f3
            
            #Obtainig parameters to calculate demand
            area_ward= feature3.GetField('Shape_Area')
            ppl_density = feature3.GetField('ppl_dens')            
            region_intersec= geometry_f3.Intersection(geometry_f2)            
            area = area_of_intersec(region_intersec)     
            print area           
            demand = demand + (ppl_density * area)                    #can also be seen as what 'fraction' of people of the corresponding ward are present in the intersecting part
              
        feature3 = wards.GetNextFeature()
    wards.ResetReading()  
    
    phc_point = layer1.GetNextFeature() 
    while phc_point:
        
        phc_id = phc_point.GetField('ID')
        if str(voronoi_no)== str(phc_id):
            print "demand", demand
            phc_point.SetField('demand', round(demand,0))
            layer1.SetFeature(phc_point)
        phc_point = layer1.GetNextFeature() 
    layer1.ResetReading()   
#   
    #writing demand to voronoi polygon as well
    voronoi.SetField('demand', round(demand,0))
    voronoi_layer.SetFeature(voronoi)


source1.Destroy()
source2.Destroy()
source3.Destroy()        
        



#%%
import osgeo
import osgeo.ogr
try:
    shapefile = osgeo.ogr.Open("E:/Projects/final/Data/test/Voronoi/voronoi_v1_clippedto_wards.shp")

    if shapefile: # checks to see if shapefile was successfully defined
        numLayers = shapefile.GetLayerCount()
    else: # if it's not successfully defined
        print "Couldn't load shapefile"
except: # Seems redundant, but if an exception is raised in the Open() call,
    #   # you get a message
    print "Exception raised during shapefile loading"

    # if you want to see the full stacktrace - like you are currently getting,
    # then you can add the following:
    raise
    
#    #%%
#    
#def change_projection(ring):   
#    from osgeo import ogr
#    from osgeo import osr
#    
#    source = osr.SpatialReference()
#    source.ImportFromEPSG(4326)
#    
#    target = osr.SpatialReference()
#    target.ImportFromEPSG(32644)
#    
#    transform = osr.CoordinateTransformation(source, target)
#    ring2 = ogr.Geometry(ogr.wkbLinearRing)
#    
#    number=ring.GetPointCount()
#    for a in range(number):
##        point = ogr.CreateGeometryFromWkt(a)
##        print point
#        b=a
#
#        print b
#        b.Transform(transform)
#        print b
#        ring2.AddPoint(b)
#    
#    #Create polygon
#    poly= ogr.Geometry(ogr.wkbPolygon)  
#    poly.AddGeometry(ring2)
#    return poly
##.ExportToWkt()

#%%
source = osr.SpatialReference()
source.ImportFromEPSG(4326)

target = osr.SpatialReference()
target.ImportFromEPSG(32644)

transform = osr.CoordinateTransformation(source, target)
ring2 = ogr.Geometry(ogr.wkbLinearRing)
number=ring_intersection.GetPointCount()
print number
print
print
for a in range(number):
    point = ring_intersection.GetPoint(a) #point read as tuple
    
    #to avoid 3rd coordinate
    X = point[0]
    Y= point[1]
    point_ = (X,Y)
    print point_
    create_point = ogr.Geometry(ogr.wkbPoint)
    create_point.AddPoint(X,Y)
    
    print create_point
    create_point.Transform(transform)
    print create_point
    
    
    
    X1 = create_point.GetX()
    Y1 = create_point.GetY()
    ring2.AddPoint(X1,Y1)
poly= ogr.Geometry(ogr.wkbPolygon)  
poly.AddGeometry(ring2)    
#%%


point= layer1.GetNextFeature()
while point:
    
    z= layer1
    z.SetSpatialFilter(point)
    for feature in z:
        x, y = feature.GetX(), feature.GetY()
        print x,y

    point= layer1.GetNextFeature()







#%%

sum_reported= 0
total_demand=0
phc=layer1.GetNextFeature()
while phc:
    #pop_rep= phc.GetField('Data Repor')
    demand_individual=phc.GetField('demand')
    #sum_reported = sum_reported + pop_rep
    total_demand=total_demand+demand_individual
    phc=layer1.GetNextFeature()
#    
#print "Sum of 'population served' reported at all facilities",sum_reported
print "Population served by all phcs", total_demand

#%%


sum_wardspopulation = 0
ward= layer3.GetNextFeature()
while ward:
    ward_pop= ward.GetField('population')
    sum_wardspopulation= sum_wardspopulation+ ward_pop
    ward= layer3.GetNextFeature()
print "Sum of population in all wards",    sum_wardspopulation

#%%
