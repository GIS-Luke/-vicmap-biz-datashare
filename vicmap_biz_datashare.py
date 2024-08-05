'''
Vicmap unzip
'''
##try: 
import os
import zipfile
import glob
from datetime import date
import shutil
import arcpy as ap
# my usual variable block
today_str = str(date.today())
path_Zdir = r'\\cappgis10\d$\ArcGISCatalog\Inputs'
path_Zips = r'\\cappgis10\d$\ArcGISCatalog\SDMZips'
# endswith accepts a tuple and not lists ergo shapefiles=()
shapefiles = ('V_PROPERTY_MP',
              'V_PARCEL_MP',
              'ANNOTATION_TEXT',
              'CAD_AREA_BDY',
              'CENTROID',
              'EASEMENT',
              'PARCEL',
              'PARCEL_PROPERTY',
              'PARCEL_VIEW',
              'PROPERTY',
              'PROPERTY_VIEW',
              'ROAD_CASEMENT',
              'ADDRESS',
              'PLAN_OVERLAY',
              'PLAN_ZONE',
              'SENSITIVITY_PUBLIC',
              'PLAN_EXHIBITED',
              'POWER_LINE',
              'SMES_FULL',
              'PLM25',
              'PPTN_LINES',
              'PPTN_POINTS',
              'PPTN_400M_UNION',
              'STRATEGIC_CYCLING_CORRIDOR',
              'PTV_METRO_BUS_ROUTE',
              'PTV_METRO_BUS_STOP',
              'PTV_METRO_TRAIN_STATION',
              'PTV_METRO_TRAM_ROUTE',
              'PTV_METRO_TRAM_STOP',
              'PTV_REGIONAL_COACH_ROUTE',
              'PTV_REGIONAL_COACH_STOP',
              'PTV_REGIONAL_TRAIN_STATION',
              'PTV_SKYBUS_ROUTE',
              'PTV_TRAIN_CARPARK',
              'PTV_TRAIN_CORRIDOR_CENTRELINE',
              'PTV_TRAIN_STATION_BIKE_STORAGE',
              'PTV_TRAIN_STATION_PLATFORM',
              'PTV_TRAIN_TRACK_CENTRELINE',
              'PTV_TRAM_TRACK_CENTRELINE',
              'BUILDING_POLYGON',
              'FOI_INDEX_CENTROID',
              'FOI_INDEX_EXTENT',
              'FOI_LINE',
              'FOI_POINT',
              'FOI_POLYGON',
              'GNR',
              'LOCALITY_POINT',
              'PL_PLACE_AREA_POLYGON',
              'TR_ROAD',
              'LOCALITY_POLYGON',
              'LGA_POLYGON',
              'POSTCODE_POLYGON',
              'PARISH_POLYGON',
              'TOWNSHIP_POLYGON',
              'AD_LGA_AREA_POLYGON')
os.chdir(path_Zdir)
z_files = glob.glob('*.zip')
for z_file in z_files:
    with zipfile.ZipFile(z_file) as zip_obj:
        info_list = zip_obj.infolist()
        for z_info in info_list:
            z_base = os.path.splitext(z_info.filename)[0]
            if z_base.endswith(shapefiles):
                z_info.filename = os.path.basename(z_info.filename)
                zip_obj.extract(z_info)
    # we need to split the file name to insert today_str
    z_base, z_ext = os.path.splitext(z_file)
    out_z_file = '{}_{}{}'.format(z_base, today_str, z_ext)
    dest_z_file = os.path.join(path_Zips, out_z_file)
    # move the zip file to it's backup dir because "just in case"
    os.rename(z_file, dest_z_file)
# now we only have to deal with a dir of shapefiles
# we have to copy ADDRESS.shp POZI tool dir
path_POZI_ADD = r'\\cappgis10\d$\PoziConnect\Vicmap\VMADD'
path_POZI_PROP = r'\\cappgis10\d$\PoziConnect\Vicmap\VMPROP'
# and v_property_mp is needed by history
history_dir = r'\\cappgis10\d$\ArcGISCatalog\PYs\weekly\property_history'
# Check if POZI really needs parcel_property.dbf
[shutil.copy(f, path_POZI_PROP) for f in os.listdir() if
 f == 'PARCEL_PROPERTY.dbf']
ap.env.overwriteOutput=True
ap.env.workspace = path_Zdir
for shp in ap.ListFeatureClasses('*'):
    if shp == 'ADDRESS.shp':
        out_shp = os.path.join(path_POZI_ADD, shp)
        ap.Copy_management(shp, out_shp)
    elif shp == 'V_PROPERTY_MP.shp':
        out_shp = os.path.join(history_dir, shp)
        ap.Copy_management(shp, out_shp)
        # POZI has been updated so don't need to slice "V_"
        out_shp = os.path.join(path_POZI_PROP, shp)
        ap.Copy_management(shp, out_shp)
        # We have to delete the property_simplified shapefiles here
        # since there is no other script to cleanup these files
        ap.Delete_management(shp)
    elif shp == 'V_PARCEL_MP.shp':
        # POZI has been updated so don't need to slice "V_"
        out_shp = os.path.join(path_POZI_PROP, shp)
        ap.Copy_management(shp, out_shp)
        # We have to delete the property_simplified shapefiles here
        # since there is no other script to cleanup these files
        ap.Delete_management(shp)
    else:
        pass # This pass is okay since we don't work with other list members.
