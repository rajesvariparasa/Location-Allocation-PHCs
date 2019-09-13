# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 08:47:11 2018

@author: Rajesvari Parasa
"""

import geopandas as gpd
# GeoDataFrame creation
poly = gpd.read_file("GreatBasinCounties.shp")
poly.head()

points = poly.copy()
# change the geometry
points.geometry = points['geometry'].centroid
# same crs
points.crs =poly.crs
points.head()
# save the shapefile
points.to_file('GreatBasinCounties_points.shp')




#%%


import osgeo.ogr as ogr

#opening input polygon file
in_shp = 'E:/Projects/final/Data/test/WARD_BOUNDARY_32644/Wards_32644.shp'
in_driver = ogr.GetDriverByName('ESRI Shapefile')
source = in_driver.Open(in_shp, 0)
in_layer=source.GetLayer()

#creating output file
out_shp=  'E:/Projects/final/Data/test/WARD_BOUNDARY_32644/Wards_32644_centroids.shp'
out_driver=ogr.GetDriverByName('ESRI Shapefile')
source2= out_driver.CreateDataSource(out_shp)
out_layer=source2.CreateLayer('Wards_32644_centroids', in_layer.GetSpatialRef() ,ogr.wkbPoint)


in_layer_defn = in_layer.GetLayerDefn()
n_fields = in_layer_defn.GetFieldCount()
#creating attribute fields for output layer
for i in range(n_fields):
    field_def= in_layer_defn.GetFieldDefn(i)
    out_layer.CreateField(field_def)    
in_layer.ResetReading()

#Creating centroids and attaching polygon attributes
out_feature_defn =out_layer.GetLayerDefn()
feature_in= in_layer.GetNextFeature()
while feature_in:
    print "new feature"
    feature_out=ogr.Feature(out_feature_defn) #creating a feature object with feature definition
    
    for i in range(out_feature_defn.GetFieldCount()):
        feature_out.SetField(out_feature_defn.GetFieldDefn(i).GetNameRef(), feature_in.GetField(i))
        #obtain geometry of polygon to calculate its centroid
    geom= feature_in.GetGeometryRef()
    centroid_p= geom.Centroid()
    feature_out.SetGeometry(centroid_p)
        
        #now that geometry and attr values are set, add the feature to the layer
    out_layer.CreateFeature(feature_out)
    print "feature created"    
    feature_in=in_layer.GetNextFeature()   
        
        
        
source.Destroy()
source2.Destroy()    
    

#%%