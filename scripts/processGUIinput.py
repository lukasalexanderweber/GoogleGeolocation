# local imports
from csvHandling import *
from connect2googlegeo import *


def processInput(gui, csv, sperator, decSeperator, adressColumn, apiKey):
    print "CSV file: " + csv
    print "CSV seperator: " + sperator
    print "Adress column: " + adressColumn
    print "Google Maps API Key: " + apiKey

    frame = gui
    success = 1

    csv = CSV(csv, sperator, adressColumn)      # create object of class CSV
    catch = csv.getAdressesToGeocode()          # will return false if unsucessfull
    
    if catch == False:
        success = 0
        frame.setMessage("error", "Could not read the csv file")
    elif len(csv.adresses) == 0:
        success = 0
        frame.setMessage("normal", "All adresses are already geolocated")
    elif csv.rows2skip == 0:
        frame.setMessage("normal", "Processing {0} adresses".format(len(csv.adresses)))
    else:
        frame.setMessage("normal", "Skipped {0} already geolocated adresses.\nProcessing {1} adresses".format(csv.rows2skip, len(csv.adresses)))


    counter = 0
    numberConnectionError = 0
    
    if len(csv.adresses) != 0:                  # would be division through 0
        parts = float(100)/len(csv.adresses)    # parts are needed for the progress bar

    for i in range(len(csv.adresses)):
        result = connect_2_service(csv.adresses[i], apiKey)
        
        if result[0] != "REQUEST_DENIED" and result[0] != "OVER_QUERY_LIMIT" and result[0] != "NETWORK_PROBLEM":
            numberConnectionError = 0
            csv.insertResult(csv.rows[i], result, decSeperator)
            if counter % 20 == 0:       # after every 20 received results
                catch = csv.saveCSV()
                print "saved results"
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
            csv.saveCSV()
            frame.setMessage("normal", "You have reached your daily limit of 2500 requests.\n{0} of {1} adresses are now geocoded.\nPlease come back tomorrow or insert another key and do not make changes at the csv".format(csv.rows2skip + counter - 1,csv.nRow-1))
            break
        
        elif result[0] == "NETWORK_PROBLEM":
            if numberConnectionError == 0:
                csv.insertResult(csv.rows[i], result, decSeperator)
                numberConnectionError = 1
                continue
            else:
                success = 0
                csv.saveCSV()
                frame.setMessage("error", "You have an connection error.\n{0} of {1} adresses are now geocoded".format(csv.rows2skip + counter,csv.nRow-1))
                break

    if success == 1:
        csv.saveCSV()
        frame.progress_var.set(100)
        frame.setMessage("normal", "Your adresses are now geolocated!")

