#!python2

# local imports
from csv_handling import *
from functionality import *

# lib imports
from Tkinter import *
from tkFileDialog import askopenfilename
import tkMessageBox
import csv

#######################################
# FUNCTIONALITY
def processInput(csv, sperator, adressColumn, apiKey):
    print "CSV file: " + csv
    print "CSV seperator: " + sperator
    print "Adress column: " + adressColumn
    print "Google Maps API Key: " + apiKey

    csv = CSV(csv, sperator, adressColumn)
    csv.getAdressesToGeocode()
    geocode_multiple_adresses(csv.adresses)

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
                    Checkbutton(self, text=c, variable=var, background=self.backgr, foreground=self.foregr, selectcolor=self.button).grid(row=6+counter, column= 1, sticky=W, padx=(self.padLeft-5, 0)) # add new checkbutton
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
        try:
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
        except:
            return False

    def startInputProcessing(self):
        self.message.set("")
        checked = self.getCheckedCheckboxes()                   # check if box is checked correctly
        if checked == True:
            if self.apiKey.get() != "":                         # check if API Key entry is filled
                processInput(self.filename, self.seperator, self.adressColumn, self.apiKey.get()) # call functionality part
                self.message.set("")
            else:
                self.message.set("Please insert your API Key")
        else:
            self.message.set("Please select adress column first")
        
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
        self.csv_file = Entry(mainframe, width=60, textvariable=self.csv)
        openFileB = Button(mainframe, text="Open", command=self.openFile)
        # "csv seperator" part
        seperatorLabel = Label(mainframe, text="CSV seperator")
        self.csv_seperator = Entry(mainframe, width=2)
        # "load csv columns" part
        loadColumnsB = Button(mainframe, text="Load CSV columns", command=self.getCsvColumns)
        self.listbox = Listbox(mainframe)
        # "Google maps API" part
        self.apiKeyLabel = Label(mainframe, text="Google Maps API Key")
        self.apiKey = Entry(mainframe, width=30)
        # "GO! button" part
        self.go = Button(mainframe, text="Go!", command=self.startInputProcessing)
        # "error/warning message part
        self.error = Label(mainframe, textvariable=self.message)

        # Layout
        self.padLeft = 10
        csvLabel.grid(column=1, row=1, sticky=W, padx=(self.padLeft, 0), pady=(10, 0))
        self.csv_file.grid(column=1, row=2, sticky=(W, E), padx=(self.padLeft, 5))
        openFileB.grid(column=3, row=2, sticky=W, padx=(0, 10))
        seperatorLabel.grid(column=1, row=3, sticky=W, padx=(self.padLeft, 0))
        self.csv_seperator.grid(column=1, row=4, sticky=(W), padx=(self.padLeft, 0))
        loadColumnsB.grid(column=1, row=6, sticky=W, padx=(self.padLeft, 0), pady=(5, 0))
        self.apiKeyLabel.grid(column=1, row=7, sticky=W, padx=(self.padLeft, 0), pady=(10, 0)) 
        self.apiKey.grid(column=1, row=8, sticky=(W), padx=(self.padLeft, 0)) 
        self.go.grid(column=1, row=9, sticky=W, padx=(self.padLeft, 0), pady=(10, 0)) 
        self.error.grid(column=1, row=10, sticky=(W, E))

        # Color scheme
        self.backgr = "#737373"
        self.foregr = "#FFFFFF"
        self.button = "#991f00"
        self.buttonFont = "#FFFFFF"
        self.configure(background=self.backgr)
        csvLabel.configure(background=self.backgr, foreground=self.foregr)
        openFileB.configure(background=self.button, foreground=self.buttonFont)
        seperatorLabel.configure(background=self.backgr, foreground=self.foregr)
        loadColumnsB.configure(background=self.button, foreground=self.buttonFont)
        self.apiKeyLabel.configure(background=self.backgr, foreground=self.foregr)
        self.go.configure(background=self.button, foreground=self.buttonFont) 
        self.error.configure(background=self.backgr, foreground=self.button) 

def on_closing():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root = Tk()
root.title("Google Geolocation")
root.protocol("WM_DELETE_WINDOW", on_closing)
app = Application(master=root)
app.mainloop()

