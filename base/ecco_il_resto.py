import requests

base = 'http://127.0.0.1:3010/e1gwis/effis/current_burnt_area'
session = requests.Session()
session.trust_env = False

def dati_ba(id):

    url = base + "?ba_id=" + str(id)
    print url

    try:
        response = session.get(url)
        return response.json()
    except:
        print response.status_code

risposta = dati_ba(2)
print risposta[0]['firedate'], risposta[0]['lastupdate']
