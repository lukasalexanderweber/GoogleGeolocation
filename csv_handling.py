#!python2

import numpy as np
from numpy import genfromtxt

class CSV:
    def __init__(self, csv, seperator, adressColumn):
        self.csv = csv
        self.seperator = seperator
        self.adressColumn = adressColumn
        
        self.adresses = []
        self.rows = []
        
    def getAdressesToGeocode(self):
        data = genfromtxt(self.csv, delimiter=self.seperator , dtype=None) # csv to numpy
        nRow = data.shape[0]                                    # number of rows
        nCol = data.shape[1]                                    # number of columns
        colNames = data[0,:]                                    # column names

        if "geolocateLAT" not in colNames or "geolocateLONG" not in colNames: # add lat long columns in not exist
            data = np.column_stack((data, np.zeros((nRow)), np.zeros((nRow))))
            data[0, nCol] = "geolocateLAT"
            data[0, nCol+1] = "geolocateLONG"

        i, = np.where(data[0,:] == self.adressColumn)[0]        # get index of adress column
        adresses = []

        for row in range(nRow):
            if data[row, nCol] == "0.0" and data[row, nCol+1] == "0.0": # for rows which doesn't have coordinates yet
                self.adresses.append(data[row, i])                    # collect row number and adress   
                self.rows.append(row)
        return self.adresses

