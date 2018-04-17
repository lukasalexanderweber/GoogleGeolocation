#!python2
from functionality import *
from Tkinter import *
from tkFileDialog import askopenfilename
import csv

#######################################
# FUNCTIONALITY
def callAPI(csv, sperator, adressColumn, apiKey):
    print "CSV file: " + csv
    print "CSV seperator: " + sperator
    print "Adress column: " + adressColumn
    print "Google Maps API Key: " + apiKey
    

#######################################
# LAYOUT
class Application(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
    def openFile(self):
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        self.csv.set(filename)       # the StringVar is set, Entry updated

    def getCsvColumns(self):
        self.filename = self.csv.get()                          # get filename from user input
        self.seperator = self.csv_seperator.get()               # get seperator from user input
        if self.filename == "" or self.seperator == "":         # check if both are filled
            self.message.set("Please enter filename and seperator first")
        else:
            try:          
                adressCSV = open(self.filename)                 # open csv
                self.columnNames = []                           # to store column names
                for row in csv.reader(adressCSV):               # iterate through rows
                    self.columnNames = row[0].split(self.seperator)# split at the given seperator
                    break                                       # only first row needed for names

                counter = 1
                self.IntVars = []                               # list to save all IntVars of the checkboxes
                for c in self.columnNames:                      # for all columns
                    var = IntVar()                              # create new IntVar (information if box is checked)
                    self.IntVars.append(var)                    # appen to IntVar list
                    Checkbutton(self, text=c, variable=var).grid(row=6+counter, column= 1, sticky=W) # add new checkbutton
                    counter += 1

                self.updateRows(len(self.columnNames))          # move other items (API key, Go-Button, Error-messages to bottom)
                self.message.set("")
            except:
                self.message.set("Error while processing CSV")

    def updateRows(self, numberColumnsCSV): 
        self.apiKeyLabel.grid(column=1, row=7+numberColumnsCSV, sticky=W) 
        self.apiKey.grid(column=1, row=8+numberColumnsCSV, sticky=(W,E)) 
        self.go.grid(column=1, row=9+numberColumnsCSV, sticky=W) 
        self.error.grid(column=1, row=10+numberColumnsCSV, sticky=(W, E))
        self.pack()

    def getCheckedCheckboxes(self):
        counter = 0
        checkedCheckboxes = []                                  # to store names of checked columns
        for box in self.IntVars:                                # for all checkboxes
            if box.get() == 1:                                  # get info if box is checked (1)
                checkedCheckboxes.append(self.columnNames[counter])# if its checked add name to list
            counter += 1
               
        if len(checkedCheckboxes) < 1:                          
            self.message.set("Please select adress column first")
            return False
        elif len(checkedCheckboxes) > 1:
            self.message.set("Only one column can be selected")
            return False
        else:                                                   # proceed if only one box is checked
            self.message.set("")
            self.adressColumn = checkedCheckboxes[0]
            return True

    def startAPIcall(self):
        checked = self.getCheckedCheckboxes()                   # check if box is checked correctly
        if checked == True:
            if self.apiKey.get() != "":                         # check if API Key entry is filled
                callAPI(self.filename, self.seperator, self.adressColumn, self.apiKey.get()) # call functionality part
                self.message.set("")
            else:
                self.message.set("Please insert your API Key")
        
    def createWidgets(self):
        # http://www.tkdocs.com/tutorial/firstexample.html#design
        mainframe = self
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        self.csv = StringVar()       # to store filepath
        self.message = StringVar()   # to store eventual error messages 

        # "open csv" part
        csvLabel =Label(mainframe, text="Open CSV with the adresses")       
        self.csv_file = Entry(mainframe, width=15, textvariable=self.csv)
        openFileB = Button(mainframe, text="Open", command=self.openFile)
        # "csv seperator" part
        seperatorLabel = Label(mainframe, text="CSV seperator")
        self.csv_seperator = Entry(mainframe, width=2)
        # "load csv columns" part
        loadColumnsB = Button(mainframe, text="Load CSV columns", command=self.getCsvColumns)
        self.listbox = Listbox(mainframe)
        # "Google maps API" part
        self.apiKeyLabel = Label(mainframe, text="Please enter your Google Maps API Key")
        self.apiKey = Entry(mainframe, width=15)
        # "GO! button" part
        self.go = Button(mainframe, text="Go!", command=self.startAPIcall)
        # "error/warning message part
        self.error = Label(mainframe, fg="red", textvariable=self.message)


        # Layout
        csvLabel.grid(column=1, row=1, sticky=W)
        self.csv_file.grid(column=1, row=2, sticky=(W, E))
        openFileB.grid(column=3, row=2, sticky=W)
        seperatorLabel.grid(column=1, row=3, sticky=W)
        self.csv_seperator.grid(column=1, row=4, sticky=(W))
        loadColumnsB.grid(column=1, row=6, sticky=W)
        self.apiKeyLabel.grid(column=1, row=7, sticky=W) 
        self.apiKey.grid(column=1, row=8, sticky=(W,E)) 
        self.go.grid(column=1, row=9, sticky=W) 
        self.error.grid(column=1, row=10, sticky=(W, E))


make_sample_export()

root = Tk()
root.title("Google Geolocation")
app = Application(master=root)
app.mainloop()
root.destroy()

