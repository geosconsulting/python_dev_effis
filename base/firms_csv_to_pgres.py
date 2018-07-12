import urllib2
import csv
import pandas as pd
import psycopg2

try:
    conn = psycopg2.connect("dbname='e1gwis' user='postgres' host='localhost' password='antarone'")
    print "Connected to the database"
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

url = "https://firms.modaps.eosdis.nasa.gov/active_fire/c6/text/MODIS_C6_Global_7d.csv"

response = urllib2.urlopen(url)
data = response.read()

# print data

read_firms = csv.DictReader(data)

read_pd = pd.read_csv(url)
print read_pd

read_pd.to_sql(read_pd, con=conn, schema='modis_viirs.modis_7g')

cur.execute("SELECT ba_id,area_ha,(ST_Area(geom)*0.0001)::integer FROM effis.current_burnt_area;")

rows = cur.fetchall()

# print "\nPrint the rows by row:\n"
for row in rows:
    print row[0], row[1], row[2]
