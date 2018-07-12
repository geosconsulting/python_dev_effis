import requests

url = 'http://effis.jrc.ec.europa.eu/rest/2/burntareas/current/'
r = requests.get(url)
print r.status_code
print r.headers['content-type']
print r.encoding
print r.text
print r.json()
