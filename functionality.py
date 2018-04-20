#!python2
# -*- coding: cp1252 -*-
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
        f.write(adress + ": " + response + "\n")
        f.close()
    except:
        pass

YOUR_API_KEY="AIzaSyC_ANbi6xo4ydjzOWs_EtWYm7R0dFMgHNs" # FOR TESTING ADD YOUR API KEY HERE

def connect_2_service(adress, key = YOUR_API_KEY):
    print adress
    if adress == "":
        log_request(adress, "empty adress")             # log 
        return ["EMPTY ADRESS", [0,0]]                  # and return status + list of zeros

    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+ adress + "&key=" + key)

    if(r.status_code == 200):                           # if connection can be established 
        json_response = r.json()                        # parse JSON response
        status = json_response["status"]                # check https://developers.google.com/maps/documentation/geocoding/intro?hl=de#StatusCodes 

        if(status == "OK"):                             # if results are returned
            j = json_response["results"]                # get the result part

            if len(j) > 1:                              # what do we do with multiple results?
                status = "MULTIPLE_RESULTS"
                #print "multiple options:"
                #for option in j:
                #    print option["formatted_address"]

            location=  j[0]["geometry"]["location"]     # get fist result
            list_lat_lon = [location["lat"],location["lng"]] # store lat and long in list
            print list_lat_lon                          # print and return status + coordinates
            return [status, list_lat_lon]

        if(status == "ZERO_RESULTS"):
            print "no results"
            log_request(adress, "no results")          
            return [status, [0,0]]                     

        if(status == "UNKNOWN_ERROR"):
            print "no results"
            log_request(adress, "unknown error")        
            return [status, [0,0]]                      

        if(status == "INVALID_REQUEST"):
            print "invalid request"
            log_request(adress, "invalid request")     
            return [status, [0,0]]                      

        if(status == "REQUEST_DENIED"):
            print "request denied"
            log_request(adress, "request denied")
            return [status, [0,0]]                      # probably API key error

        if(status == "OVER_QUERY_LIMIT"):
            print "over google map api query limit (not more than 2500 queries a day)"
            log_request(adress, "over query limit")
            return [status, [0,0]]                      # all 2500 requests per day used

    else:
        print "could not establish connection to google-geocoding service - CHECK NETWORK"
        log_request(adress, "status code: " + str(r.status_code))
        return ["NETWORK_PROBLEM", [0,0]]


def geocode_multiple_adresses(adress_list, key = YOUR_API_KEY):
    if len(adress_list) < 2:
        return ["MULTIPLE_ADRESSES_NEEDED, use connect_2_service() for single adress", []]

    latlongList = []
    for adress in adress_list:
        result = connect_2_service(adress, key)
        if result[0] != "REQUEST_DENIED" and result[0] != "OVER_QUERY_LIMIT" and result[0] != "NETWORK_PROBLEM":
            latlongList.append(result)
        elif result[0] == "REQUEST_DENIED":
            return ["REQUEST_DENIED", []]
            break
        elif result[0] == "OVER_QUERY_LIMIT":
            return ["OVER_QUERY_LIMIT", latlongList]
            break
        elif result[0] == "NETWORK_PROBLEM":
            return ["NETWORK_PROBLEM", latlongList]
            break
    return ["OK", latlongList]
    
    

#Test - delete later
test = ""
#print test
#connect_2_service(test)

test2 = ["resedenweg 48 76199 karlsruhe", "schleusenstrasse", "dsfsddfgsadsadasfdsfs"]
#print test2
#print geocode_multiple_adresses(test2)

