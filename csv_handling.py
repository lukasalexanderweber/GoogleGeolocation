#!python2

import numpy as np
from numpy import genfromtxt

class CSV:
    def __init__(self, csv, seperator, adressColumn):
        self.csv = csv
        self.seperator = seperator
        self.adressColumn = adressColumn

        self.nRow = 0
        self.nCol = 0
        self.rows2skip = 0
        
        self.adresses = []
        self.rows = []
        
    def getAdressesToGeocode(self):
        try:
            self.data = genfromtxt(self.csv, delimiter=self.seperator , dtype=None)  # csv to numpy
        except:
            return False
        
        self.nRow = self.data.shape[0]                                           # number of rows
        self.nCol = self.data.shape[1]                                           # number of columns
        colNames = self.data[0,:]                                                # column names

        if "geolocateLAT" not in colNames or "geolocateLONG" not in colNames: # add lat long columns in not exist
            self.data = np.column_stack((self.data, np.repeat("", self.nRow), np.repeat("", self.nRow), np.repeat("", self.nRow)))
            self.data[0, self.nCol] = "geolocateLAT"
            self.data[0, self.nCol+1] = "geolocateLONG"
            self.data[0, self.nCol+2] = "geolocateSTATUS"
            self.nCol += 3

        i, = np.where(self.data[0,:] == self.adressColumn)[0]                    # get index of adress column
        adresses = []
        
        for row in range(self.nRow):
            if self.data[row, self.nCol-1] == "":                                # for rows which wasn't geolocated yet (no status)
                self.adresses.append(self.data[row, i])                          # collect row number and adress   
                self.rows.append(row)

        if self.nRow-1 != len(self.adresses):
            self.rows2skip = self.nRow - len(self.adresses)
        
        return self.adresses

    def insertResult(self, row, result):
        status = result[0]
        lat = result[1][0]
        lon = result[1][1]
        
        self.data[row, self.nCol-3] = str(lat)      # lat
        self.data[row, self.nCol-2] = str(lon)      # long
        self.data[row, self.nCol-1] = status        # status

        try:
            np.savetxt(self.csv, self.data, delimiter=self.seperator, fmt="%s")
        except:
            return False
        return True

##csvP = "C:/Users/Lukas/Desktop/GoogleGeolocation/data/FastFood_sample.csv"
##csv = CSV(csvP, ";", "With brand")
##csv.getAdressesToGeocode()
##csv.insertResult(1,["OK",["123","234"]])
##csv.insertResult(2,["FU",["123","234"]])
##print csv.data
##print csv.rows
###print csv.adresses
