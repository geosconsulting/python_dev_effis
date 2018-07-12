#!/usr/bin/env python
#
# Created on 9/27/2012 Pat Cappelaere - Vightel Corporation
#
# Requirements:
#	gdal, numpy pytrmm...
#
# Access and Process MODIS Active Fires
#
# https://firms.modaps.eosdis.nasa.gov/active_fire/text/Central_America_7d.csv
# http://firms.modaps.eosdis.nasa.gov/active_fire/text/Central_America_48h.csv
# http://firms.modaps.eosdis.nasa.gov/active_fire/text/Central_America_24h.csv
#

import numpy, sys, os, inspect, io, glob, shutil
import urllib
import csv
import json
import ssl

import datetime
from datetime import date, timedelta
from dateutil.parser import parse

import browseimage
from browseimage import mapbox_image

# Site configuration
import config
import argparse
from s3 import CopyToS3

# 24hr fires
active_fires_urls = {
    "d02": "https://firms.modaps.eosdis.nasa.gov/active_fire/text/Central_America_24h.csv",
    "d03": "https://firms.modaps.eosdis.nasa.gov/active_fire/text/Central_America_24h.csv",
    "d09": "https://firms.modaps.eosdis.nasa.gov/active_fire/text/South_America_24h.csv",
    "d10": "https://firms.modaps.eosdis.nasa.gov/active_fire/text/South_America_24h.csv",
    "d04": "https://firms.modaps.eosdis.nasa.gov/active_fire/text/Southern_Africa_24h.csv",
    "d07": "https://firms.modaps.eosdis.nasa.gov/active_fire/text/South_Asia_24h.csv",
    "d08": "https://firms.modaps.eosdis.nasa.gov/active_fire/text/South_Asia_24h.csv"
}


def execute(cmd):
    if verbose:
        print cmd
    os.system(cmd)


def inbbox(bbox, lat, lon):
    if (lon >= bbox[0]) and (lon <= bbox[2]) and (lat >= bbox[1]) and (lat <= bbox[3]):
        return 1
    return 0


def csv_to_geojson(csv_filename, geojson_filename, bbox):
    f = open(csv_filename, 'r')
    reader = csv.DictReader(f, fieldnames=('latitude', 'longitude', 'brightness', 'scan', 'track', 'acq_date',
                                           'acq_time', 'satellite', 'confidence', 'version', 'bright_t31', 'frp'))

    features = []
    index = 0

    for row in reader:
        # skip first row
        if index > 0:
            dt = row['acq_time']
            sat = row['satellite']
            if sat == 'T':
                sat = 'Terra'
            if sat == 'A':
                sat = 'Aqua'
            properties = {
                'brightness': row['brightness'],
                'acq_date': row['acq_date'] + "T" + dt[1:3] + ":" + dt[3:] + "Z",
                'satellite': sat,
                'confidence': row['confidence']
            }
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])
            coordinates = [longitude, latitude]

            if inbbox(bbox, latitude, longitude):
                feature = {"type": "Feature", "geometry": {"type": "Point", "coordinates": coordinates},
                           "properties": properties}
                features.append(feature)

        index += 1

    geojson = {"type": "FeatureCollection", "features": features}
    # print "features found:", len(features)

    with io.open(geojson_filename, 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(geojson, ensure_ascii=False)))

    if verbose:
        print "Done:", geojson_filename


def process_url(mydir, url, ymd, bbox, zoom, s3_bucket, s3_folder):
    csv_filename = os.path.join(os.path.join(mydir, "modis_af." + ymd + '.csv'))
    geojson_filename = os.path.join(os.path.join(mydir, "modis_af." + ymd + '.geojson'))
    geojsongz_filename = os.path.join(os.path.join(mydir, "modis_af." + ymd + '.geojson.gz'))
    tif_filename = os.path.join(os.path.join(mydir, "modis_af." + ymd + '.tif'))
    osm_bg_image = os.path.join(os.path.join(mydir, "osm_bg_image.tif"))
    thn_image = os.path.join(os.path.join(mydir, "modis_af." + ymd + '_thn.jpg'))

    if verbose:
        print "sys version", sys.version_info[0], sys.version_info[1], sys.version_info[2]

    if (sys.version_info[0] == 2) and (sys.version_info[1] >= 7) and (sys.version_info[2] > 9):
        context = ssl._create_unverified_context()
    else:
        context = None

    if force or not os.path.exists(csv_filename):
        if verbose:
            print "retrieve", url, csv_filename

        if context:
            urllib.urlretrieve(url, csv_filename, context=context)
        else:
            urllib.urlretrieve(url, csv_filename)

    if force or not os.path.exists(geojson_filename):
        csv_to_geojson(csv_filename, geojson_filename, bbox)

    if force or not os.path.exists(geojsongz_filename):
        cmd = 'gzip -f < %s > %s' % (geojson_filename, geojsongz_filename)
        execute(cmd)

    # url = "https://firms.modaps.eosdis.nasa.gov/wms/?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=fires24&width=400&height=250&BBOX=54,5.5,102,40"

    # if force or not os.path.exists(tif_filename):
    #	urllib.urlretrieve(url, tif_filename)
    #	print "retrieved ", tif_filename

    centerlat = (bbox[1] + bbox[3]) / 2
    centerlon = (bbox[0] + bbox[2]) / 2
    rasterXSize = 400
    rasterYSize = 250

    mapbox_image(centerlat, centerlon, zoom, rasterXSize, rasterYSize, osm_bg_image)

    ullon, ullat, lrlon, lrlat = browseimage.Gen_bbox(centerlat, centerlon, zoom, rasterXSize, rasterYSize)
    # print ullon, lrlat, lrlon, ullat

    url = "https://firms.modaps.eosdis.nasa.gov/wms/?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=fires24&width=400&height=250&BBOX="
    url += str(ullon) + "," + str(lrlat) + "," + str(lrlon) + "," + str(ullat)

    if force or not os.path.exists(tif_filename):
        if verbose:
            print "retrieve", tif_filename

        if context:
            urllib.urlretrieve(url, tif_filename, context=context)
        else:
            urllib.urlretrieve(url, tif_filename)
    # print "retrieved ", tif_filename

    # superimpose the suface water over map background
    if force or not os.path.isfile(thn_image):
        cmd = str.format("composite -quiet -gravity center {0} {1} {2}", tif_filename, osm_bg_image, thn_image)
        execute(cmd)

    file_list = [tif_filename, geojson_filename, geojsongz_filename, thn_image]
    CopyToS3(s3_bucket, s3_folder, file_list, force, verbose)


def cleanupdir(mydir):
    if verbose:
        print "cleaning up", mydir

    today = datetime.date.today()
    delta = timedelta(days=config.DAYS_KEEP)
    dl = today - delta
    lst = glob.glob(mydir + '/[0-9]*')

    for l in lst:
        basename = os.path.basename(l)
        if len(basename) == 8:
            year = int(basename[0:4])
            month = int(basename[4:6])
            day = int(basename[6:8])
            dt = datetime.date(year, month, day)

            if dt < dl:
                msg = "** delete " + l
                if verbose:
                    print msg
                shutil.rmtree(l)


def cleanup():
    _dir = os.path.join(config.data_dir, "modis_af")
    cleanupdir(_dir)


#
# ======================================================================
#
# python modis-active-fires.py --region d02 --date 2015-10-13
#
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MODIS Processing')
    apg_input = parser.add_argument_group('Input')
    apg_input.add_argument("-f", "--force", action='store_true', help="forces new product to be generated")
    apg_input.add_argument("-v", "--verbose", action='store_true', help="Verbose Flag")
    apg_input.add_argument("-r", "--region", help="Region")
    apg_input.add_argument("-d", "--date", help="date")

    options = parser.parse_args()
    force = options.force
    verbose = options.verbose
    regionName = options.region
    region = config.regions[regionName]
    assert (region)

    todaystr = date.today().strftime("%Y-%m-%d")
    options = parser.parse_args()

    dt = options.date or todaystr
    today = parse(dt)

    year = today.year
    month = today.month
    day = today.day
    doy = today.strftime('%j')

    ymd = "%d%02d%02d" % (year, month, day)

    mydir = os.path.join(config.MODIS_ACTIVE_FIRES_DIR, ymd, regionName)
    if not os.path.exists(mydir):
        os.makedirs(mydir)

    # get last 24 hrs
    # url_7day 	= "https://firms.modaps.eosdis.nasa.gov/active_fire/text/Central_America_7d.csv"
    url_24hr = active_fires_urls[regionName]
    assert (url_24hr)

    s3_folder = os.path.join("modis_af", str(year), doy)
    s3_bucket = region['bucket']
    bbox = region['bbox']
    zoom = region['thn_zoom']

    process_url(mydir, url_24hr, ymd, bbox, zoom, s3_bucket, s3_folder)
    cleanup()