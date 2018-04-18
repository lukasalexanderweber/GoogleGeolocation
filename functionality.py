#!python2
try:
    import requests
except ImportError:
    print("""You need "requests" !    or run :C:\Python27\Scripts>pip install requests """)


#CALL GOOGLE API

def make_sample_export():
    print "test"

def log_request(adress, response):
    try:
        f = open("api_failure.log", 'a')
        f.write(adress + "," + response)
        f.close()
    except:
        pass

def connect_2_service(adress):
    YOUR_API_KEY=""
    
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+ adress + "&key=" + YOUR_API_KEY)
    print r.status_code
    if(r.status_code == 200):
        json_response = r.json()
        print json_response["status"]
        if(json_response["status"] == "OK"):
            #print json_response["results"]
            j= json_response["results"]
            #Problem wenn Google mehrer Positionen für den Punkt findet wird aktuell nur die erste übergeben
            if(len(j)>0):
                location=  j[0]["geometry"]["location"]
                list_lat_lon = [location["lat"],location["lng"]]
                print list_lat_lon
                return list_lat_lon
            else:
                return [0,0]
        else:
            log_request(adress, json_response["status"])
    else:
        log_request(adress, "status code: "+ r.status_code)
        print "could not establish connection to google-geocoding service - CHECK NETWORK"


#Test - delete later
connect_2_service("Stuttgart")

