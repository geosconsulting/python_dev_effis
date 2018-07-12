import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

try:
    conn = psycopg2.connect("dbname='e1gwis' user='e1gwis' host='localhost' password='ka4Zie4i'")
    # print "Connected to the database"
except:
    print "I am unable to connect to the database"
    
cur = conn.cursor()

#"create table nasa_modis_ba.not_calc_cntrs as " +
qry = ("select a.name_en,a.id " +
       "from admin_level_0 a " +
       "where not exists (select 1 " +
 		        	    "from nasa_modis_ba.gwis_stats b " +
 					    "where a.id = b.country_code)"
                        " order by name_en;")

data_frame = pd.read_sql_query(qry, conn) #, index_col='country_code')
# print data_frame

row_iterator = data_frame.iterrows()
# _, last = row_iterator.next()

for i, row in row_iterator:
    # for year_stat in range(2001, 2018):
    # for year_stat in range(2000, 2001):
    for year_stat in range(2018, 2019):
    # for month_stat in range(1, 13):
        # for month_stat in range(1, 13):
        # for month_stat in range(11, 13):
        for month_stat in range(1, 3):
            qry_rotate_insert = "insert into nasa_modis_ba.not_calc_cntrs(country, country_code, year_stats, months_stats, " \
                                                               "number_of_fires,hectares_stats)" \
                                                        "values('{}', {}, {}, {}, {}, {});".format(row['name_en'], row['id'],
                                                                                           year_stat,month_stat,0,0)
            # print qry_rotate_insert
            cur.execute(qry_rotate_insert)
conn.commit()
cur.close()
conn.close()
