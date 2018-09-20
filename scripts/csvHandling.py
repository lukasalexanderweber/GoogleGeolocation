#!python2

import traceback
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
        
        self.adresses = []      # empty list for adresses to geocode
        self.rows = []          # empty list for the respective row numbers of the adresses
        
    def getAdressesToGeocode(self):
        try:
            self.data = genfromtxt(self.csv, delimiter=self.seperator , dtype=None)  # csv to numpy

            if len(self.data.shape) == 1:                                            # only 1 column -> no multidimensional numpy array
                self.nRow = self.data.shape[0]                                       # number of rows
                self.nCol = 1                                                        # number of columns
                colNames = self.data[0]                                              # column name
            else:                                                                    # more than 1 column -> multidimensional numpy arrays
                self.nRow = self.data.shape[0]                                       # number of rows
                self.nCol = self.data.shape[1]                                       # number of columns
                colNames = self.data[0,:]                                            # column names

            if "geolocateLAT" not in colNames or "geolocateLONG" not in colNames:    # add GEOLOCATE columns if not exist
                self.data = np.column_stack((self.data, np.repeat("", self.nRow), np.repeat("", self.nRow), np.repeat("", self.nRow), np.repeat("", self.nRow)))
                self.data[0, self.nCol] = "geolocateLAT"
                self.data[0, self.nCol+1] = "geolocateLONG"
                self.data[0, self.nCol+2] = "geolocateSTATUS"
                self.data[0, self.nCol+3] = "geolocateADRESS"
                self.nCol += 4 # update new number of columns

            i, = np.where(self.data[0,:] == self.adressColumn)[0]                    # get index of adress column
            
            for row in range(self.nRow):
                if self.data[row, self.nCol-2] == "":                                # for rows which wasn't geolocated yet (no status):
                    self.adresses.append(self.data[row, i])                          # collect adress (i is the adress column)  
                    self.rows.append(row)                                            # collect row number

            if self.nRow-1 != len(self.adresses):                                    # if there are rows which are already geolocated (-1 for the column names)
                self.rows2skip = self.nRow-1 - len(self.adresses)                    # safe the difference to inform the user 

            return True

        except Exception as e:
            traceback.print_exc()
            print str(e)
            return False


    def insertResult(self, row, result, decSep = ","):
        status = result[0]
        lat = str(result[1][0]).replace(".", decSep)
        lon = str(result[1][1]).replace(".", decSep)
        try:
            adress = result[2].encode("iso-8859-1")
            adress = adress.replace(",", "")
            adress = adress.replace(";", "")
        except:
            adress = ""
        
        self.data[row, self.nCol-4] = lat                           # lat
        self.data[row, self.nCol-3] = lon                           # long
        self.data[row, self.nCol-2] = status                        # status
        self.data[row, self.nCol-1] = adress                        # adress

    def saveCSV(self):
        try:
            np.savetxt(self.csv, self.data, delimiter=self.seperator, fmt="%s")
        except:
            return False
        return True


