#!python2

import numpy as np
from numpy import genfromtxt

def getAdressesToGeocode(csv, sperator, adressColumn):
    data = genfromtxt(csv, delimiter=sperator , dtype=None) # csv to numpy
    nRow = data.shape[0]                                    # number of rows
    nCol = data.shape[1]                                    # number of columns
    colNames = data[0,:]                                    # column names

    if "geolocateLAT" not in colNames or "geolocateLONG" not in colNames: # add lat long columns in not exist
        data = np.column_stack((data, np.zeros((nRow)), np.zeros((nRow))))
        data[0, nCol] = "geolocateLAT"
        data[0, nCol+1] = "geolocateLONG"

    i, = np.where(data[0,:] == adressColumn)[0]             # get index of adress column
    adresses = []

    for row in range(nRow):
        if data[row, nCol] == "0.0" and data[row, nCol+1] == "0.0": # for rows which doesn't have coordinates yet
            adresses.append([row, data[row, i]])                    # collect row number and adress   

    return adresses

