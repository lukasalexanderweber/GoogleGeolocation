# local imports
from csv_handling import *
from functionality import *


def processInput(gui, csv, sperator, decSeperator, adressColumn, apiKey):
    print "CSV file: " + csv
    print "CSV seperator: " + sperator
    print "Adress column: " + adressColumn
    print "Google Maps API Key: " + apiKey

    frame = gui
    success = 1

    csv = CSV(csv, sperator, adressColumn)
    catch = csv.getAdressesToGeocode()
    if catch == False:
        frame.setMessage("error", "Could not read the csv file using \"genfromtxt\"")

    if len(csv.adresses) == 0:
        success = 0
        frame.setMessage("normal", "All adresses are already geolocated")
    elif csv.rows2skip == 0:
        frame.setMessage("normal", "Processing {0} adresses".format(len(csv.adresses)))
    else:
        frame.setMessage("normal", "Skipped {0} already geolocated adresses.\nProcessing {1} adresses".format(csv.rows2skip-1, len(csv.adresses)))

    counter = 1
    if len(csv.adresses) != 0:          # would be division through 0
        parts = 100/len(csv.adresses)

    for i in range(len(csv.adresses)):
        result = connect_2_service(csv.adresses[i], apiKey)
        
        if result[0] != "REQUEST_DENIED" and result[0] != "OVER_QUERY_LIMIT" and result[0] != "NETWORK_PROBLEM":
            catch = csv.insertResult(csv.rows[i], result, decSeperator)
            if catch == False:
                frame.setMessage("error", "Error while writing into csv. Please close the file if open")
                success = 0
                break
            frame.progress_var.set(counter*parts)
            frame.update()
            counter += 1
            
        elif result[0] == "REQUEST_DENIED":
            success = 0
            frame.setMessage("error", "Your Google Maps API Key seems to be not valid")
            break
        
        elif result[0] == "OVER_QUERY_LIMIT":
            success = 0
            frame.setMessage("normal", "You have reached your daily limit of 2500 requests.\n{0} of {1} adresses are now geocoded.\nPlease come back tomorrow and do not make changes at the csv".format(csv.rows2skip + counter - 1,csv.nRow-1))
            break
        
        elif result[0] == "NETWORK_PROBLEM":
            success = 0
            frame.setMessage("error", "You have an connection error.\n{0} of {1} adresses are now geocoded".format(csv.rows2skip + counter - 1,csv.nRow-1))
            break

    if success == 1:
        frame.progress_var.set(100)
        frame.setMessage("normal", "Your adresses are now geolocated!")

