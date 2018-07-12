from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import pandas as pd
from datetime import date

api = SentinelAPI('fabiolana', 'Albertone_2016')
footprint = geojson_to_wkt(read_geojson('/media/sf_Downloads/__effis/ricerca.geojson'))

products = api.query(footprint,
                     # date=('20170801', date(2017, 12, 15)),
                     date=('20151001', '20171205'),
                     platformname='Sentinel-2',
                     # producttype='SLC')
                     #,orbitdirection='ASCENDING') #,
                     cloudcoverpercentage=(0, 10))


# download all results from the search
# api.download_all(products)

# GeoJSON FeatureCollection containing footprints and metadata of the scenes
api.to_geojson(products)

# inserito in dataframe
df_prods = pd.DataFrame(api.to_geojson(products))
# print df_prods

# GeoPandas GeoDataFrame with the metadata of the scenes and the footprints as geometries
print api.to_geodataframe(products)

# Get basic information about the product: its title, file size, MD5 sum, date, footprint and
# its download url
# api.get_product_odata(<product_id>)

# Get the product's full metadata available on the server
# api.get_product_odata(<product_id>, full=True)