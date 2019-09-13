# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 14:03:57 2018

@author: Rajesvari Parasa
"""
#loop through csv
#    read csv ward no. field=x
#    find x in shapefile ward no field
#    add population of ward csv to shp 
    
#%%

import csv
from osgeo import ogr

# Open a Shapefile, and get field names
shapefilename='E:/Projects/final/Data/test/WARD_BOUNDARY_test/WARD_BOUNDARY_4326_test.shp'
driver= ogr.GetDriverByName('ESRI Shapefile')
source= driver.Open(shapefilename, 1)

layer= source.GetLayer()

feature= layer.GetNextFeature()
#layer_defn = layer.GetLayerDefn()
#field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())]
#print len(field_names),field_names

with open("ward population.csv", 'rb') as csv_obj:
    spamreaderss = csv.reader(csv_obj)  
    for row in spamreaderss:
        i=row[1]
        j=int(row[2])
        print i,j
        print
        print
        
        #feature=layer.GetNextFeature()
        
        while feature:
            print "started"
            print feature.GetField('WARD_NO')
    
            
            if i== feature.GetField('WARD_NO'):
            
                feature.SetField('population', j)
                layer.SetFeature(feature)
                break
            else:
                feature= layer.GetNextFeature()
        layer.ResetReading()
        feature= layer.GetNextFeature()
            
        
source=None

#%%
#Calculating Population per unit area

from osgeo import ogr
shapefile= "E:/Projects/final/Data/test/WARD_BOUNDARY_test/WARD_BOUNDARY_4326_test.shp"
driver=ogr.GetDriverByName('ESRI Shapefile') #call driver
source= driver.Open(shapefile, 1) #using driver to access shapefile
layer= source.GetLayer()
#if source:
#    print "Yes" 
#print source

new_field1 = ogr.FieldDefn('ppl_dens', ogr.OFTReal) #field definition
new_field1.SetWidth(32)
new_field1.SetPrecision(4)
layer.CreateField(new_field1)

feature = layer.GetNextFeature() #initializing feature
while feature:
    i= (feature.GetField('Shape_Area')) 
    j= float(feature.GetField('population'))            #since population is an integer value
    print i,j
    density= j / i #Population/Area
    x=format(density, '.4f')
    feature.SetField('ppl_dens', x)
    print "done"
    layer.SetFeature(feature)
    feature= layer.GetNextFeature()                    #setting reader position to next feature
   
source= None
    
    


#%%






