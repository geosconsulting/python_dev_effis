import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

try:
    conn = psycopg2.connect("dbname='e1gwis' user='postgres' host='localhost' password='antarone'")
    print "Connected to the database"
except:
    print "I am unable to connect to the database"
    
cur = conn.cursor()

# cur.execute("SELECT ba_id,area_ha,(ST_Area(geom)*0.0001)::integer FROM effis.current_burnt_area;")

qry = "select anno::integer , mese::integer, anno ||'-' || mese|| '-' || '15' as data_media, numero_incendi::integer, ettari::double precision " \
      "from nasa_modis_ba.centralamerica_20010101_20011231 " \
      "where paese in ('El Salvador') order by anno,mese;"

cur.execute(qry)

rows = cur.fetchall()

data_frame = pd.DataFrame(rows)
print(data_frame)

data_frame['data_media'] = pd.to_datetime(data_frame[2])
print(data_frame)

# data_frame.plot(x=data_frame[2], y=data_frame[3], xticks=data_frame[2])
# plt.show()

# print "\nPrint the rows by row:\n"
# for row in rows:
#     #print row[0], row[1], row[2]
#     print(row)
# print

frame_data = pd.read_sql_query(qry, conn)

frame_data['data_media'] = pd.to_datetime(frame_data['data_media'].replace(r'\\n', '', regex=True))
print(frame_data)

# frame_data.plot(x=frame_data['data_media'], y=frame_data['count'])
# plt.show()
# print(frame_data[['anno','mese']])

# df['period'] = df[['Year', 'quarter']].apply(lambda x: ''.join(x), axis=1)
# frame_data['data'] = frame_data[['anno', 'mese']].apply(lambda x: ''.join(str(x) for v in frame_data[['anno','mese']]), axis=1)
# print(frame_data)

# frame_data.plot(x='data_media', y='count')
# ax.xticks(frame_data['data_media'])

# plt.xlabel('Date')
# plt.show()

# side = math.sqrt(10000000)
# print "Rett con lato %f da' questi metri quadrati %d" % (side, side*side)

# def connect(user, password, db, host='localhost', port=5432):
#     
#     '''Returns a connection and a metadata object'''
#     # We connect with the help of the PostgreSQL URL
#     url = 'postgresql://{}:{}@{}:{}/{}'    
#     url = url.format(user, password, host, port, db)
#     
# 
#     # The return value of create_engine() is our connection object
#     con = sqlalchemy.create_engine(url, client_encoding='utf8')
# 
#     # We then bind the connection to MetaData()
#     meta = sqlalchemy.MetaData(bind=con, reflect=True)
# 
#     return con, meta
# 
# con, meta = connect('postgres', 'antarone', 'effis')
# 
# print con
#    
# hotspots_df = pd.read_table('hostspots',con)