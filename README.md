# GoogleGeolocation

Python tool to extend a csv file with lat long columns based on an adress column by calling the Google Maps Geolocation API
Open the GUI.py file to start the application. A test dataset (./data) and an API key are given for testing.

![Alt Text](https://github.com/lukasalexanderweber/GoogleGeolocation/blob/master/img/GUI.png)


### Dependencies

Following libraries are needed to run this program

* Tkinter 
	* tkFileDialog
	* ttk
	* tkMessageBox
* csv
* numpy
* requests
* json

### Google Geolocation API

The code for an API call is given in [scripts/connect2googlegeo.py](scripts/connect2googlegeo.py)

The Google Geolocation API allows you to use the use of a search comparable to a Google Maps search request. Google searchs for the most probable result and returns the coordinates which would usually be displayed on Google Maps. The lat and long coordinates can be extracted from the returned json file and if stored in a csv easily be loaded in an GIS. The key given here is just for testing and to get an understanding for the functionality. Please use your own key for bigger geolocalisation projects. 

https://maps.googleapis.com/maps/api/geocode/json?address= YOUR ADRESS &key=AIzaSyC_ANbi6xo4ydjzOWs_EtWYm7R0dFMgHNs

Check the Google Developer Guide for status codes:
https://developers.google.com/maps/documentation/geocoding/intro?hl=de#StatusCodes

Get your very own Geolocation Key:
https://developers.google.com/maps/documentation/geocoding/get-api-key?hl=de

**Note:**
One API is restricted to 2500 requests per day! The Tool will then stop and you can either add another key or wait till the next day and restart the Tool. Already geolocated adresses will be skipped!