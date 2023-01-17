############### IMPORT NECESSARY RESOURCES AND PROGRAMS ###############
#      Throughout the development of this project, many different     #
# recourses are used in order to make this program function. Below is #
# a list of all of the resources I have used and a brief description  #
#                     of why they are being used.                     #
#######################################################################

import tkinter as tk # import tkinter for gui
import customtkinter as ctk # import tkinter upgrade for 'beautifying'
import psycopg2 as pg2 # import psycopg2 to communicate with 'Receipt_Project_v3.0' database
import re # import re regular expressions for data filter
import datetime # import date to import calendar
from transmit_appended_data import transmitAppendedData # import needed 'transmitAppendedData' functionality
from transmit_entered_data import transmitEnteredData # import needed 'transmitEnteredData' functionality
from make_quarterly_moving_average import makeQuarterlyMovingAverage # import needed 'makeQuarterlyMovingAverage' functionality
from make_data_analytics import makeDataAnalytics # import needed 'makeDataAnalytics' functionality
from PIL import ImageTk, Image # import needed PIL functionality for displaying graphs



############### CREATE LINK BETWEEN PYTHON AND SQL SERVER ###############
# The point of this section of code is to use the psycopg2 library in   #
#         order to establish a connection between Python and the        #
# Receipt_Project_v3.0 database. With this connection, required in-file #
# functionalities such as searching for specific dates and displaying   #
#                       entries can be performed.                       #
#########################################################################

receipt_project = pg2.connect( # connect python to SQL
    host='localhost',
    database='Receipt_Project_v3.0',
    user='',
    password=''
)
receiptProjectCursor = receipt_project.cursor() # create cursor to input commands



############### LABEL FUNCTIONALITY ###############
# The point of the label functionality is to use  #
#  the mentioned psycopg2 cursor in order to get  #
#     the last entry date, as well as use the     #
#   datetime library in order to get the current  #
#                      date.                      #
###################################################

##### CURRENT DATE #####

getCurrentDate = datetime.datetime.now().date() # get the current date and assign contents to 'getCurrentDate'

##### LAST ENTRY #####

receiptProjectCursor.execute('select max(purchase_date) from base_fields_table') # grab date of last entry from 'Receipt_Project_v3.0'

getLastEntry = str(receiptProjectCursor.fetchall()[0][0]) # assign contents of SQL query to 'getLastEntry'



############### MAIN GUI CLASS ###############
#  The main gui class is the basis for all   #
#   the different elements of the project.   #
#   all frames, buttons, etc. are rooted to  #
#                this class.                 #
##############################################

class MainGUI(ctk.CTk): # establish 'MainGUI' class

    ##### 'MainGUI' DIMENSIONS #####

    WIDTH = 780  # width of tab set to 780px
    HEIGHT = 520  # height of tab set to 520px

    def __init__(gui): # main page functionality
        super().__init__()

        ##### CREATE TAB, SIZE AND TITLE #####

        gui.title("Matthew's Finance Tracker") # set title of tab
        gui.geometry(f"{MainGUI.WIDTH}x{MainGUI.HEIGHT}") # establish geometry with previous constants
        gui.resizable(False, False) # disable dynamic resizing of tab

        ##### CONSTRUCT GRID #####

        gui.grid_columnconfigure(1, weight=1) # configure tab grid x axis
        gui.grid_rowconfigure(0, weight=1) # configure tab grid y axis



############### OPTIONS BAR ###############
# The options bar is the one part of the  #
# gui that remains the same. It serves as #
# the navigational element for selection  #
#           of different pages.           #
###########################################

        ##### 'optionsBar' FRAME #####

        gui.optionsBar = ctk.CTkFrame( # construct 'optionsBar' frame
            master=gui,
            width=180,
            corner_radius=0
        )
        gui.optionsBar.grid(row=0, column=0, sticky="nswe") # align 'optionsBar' frame

        ##### 'optionsBar' GRID #####

        gui.optionsBar.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        gui.optionsBar.grid_rowconfigure(5, weight=1)  # empty row as spacing
        gui.optionsBar.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        gui.optionsBar.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        ##### 'optionsBarLabel' LABEL IN 'optionsBar' #####

        gui.optionsBarLabel = ctk.CTkLabel( # construct 'optionsBarLabel' label in 'optionsBar'
            master=gui.optionsBar,
            text="Options:",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -18)
        )
        gui.optionsBarLabel.grid(row=1, column=0, pady=10, padx=10) # align 'optionBarLabel' label in 'optionsBar'

        ##### 'displayAnalyticsButton' BUTTON IN 'optionsBar' #####

        gui.displayAnalyticsButton = ctk.CTkButton( # construct 'displayAnalyticsButton' button in 'optionsBar'
            master=gui.optionsBar,
            text="show analytics",
            command=gui.displayAnalyticsPage,
            hover=True,
            width=120,
            height=32,
            corner_radius=8,
            text_color="#E7F6F2",
            fg_color="#395B64",
            hover_color="#A5C9CA"
        )
        gui.displayAnalyticsButton.grid(row=2, column=0, pady=10, padx=20) # align 'displayAnalyticsButton' button in 'optionsbar'

        ##### 'addDataButton' BUTTON IN 'optionsBar' #####

        gui.addDataButton = ctk.CTkButton( # construct 'addDataButton' button in 'optionsBar'
            master=gui.optionsBar,
            text="add data",
            command=gui.addDataPage,
            hover = True,
            width=120,
            height=32,
            corner_radius=8,
            text_color="#E7F6F2",
            fg_color="#395B64",
            hover_color="#A5C9CA"
        )
        gui.addDataButton.grid(row=3, column=0, pady=10, padx=20) # align 'addDataButton' button in 'optionsBar'

        ##### 'appendDataButton' BUTTON IN 'optionsBar' #####

        gui.appendDataButton = ctk.CTkButton( # construct 'appendDataButton' button in 'optionsBar'
            master=gui.optionsBar,
            text="append data",
            command=gui.appendDataPage,
            hover = True,
            width=120,
            height=32,
            corner_radius=8,
            text_color="#E7F6F2",
            fg_color="#395B64",
            hover_color="#A5C9CA"
        )
        gui.appendDataButton.grid(row=4, column=0, pady=10, padx=20) # align 'appendDataButton' button in 'optionsBar'

        ##### 'homeButton' BUTTON IN 'optionsBar' #####

        gui.homeButton = ctk.CTkButton( # construct 'homeButton' button in 'optionsBar'
            master=gui.optionsBar,
            text="home",
            command=gui.returnHomePage,
            hover=True,
            width=120,
            height=32,
            corner_radius=8,
            text_color="#E7F6F2",
            fg_color="#395B64",
            hover_color="#A5C9CA"
        )
        gui.homeButton.grid(row=8, column=0, pady=10, padx=20) # align 'homeButton' button in 'optionsBar'



############### HOME PAGE ###############
# The home page is the opening page of  #
# the application; it is the exact same #
#     as the returnHomePage function.   #
#########################################

        ##### 'homePage' FRAME #####

        gui.homePage = ctk.CTkFrame( # construct 'homePage' frame
            master=gui,
            border_width=2,
            corner_radius=8,
            fg_color="#395B64",
            border_color="#395B64"
        )
        gui.homePage.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)  # align 'homePage' frame

        ##### 'homePage' GRID #####

        gui.homePage.rowconfigure((0, 1, 2, 3), weight=1)
        gui.homePage.rowconfigure(7, weight=10)
        gui.homePage.columnconfigure((0, 1), weight=1)
        gui.homePage.columnconfigure(2, weight=0)

        ##### 'graphLabel' LABEL IN 'homePage' #####

        gui.graphLabel = ctk.CTkLabel( # construct 'graphLabel' label in 'homePage'
            master=gui.homePage,
            text="Last Quarter:",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.graphLabel.grid(row=0, column=0, columnspan=6, rowspan=1, pady=15, padx=10, sticky="nsew") # align 'graphLabel' label in 'homePage'

        ##### 'graphBox' FRAME IN 'homePage' #####

        gui.graphBox = ctk.CTkFrame( # construct 'graphBox' frame in 'homePage' frame
            master=gui.homePage,
            border_width=2,
            corner_radius=8,
            border_color="#395B64"
        )
        gui.graphBox.grid(row=1, column=0, columnspan=6, rowspan=7, pady=0, padx=10, sticky="nsew") # align 'graphBox' frame in 'homePage'

        ##### 'graphBox' GRID IN 'homePage' #####

        gui.graphBox.rowconfigure(0, weight=1)  # configure 'graphBox' grid x axis
        gui.graphBox.columnconfigure(0, weight=1)  # configure 'graphBox' grid y axis

        ##### 'totalMovingAverageGraph' GRAPH IN 'graphBox' #####

        try: # try to make 'quarterlyMovingAverageGraph'

            makeQuarterlyMovingAverage() # call 'makeQuarterlyMovingAverage' from 'make_quarterly_moving_average.py' for 'quarterlyMovingAverageGraph.png'

            gui.quarterlyMovingAverageGraphImage = ImageTk.PhotoImage( # create 'quarterlyMovingAverageGraphImage' image
                Image.open(
                    '/Users/matthewbeck/Desktop/Projects/Receipt_Project_v3.0/quarterlyMovingAverageGraph.png'
                )
            )

            gui.quarterlyMovingAverageGraph = ctk.CTkLabel( # construct 'quarterlyMovingAverageGraph' graph in 'graphBox'
                master=gui.graphBox,
                image=gui.quarterlyMovingAverageGraphImage
            )
            gui.quarterlyMovingAverageGraph.quarterlyMovingAverageGraphImage = gui.quarterlyMovingAverageGraphImage # display 'quarterlyMovingAverageGraphImage' image
            gui.quarterlyMovingAverageGraph.grid(column=0, row=0, sticky="nwe", padx=15, pady=15) # align 'quarterlyMovingAverageGraph' graph in 'graphBox'

        except: # if 'quarterlyMovingAverageGraph' cannot be made, pass

            pass

        ##### 'currentDateLabel' LABEL IN 'homePage' #####

        gui.currentDateLabel = ctk.CTkLabel( # construct 'currentDateLabel' label in 'graphBox'
            master=gui.homePage,
            text="Current Date:",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.currentDateLabel.grid(row=8, column=0, columnspan=1, pady=10, padx=0, sticky="w") # align 'currentDateLabel' label in 'graphBox' frame

        ##### 'currentDate' LABEL IN 'homePage' #####

        gui.currentDate = ctk.CTkLabel( # construct 'currentDate' label in 'graphBox'
            master=gui.homePage,
            text=getCurrentDate,
            text_color="#E7F6F2"
        )
        gui.currentDate.grid(row=8, column=2, columnspan=1, pady=10, padx=0, sticky="w") # align 'currentDate' label in 'graphBox'

        ##### 'lastEntryLabel' LABEL IN 'homePage' #####

        gui.lastEntryLabel = ctk.CTkLabel( # construct 'lastEntryLabel' label in 'homePage'
            master=gui.homePage,
            text="Last Entry:",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.lastEntryLabel.grid(row=8, column=3, columnspan=1, pady=10, padx=0, sticky="e") # align 'lastEntryLabel' label in 'homePage'

        ##### 'lastEntry' LABEL IN 'homePage' #####

        gui.lastEntry = ctk.CTkLabel( # construct 'lastEntry' label in 'homePage'
            master=gui.homePage,
            text=getLastEntry,
            text_color="#E7F6F2"
        )
        gui.lastEntry.grid(row=8, column=4, columnspan=1, pady=10, padx=0, sticky="e")  # align 'lastEntry' label in 'homePage'

############### OPTIONS BAR BUTTON FUNCTIONALITY ###############
#  The options bar functionality are the function definitions  #
# that are called whenever a button within the options bar is  #
#  pressed. These functions include (but are not limited to)   #
#  the displayAnalyticsPage, appendDataPage, addDataPage, and  #
#               returnHomePage functionalities.                #
################################################################

    ########## 'displayAnalyticsPage' FUNCTION ##########
    #  The displayAnalyticsFunction is used to, as its  #
    #  name implies, display the analytics page, and is #
    #  accessed with the displayAnalyticsButton button. #
    #####################################################

    def displayAnalyticsPage(gui):

        ##### CONSTRUCT GRID #####

        gui.grid_columnconfigure(1, weight=1) # configure grid x axis
        gui.grid_rowconfigure(0, weight=1) # configure grid y axis

        ##### 'dataAnalyticsFrame' FRAME #####

        gui.dataAnalyticsFrame = ctk.CTkFrame( # construct 'dataAnalyticsFrame' frame
            master=gui,
            border_width=2,
            corner_radius=8,
            fg_color="#395B64",
            border_color="#395B64"
        )
        gui.dataAnalyticsFrame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20) # align 'dataAnalyticsFrame frame

        ##### 'dataAnalyticsFrame' GRID #####

        gui.dataAnalyticsFrame.rowconfigure((0, 1, 2, 3), weight=1)
        gui.dataAnalyticsFrame.rowconfigure(7, weight=10)
        gui.dataAnalyticsFrame.columnconfigure((0, 1), weight=1)
        gui.dataAnalyticsFrame.columnconfigure(2, weight=0)

        ##### 'dataAnalyticsLabel' LABEL IN 'dataAnalyticsFrame' #####

        gui.dataAnalyticsLabel = ctk.CTkLabel( # construct 'dataAnalyticsLabel' label
            master=gui.dataAnalyticsFrame,
            text="Data Analytics:",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.dataAnalyticsLabel.grid(row=0, column=0, columnspan=6, rowspan=1, pady=11, padx=0, sticky="n") # align 'dataAnalyticsLabel' label

        ##### 'periodOption' OPTION IN 'dataAnalyticsFrame' #####

        gui.periodOption = ctk.CTkOptionMenu( # construct 'yColumnOption' option in 'dataAnalyticsFrame'
            master=gui.dataAnalyticsFrame,
            values=["period", "total", "annual", "quarterly", "month"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.periodOption.grid(row=1, column=0, columnspan=1, pady=0, padx=10, sticky="") # align 'periodOption' option in 'dataAnalyticsFrame'

        ##### 'compareOneOption' OPTION IN 'dataAnalyticsFrame' #####

        gui.compareOneOption = ctk.CTkOptionMenu( # construct 'compareOneOption' option in 'dataAnalyticsFrame'
            master=gui.dataAnalyticsFrame,
            values=[
                "option 1", "all", "grocery", "gas/automobile", "healthcare", "school", "restaurant", "entertainment", "alcohol",
                "hair-care", "projects", "rent/home", "miscellaneous", "salary", "investments", "gift", "location", "city", "state"
            ],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.compareOneOption.grid(row=1, column=1, columnspan=1, pady=0, padx=10, sticky="") # align 'compareOneOption' option in 'dataAnalyticsFrame'

        ##### 'compareTwoOption' OPTION IN 'dataAnalyticsFrame' #####

        gui.compareTwoOption = ctk.CTkOptionMenu( # construct 'compareTwoOption' option in 'dataAnalyticsFrame'
            master=gui.dataAnalyticsFrame,
            values=[
                "option 2", "none", "grocery", "gas/automobile", "healthcare", "school", "restaurant", "entertainment", "alcohol",
                "hair-care", "projects", "rent/home", "miscellaneous", "salary", "investments", "gift"
            ],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.compareTwoOption.grid(row=1, column=2, columnspan=1, pady=0, padx=10, sticky="") # align 'compareTwoOption' option in 'dataAnalyticsFrame'

        ##### 'compareTypeOption' OPTION IN 'dataAnalyticsFrame' #####

        gui.compareTypeOption = ctk.CTkOptionMenu( # construct 'compareTypeOption' option in 'dataAnalyticsFrame'
            master=gui.dataAnalyticsFrame,
            values=["type", "avg", "reg", "bar"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.compareTypeOption.grid(row=1, column=3, columnspan=1, pady=0, padx=10, sticky="") # align 'compareTypeOption' option in 'dataAnalyticsFrame'

        ##### 'createGraphButton' BUTTON IN 'dataAnalyticsFrame' #####

        gui.createGraphButton = ctk.CTkButton( # construct 'createGraphButton' button in 'dataAnalyticsFrame'
            master=gui.dataAnalyticsFrame,
            text="create",
            hover=True,
            width=120,
            height=32,
            corner_radius=8,
            text_color="#395B64",
            fg_color="#A5C9CA",
            hover_color="#E7F6F2",
            command=gui.createDataAnalyticsGraph
        )
        gui.createGraphButton.grid(row=1, column=4, columnspan=1, pady=0, padx=10, sticky="") # align 'createGraphButton' button in 'dataAnalyticsFrame'

        ##### 'dataAnalyticsGraphBox' FRAME IN 'dataAnalyticsFrame' #####

        gui.dataAnalyticsGraphBox = ctk.CTkFrame( # construct 'dataAnalyticsGraphBox' frame in 'dataAnalyticsFrame' frame
            master=gui.dataAnalyticsFrame,
            border_width=2,
            corner_radius=8,
            border_color="#395B64"
        )
        gui.dataAnalyticsGraphBox.grid(row=2, column=0, columnspan=6, rowspan=7, pady=10, padx=10, sticky="nsew") # align 'dataAnalyticsGraphBox' frame in 'dataAnalyticsFrame'

        ##### 'dataAnalyticsGraphBox' GRID IN 'dataAnalyticsFrame' #####

        gui.graphBox.rowconfigure(0, weight=1)  # configure 'dataAnalyticsGraphBox' grid x axis
        gui.graphBox.columnconfigure(0, weight=1)  # configure 'dataAnalyticsGraphBox' grid y axis

        ##### 'dataAnalyticsGraphLabel' LABEL IN 'dataAnalyticsGraphBox' #####

        gui.dataAnalyticsGraphLabel = ctk.CTkLabel( # construct 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'
            master=gui.dataAnalyticsGraphBox,
            text="Enter Fields",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.dataAnalyticsGraphLabel.grid(column=0, row=0, sticky="ws", padx=215, pady=170) # align 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'

        ##### CONSTRUCT 'dataAnalyticsFrame' GRID #####

        gui.dataAnalyticsFrame.columnconfigure((0, 1), weight=1) # configure 'dataAnalyticsFrame' grid x axis
        gui.dataAnalyticsFrame.columnconfigure(2, weight=0) # configure 'dataAnalyticsFrame' grid x axis
        gui.dataAnalyticsFrame.rowconfigure((0, 1, 2, 3), weight=1) # configure 'dataAnalyticsFrame' grid y axis
        gui.dataAnalyticsFrame.rowconfigure(7, weight=10) # configure 'dataAnalyticsFrame' grid y axis



    ########## 'createAnalyticsGraph' FUNCTION ##########
    # The createAnalyticsGraph function is used to take #
    # entered parameters from the displayAnalyticsPage  #
    #  function page and then create a graph based on   #
    #                 those parameters.                 #
    #####################################################

    def createDataAnalyticsGraph(gui):

        ##### REFRESH 'createGraphButton' BUTTON AND 'dataAnalyticsGraph' LABEL IF EMPTY #####

        if ( # if all fields empty, throw 'createGraphButton' error
                (str(gui.periodOption.get()) == 'period') and
                (str(gui.compareOneOption.get()) == 'option 1') and
                (str(gui.compareTwoOption.get()) == 'option 2') and
                (str(gui.compareTypeOption.get()) == 'type')
        ):

            ##### REMOVE 'dataAnalyticsGraph' GRAPH #####

            try:  # remove 'dataAnalyticsGraph' to refresh page if it exists

                gui.dataAnalyticsGraph.configure(
                    image="",
                    sticky="nsew"
                )

            except:  # pass if 'dataAnalyticsGraph' does not exist

                pass

            ##### DISABLE 'createGraphButton' BUTTON IN 'dataAnalyticsFrame' #####

            gui.createGraphButton.configure( # reconfigure 'createGraphButton' to 'disable'
                text_color="#C6A49B",
                fg_color="#5A3635",
                hover_color="#18090D"
            )

            ##### 'dataAnalyticsGraph' ERROR LABEL IN 'dataAnalyticsFrame' #####

            try:  # reconfigure 'dataAnalyticsGraphLabel' label/graph to 'disable' if it exists

                gui.dataAnalyticsGraphLabel.configure(
                    text="Enter Fields",
                    text_color="#5A3635"
                )

            except:  # make 'dataAnalyticsGraphLabel' label/graph to 'disable' if it does not exist

                gui.dataAnalyticsGraphLabel = ctk.CTkLabel( # construct 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'
                    master=gui.dataAnalyticsGraphBox,
                    text="Enter Fields",
                    text_color="#5A3635",
                    text_font=("Roboto Medium", -15)
                )
                gui.dataAnalyticsGraphLabel.grid(column=0, row=0, sticky="ws", padx=215, pady=170) # align 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'

        ##### REFRESH 'createGraphButton' BUTTON AND 'dataAnalyticsGraph' LABEL IF PARTIALLY EMPTY #####

        elif ( # if some fields empty, throw 'createGraphButton' error
                (str(gui.periodOption.get()) == 'period') or
                (str(gui.compareOneOption.get()) == 'option 1') or
                (str(gui.compareTwoOption.get()) == 'option 2') or
                (str(gui.compareTypeOption.get()) == 'type')
        ):

            ##### REMOVE 'dataAnalyticsGraph' GRAPH #####

            try:  # remove 'dataAnalyticsGraph' to refresh page if it exists

                gui.dataAnalyticsGraph.configure(
                    image="",
                    sticky="nsew"
                )

            except:  # pass if 'dataAnalyticsGraph' does not exist

                pass

            ##### DISABLE 'createGraphButton' BUTTON IN 'dataAnalyticsFrame' #####

            gui.createGraphButton.configure( # reconfigure 'createGraphButton' to 'disable'
                text_color="#C6A49B",
                fg_color="#5A3635",
                hover_color="#18090D"
            )

            ##### 'dataAnalyticsGraph' ERROR LABEL IN 'dataAnalyticsFrame' #####

            try:  # reconfigure 'dataAnalyticsGraphLabel' label/graph to 'disable' if it exists

                gui.dataAnalyticsGraphLabel.configure(
                    text="Missing Fields",
                    text_color="#5A3635"
                )

            except:  # make 'dataAnalyticsGraphLabel' label/graph to 'disable' if it does not exist

                gui.dataAnalyticsGraphLabel = ctk.CTkLabel( # construct 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'
                    master=gui.dataAnalyticsGraphBox,
                    text="Missing Fields",
                    text_color="#5A3635",
                    text_font=("Roboto Medium", -15)
                )
                gui.dataAnalyticsGraphLabel.grid(column=0, row=0, sticky="ws", padx=215, pady=170)  # align 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'

        ##### IF ALL FIELDS FILLED, PROCEED #####

        elif ( # if all fields entered, proceed
            ((str(gui.periodOption.get()) != 'period') and
            (str(gui.compareOneOption.get()) != 'option 1') and
            (str(gui.compareTwoOption.get()) != 'option 2') and
            (str(gui.compareTypeOption.get()) != 'type'))
        ):

            ##### REFRESH 'createGraphButton' BUTTON AND 'dataAnalyticsGraph' LABEL IF FIELDS INCOMPATIBLE #####

            if ( # if some fields not compatible, throw 'createGraphButton' error
                (str(gui.compareTypeOption.get()) == 'bar') and
                ((str(gui.compareOneOption.get()) != 'location') or
                (str(gui.compareOneOption.get()) != 'city') or
                (str(gui.compareOneOption.get()) != 'state')) and
                (str(gui.compareTwoOption.get()) != 'none')
            ):

                ##### REMOVE 'dataAnalyticsGraph' GRAPH #####

                try:  # remove 'dataAnalyticsGraph' to refresh page if it exists

                    gui.dataAnalyticsGraph.configure(
                        image="",
                        sticky="nsew"
                    )

                except:  # pass if 'dataAnalyticsGraph' does not exist

                    pass

                ##### DISABLE 'createGraphButton' BUTTON IN 'dataAnalyticsFrame' #####

                gui.createGraphButton.configure( # reconfigure 'createGraphButton' to 'disable'
                    text_color="#C6A49B",
                    fg_color="#5A3635",
                    hover_color="#18090D"
                )

                ##### 'dataAnalyticsGraph' ERROR LABEL IN 'dataAnalyticsFrame' #####

                try:  # reconfigure 'dataAnalyticsGraphLabel' label/graph to 'disable' if it exists

                    gui.dataAnalyticsGraphLabel.configure(
                        text="Incompatible Fields",
                        text_color="#5A3635"
                    )

                except:  # make 'dataAnalyticsGraphLabel' label/graph to 'disable' if it does not exist

                    gui.dataAnalyticsGraphLabel = ctk.CTkLabel( # construct 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'
                        master=gui.dataAnalyticsGraphBox,
                        text="Incompatible Fields",
                        text_color="#5A3635",
                        text_font=("Roboto Medium", -15)
                    )
                    gui.dataAnalyticsGraphLabel.grid(column=0, row=0, sticky="ws", padx=215, pady=170) # align 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'

            ##### REFRESH ''createGraphButton' BUTTON AND 'dataAnalyticsGraphLabel' LABEL IF FIELDS INCOMPATIBLE #####

            elif ( # if some fields not compatible, throw 'createGraphButton' error
                (str(gui.compareTypeOption.get()) != 'bar') and
                ((str(gui.compareOneOption.get()) == 'location') or
                (str(gui.compareOneOption.get()) == 'city') or
                (str(gui.compareOneOption.get()) == 'state'))
            ):

                ##### REMOVE 'dataAnalyticsGraph' GRAPH #####

                try: # remove 'dataAnalyticsGraph' to refresh page if it exists

                    gui.dataAnalyticsGraph.configure(
                        image="",
                        sticky="nsew"
                    )

                except: # pass if 'dataAnalyticsGraph' does not exist

                    pass

                ##### DISABLE 'createGraphButton' BUTTON IN 'dataAnalyticsFrame' #####

                gui.createGraphButton.configure( # reconfigure 'createGraphButton' to 'disable'
                    text_color="#C6A49B",
                    fg_color="#5A3635",
                    hover_color="#18090D"
                )

                ##### 'dataAnalyticsGraph' ERROR LABEL IN 'dataAnalyticsFrame' #####

                try:  # reconfigure 'dataAnalyticsGraphLabel' label/graph to 'disable' if it exists

                    gui.dataAnalyticsGraphLabel.configure(
                        text="Incompatible Fields",
                        text_color="#5A3635"
                    )

                except:  # make 'dataAnalyticsGraphLabel' label/graph to 'disable' if it does not exist

                    gui.dataAnalyticsGraphLabel = ctk.CTkLabel( # construct 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'
                        master=gui.dataAnalyticsGraphBox,
                        text="Incompatible Fields",
                        text_color="#5A3635",
                        text_font=("Roboto Medium", -15)
                    )
                    gui.dataAnalyticsGraphLabel.grid(column=0, row=0, sticky="ws", padx=215, pady=170) # align 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'

            ##### REFRESH ''createGraphButton' BUTTON AND 'dataAnalyticsGraphLabel' LABEL IF FIELDS INCOMPATIBLE #####

            elif ( # if duplicate fields, throw 'createGraphButton' error
                str(gui.compareOneOption.get()) == str(gui.compareTwoOption.get())
            ):

                ##### REMOVE 'dataAnalyticsGraph' GRAPH #####

                try:  # remove 'dataAnalyticsGraph' to refresh page if it exists

                    gui.dataAnalyticsGraph.configure(
                        image="",
                        sticky="nsew"
                    )

                except:  # pass if 'dataAnalyticsGraph' does not exist

                    pass

                ##### DISABLE 'createGraphButton' BUTTON IN 'dataAnalyticsFrame' #####

                gui.createGraphButton.configure(  # reconfigure 'createGraphButton' to 'disable'
                    text_color="#C6A49B",
                    fg_color="#5A3635",
                    hover_color="#18090D"
                )

                ##### 'dataAnalyticsGraph' ERROR LABEL IN 'dataAnalyticsFrame' #####

                try: # reconfigure 'dataAnalyticsGraphLabel' label/graph to 'disable' if it exists

                    gui.dataAnalyticsGraphLabel.configure(
                        text="Duplicate Fields",
                        text_color="#5A3635"
                    )

                except:  # make 'dataAnalyticsGraphLabel' label/graph to 'disable' if it does not exist

                    gui.dataAnalyticsGraphLabel = ctk.CTkLabel( # construct 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'
                        master=gui.dataAnalyticsGraphBox,
                        text="Duplicate Fields",
                        text_color="#5A3635",
                        text_font=("Roboto Medium", -15)
                    )
                    gui.dataAnalyticsGraphLabel.grid(column=0, row=0, sticky="ws", padx=215, pady=170) # align 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'

            ##### IF ALL FIELDS CORRECTLY FILLED, PROCEED #####

            elif ( # if all fields correctly entered and are compatible, proceed
                ((str(gui.compareTypeOption.get()) == 'bar') and
                ((str(gui.compareOneOption.get()) == 'location') or
                (str(gui.compareOneOption.get()) == 'city') or
                (str(gui.compareOneOption.get()) == 'state'))) or
                ((str(gui.compareTypeOption.get()) != 'bar') and
                ((str(gui.compareOneOption.get()) != 'location') or
                (str(gui.compareOneOption.get()) != 'city') or
                (str(gui.compareOneOption.get()) != 'state')))
            ):

                ##### CREATE PARAMETERS FOR 'makeDataAnalytics' FUNCTION #####

                period = str(gui.periodOption.get())
                compareOne = str(gui.compareOneOption.get())
                compareTwo = str(gui.compareTwoOption.get())
                compareType = str(gui.compareTypeOption.get())

                ##### CALL 'makeDataAnalytics' FROM 'make_data_analytics.py' #####

                makeDataAnalytics(period, compareOne, compareTwo, compareType) # call 'makeDataAnalytics' from 'make_data_analytics.py' to make graph image

                ##### REMOVE 'dataAnalyticsGraphLabel' LABEL IN 'dataAnalyticsGraphBox' #####

                gui.dataAnalyticsGraphLabel.destroy()

                ##### MAKE 'dataAnalyticsGraph' GRAPH #####

                gui.dataAnalyticsGraphImage = ImageTk.PhotoImage(# create 'dataAnalyticsGraphImage' image
                    Image.open(
                        '/Users/matthewbeck/Desktop/Projects/Receipt_Project_v3.0/dataAnalyticsGraph.png'
                    )
                )

                gui.dataAnalyticsGraph = ctk.CTkLabel( # construct 'dataAnalyticsGraph' graph in 'graphBox'
                    master=gui.dataAnalyticsGraphBox,
                    image=gui.dataAnalyticsGraphImage
                )
                gui.dataAnalyticsGraph.dataAnalyticsGraphImage = gui.dataAnalyticsGraphImage  # display 'dataAnalyticsGraphImage' image
                gui.dataAnalyticsGraph.grid(column=0, row=0, sticky="nsew", padx=5, pady=20)  # align 'dataAnalyticsGraph' graph in 'dataAnalyticsGraphBox'

                ##### ENABLE 'createGraphButton' BUTTON IN 'dataAnalyticsFrame' #####

                gui.createGraphButton.configure( # reconfigure 'createGraphButton' to 'enable'
                    text_color="#395B64",
                    fg_color="#A5C9CA",
                    hover_color="#E7F6F2"
                )

            ##### REFRESH 'createGraphButton' BUTTON AND 'dataAnalyticsGraphLabel' LABEL IF UNSUCCESSFUL #####

            else: # if code somehow fails, proceed

                ##### REMOVE 'dataAnalyticsGraph' GRAPH #####

                try:  # remove 'dataAnalyticsGraph' to refresh page if it exists

                    gui.dataAnalyticsGraph.configure(
                        image="",
                        sticky="nsew"
                    )

                except:  # pass if 'dataAnalyticsGraph' does not exist

                    pass

                ##### DISABLE 'createGraphButton' BUTTON IN 'dataAnalyticsFrame' #####

                gui.createGraphButton.configure(  # reconfigure 'createGraphButton' to 'disable'
                    text_color="#C6A49B",
                    fg_color="#5A3635",
                    hover_color="#18090D"
                )

                ##### 'dataAnalyticsGraph' ERROR LABEL IN 'dataAnalyticsFrame' #####

                try: # reconfigure 'dataAnalyticsGraphLabel' label/graph to 'disable' if it exists

                    gui.dataAnalyticsGraphLabel.configure(
                        text="Incompatible Fields",
                        text_color="#5A3635"
                    )

                except: # make 'dataAnalyticsGraphLabel' label/graph to 'disable' if it does not exist

                    gui.dataAnalyticsGraphLabel = ctk.CTkLabel(# construct 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'
                        master=gui.dataAnalyticsGraphBox,
                        text="Incompatible Fields",
                        text_color="#5A3635",
                        text_font=("Roboto Medium", -15)
                    )
                    gui.dataAnalyticsGraphLabel.grid(column=0, row=0, sticky="ws", padx=215,pady=170)  # align 'dataAnalyticsGraphLabel' label in 'dataAnalyticsGraphBox'



    ########## 'appendDataPage' FUNCTION ##########
    #  The appendDataPage is used to display the  #
    # gui for appending past instances of data in #
    #                 the database.               #
    ###############################################

    def appendDataPage(gui):

        ##### CONSTRUCT APPEND DATA GRID #####

        gui.grid_columnconfigure(1, weight=1) # configure grid x axis
        gui.grid_rowconfigure(0, weight=1) # configure grid y axis

        ##### 'appendDataFrame' FRAME #####

        gui.appendDataFrame = ctk.CTkFrame( # construct 'appendDataFrame' frame
            master=gui,
            border_width=2,
            corner_radius=8,
            fg_color="#395B64",
            border_color="#395B64"
        )
        gui.appendDataFrame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20) # align 'appendDataFrame' frame

        ##### 'appendDataLabel' LABEL IN 'appendDataFrame' #####

        gui.appendDataLabel = ctk.CTkLabel( # construct 'appendDataLabel' label in 'appendDataFrame'
            master=gui.appendDataFrame,
            text="Enter Day:",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.appendDataLabel.grid(row=0, column=0, columnspan=6, rowspan=1, pady=5, padx=10, sticky="nsew") # align 'appendDataLabel' label in 'appendDataFrame'

        ##### 'appendPurchaseTypeLabel' LABEL IN 'appendDataFrame' #####

        gui.appendPurchaseTypeLabel = ctk.CTkLabel( # construct 'appendPurchaseTypeLabel' label in 'appendDataFrame'
            master=gui.appendDataFrame,
            text="Date (dd/mm/yyyy):",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.appendPurchaseTypeLabel.grid(row=1, column=0, columnspan=1, pady=6, padx=10, sticky="w") # align 'appendPurchaseTypeLabel' label in 'appendDataFrame'

        ##### 'appendPurchaseDayOption' OPTION IN 'appendDataFrame' #####

        gui.appendPurchaseDayOption = ctk.CTkOptionMenu( # construct 'appendPurchaseDayEntry' option in 'appendDataFrame'
            master=gui.appendDataFrame,
            values=["day", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
                    "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.appendPurchaseDayOption.grid(row=1, column=1, columnspan=1, pady=6, padx=10, sticky="we") # align 'appendPurchaseDayEntry' option in 'appendDataFrame'

        ##### 'appendPurchaseMonthOption' OPTION IN 'appendDataFrame' #####

        gui.appendPurchaseMonthOption = ctk.CTkOptionMenu( # construct 'appendPurchaseMonthEntry' option in 'appendDataFrame'
            master=gui.appendDataFrame,
            values=["month", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.appendPurchaseMonthOption.grid(row=1, column=2, columnspan=1, pady=6, padx=10, sticky="we") # align 'appendPurchaseMonthEntry' option in 'appendDataFrame'

        ##### 'appendPurchaseYearOption' OPTION IN 'appendDataFrame' #####

        gui.appendPurchaseYearOption = ctk.CTkOptionMenu( # construct 'appendPurchaseYearEntry' option in 'appendDataFrame'
            master=gui.appendDataFrame,
            values=["year", "2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030",
                    "2031", "2032", "2033", "2034", "2035", "2036", "2037", "2038", "2039", "2040", "2041", "2042",
                    "2043", "2044", "2045", "2046", "2047", "2048", "2049", "2050", "2051", "2052", "2053", "2054",
                    "2055", "2056", "2057", "2058", "2059", "2060", "2061", "2062", "2063", "2064", "2065", "2066",
                    "2067", "2068", "2069", "2070", "2071", "2072", "2073", "2074", "2075", "2076", "2077", "2078",
                    "2079", "2080", "2081", "2082", "2083", "2084", "2085", "2086", "2087", "2088", "2089", "2090",
                    "2091", "2092", "2093", "2094", "2095", "2096", "2097", "2098", "2099", "2100", "2101", "2102",
                    "2103", "2104", "2105", "2106", "2107", "2108", "2109", "2110", "2111", "2112", "2113", "2114",
                    "2115", "2116", "2117", "2118", "2119", "2120"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.appendPurchaseYearOption.grid(row=1, column=3, columnspan=1, pady=6, padx=10, sticky="w") # align 'appendPurchaseYearEntry' option in 'appendDataFrame'

        ##### 'appendDataButton' BUTTON IN 'appendDataFrame' #####

        gui.appendDataButton = ctk.CTkButton( # construct 'appendDataButton' button in 'appendDataFrame'
            master=gui.appendDataFrame,
            text="enter",
            hover=True,
            width=120,
            height=32,
            corner_radius=8,
            text_color="#395B64",
            fg_color="#A5C9CA",
            hover_color="#E7F6F2",
            command=gui.appendDataInputWindow
        )
        gui.appendDataButton.grid(row=9, column=3, columnspan=1, pady=10, padx=10, sticky="es")  # align 'appendDataButton' button in 'appendDataFrame'

        ##### 'appendDataStatusLabel' LABEL IN 'appendDataFrame' #####

        gui.appendDataStatusLabel = ctk.CTkLabel( # construct 'appendDataStatusLabel' label in 'appendDataFrame'
            master=gui.appendDataFrame,
            text="",
            text_color="#395B64",
            text_font=("Roboto Medium", -15)
        )
        gui.appendDataStatusLabel.grid(row=9, column=2, columnspan=1, pady=10, padx=0, sticky="es") # align 'appendDataStatusLabel' label in 'appendDataFrame'

        ##### 'searchBox' FRAME IN 'appendDataFrame' #####

        gui.searchBox = ctk.CTkFrame(  # construct 'searchBox' frame in 'appendDataFrame'
            master=gui.appendDataFrame,
            border_width=2,
            corner_radius=8,
            border_color="#395B64"
        )
        gui.searchBox.grid(row=2, column=0, columnspan=6, rowspan=7, pady=0, padx=10, sticky="nsew")  # align 'searchBox' frame in 'appendDataFrame'

        ##### 'searchBox' FRAME GRID #####

        gui.searchBox.columnconfigure(0, weight=1) # configure 'searchBox' grid x axis
        gui.searchBox.rowconfigure(100, weight=1)  # configure 'searchBox' grid y axis

        ##### APPEND DATA GRID #####

        gui.appendDataFrame.columnconfigure((0, 1), weight=1) # configure 'appendDataFrame' grid x axis
        gui.appendDataFrame.columnconfigure(2, weight=0) # configure 'appendDataFrame' grid x axis
        gui.appendDataFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1) # configure 'appendDataFrame' grid y axis
        gui.appendDataFrame.rowconfigure(9, weight=1) # configure 'appendDataFrame' grid y axis



    ########## 'appendDataInputWindow' FUNCTION ##########
    #  The appendDataInput function is used to transmit  #
    #   data entered in the append data page to SQL in   #
    #         order to find past date instances.         #
    ######################################################

    def appendDataInputWindow(gui): # function to filter data entered in 'addDataFrame' before transmitting to 'Receipt_Project_v3.0' database

        if ( # if all fields are left blank
            str(gui.appendPurchaseDayOption.get()) == 'day' or
            str(gui.appendPurchaseMonthOption.get()) == 'month' or
            str(gui.appendPurchaseYearOption.get()) == 'year'
        ):

            ##### RESET 'searchBox' IN 'appendDataFrame' IN 'appendDataFrame' #####

            del gui.searchBox # delete 'searchBox' in 'appendDataFrame'

            gui.searchBox = ctk.CTkFrame( # construct 'searchBox' frame in 'appendDataFrame'
                master=gui.appendDataFrame,
                border_width=2,
                corner_radius=8,
                border_color="#395B64"
            )
            gui.searchBox.grid(row=2, column=0, columnspan=6, rowspan=7, pady=0, padx=10, sticky="nsew")  # align 'searchBox' frame in 'appendDataFrame'

            gui.searchBox.columnconfigure(0, weight=1)  # configure 'searchBox' grid x axis
            gui.searchBox.rowconfigure(100, weight=1)  # configure 'searchBox' grid y axis

            ##### DISABLE 'appendDataButton' BUTTON IN 'appendDataFrame' #####

            gui.appendDataButton.configure( # reconfigure 'appendDataButton' to 'disable'
                text_color="#C6A49B",
                fg_color="#5A3635",
                hover_color="#18090D"
            )

            ##### 'appendDataStatusLabel' ERROR LABEL IN 'appendDataFrame' #####

            gui.appendDataStatusLabel.configure( # reconfigure 'appendDataStatusLabel' to prompt fields
                text="Enter Full Date",
                text_color="#5A3635",
            )

        elif ( # if fields correctly filled in
                str(gui.appendPurchaseDayOption.get()) != 'day' or
                str(gui.appendPurchaseMonthOption.get()) != 'month' or
                str(gui.appendPurchaseYearOption.get()) != 'year'
        ):

            ##### FIND 'appendDate' IN 'allDates' #####

            appendDate = str(gui.appendPurchaseYearOption.get()) + '/' + str(gui.appendPurchaseMonthOption.get()) + '/' + str(gui.appendPurchaseDayOption.get())

            if (appendDate.split('/')[1][0] == '0'):  # if month date begins with 0, remove 0
                monthDate = appendDate.split('/')[1][1]  # store value into 'monthDate'

            elif (appendDate.split('/')[1][0] != '0'):  # if month date does not begin with 0, change nothing
                monthDate = appendDate.split('/')[1]  # store value into 'monthDate'

            if (appendDate.split('/')[2][0] == '0'):  # if day date begins with 0, remove 0
                dayDate = appendDate.split('/')[2][1]  # store value into 'dayDate'

            elif (appendDate.split('/')[2][0] != '0'):  # if day date does not begin with 0, change nothing
                dayDate = appendDate.split('/')[2]  # store value into 'dayDate'

            # formulate 'appendDate' for date query to check for past instances
            appendDate = '(datetime.date(' + str(gui.appendPurchaseYearOption.get()) + ', ' + monthDate + ', ' + dayDate + '),)'

            receiptProjectCursor.execute( # grab list of all dates
                'select purchase_date from base_fields_table'
            )
            allDates = str(receiptProjectCursor.fetchall()) # assign contents to 'allDates'

            ##### REFRESH 'appendDataButton' BUTTON AND 'appendDataStatusLabel' LABEL IF SUCCESSFUL #####

            if (appendDate in allDates): # if selected 'appendDate' date with data to append in 'allDates'

                del gui.searchBox # delete 'searchBox' in 'appendDataFrame'

                ##### 'searchBox' FRAME IN 'appendDataFrame' IN 'appendDataFrame' #####

                gui.searchBox = ctk.CTkFrame(  # construct 'searchBox' frame in 'appendDataFrame'
                    master=gui.appendDataFrame,
                    border_width=2,
                    corner_radius=8,
                    border_color="#395B64"
                )
                gui.searchBox.grid(row=2, column=0, columnspan=6, rowspan=7, pady=0, padx=10,
                                   sticky="nsew")  # align 'searchBox' frame in 'appendDataFrame'

                ##### 'searchBox' FRAME GRID IN 'appendDataFrame' #####

                gui.searchBox.columnconfigure(0, weight=1)  # configure 'searchBox' grid x axis
                gui.searchBox.rowconfigure(100, weight=1)  # configure 'searchBox' grid y axis

                #### CREATE 'appendDataInstancesButton' BUTTONS #####

                appendDate = str(gui.appendPurchaseYearOption.get()) + ', ' + monthDate + ', ' + dayDate # restructure 'appendDate'

                receiptProjectCursor.execute( # grab list of all purchases
                    'select count(purchase_time) from purchase_table inner join base_fields_table on purchase_table.day_id = base_fields_table.day_id where base_fields_table.purchase_date = (%s)',
                    ((appendDate),)
                )
                dayTimeCount = str(receiptProjectCursor.fetchall()) # assign contents to 'dayTimeCount'

                dayTimeCount = int(re.sub( # restructure 'dayTimeCount'
                    '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§.,«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(dayTimeCount),
                    count=len(str(dayTimeCount))
                ))

                if (dayTimeCount == 0): # if no purchases found, throw error

                    ##### RESET 'searchBox' IN 'appendDataFrame' #####

                    del gui.searchBox  # delete 'searchBox' in 'appendDataFrame'

                    gui.searchBox = ctk.CTkFrame(  # construct 'searchBox' frame in 'appendDataFrame'
                        master=gui.appendDataFrame,
                        border_width=2,
                        corner_radius=8,
                        border_color="#395B64"
                    )
                    gui.searchBox.grid(row=2, column=0, columnspan=6, rowspan=7, pady=0, padx=10,
                                       sticky="nsew")  # align 'searchBox' frame in 'appendDataFrame'

                    gui.searchBox.columnconfigure(0, weight=1)  # configure 'searchBox' grid x axis
                    gui.searchBox.rowconfigure(100, weight=1)  # configure 'searchBox' grid y axis

                    ##### DISABLE 'appendDataButton' BUTTON IN 'appendDataFrame' #####

                    gui.appendDataButton.configure(  # reconfigure 'appendDataButton' to 'disable'
                        text_color="#C6A49B",
                        fg_color="#5A3635",
                        hover_color="#18090D"
                    )

                    ##### 'appendDataStatusLabel' ERROR LABEL IN 'appendDataFrame' #####

                    gui.appendDataStatusLabel.configure(  # reconfigure 'appendDataStatusLabel' for query failure
                        text="No Entries",
                        text_color="#5A3635",
                    )

                else: # if purchases found, proceed

                    dayTimes = [] # create array 'dayTimes' to store time instances

                    dayNames = [] # create array 'dayNames' to store name instances

                    for i in range(dayTimeCount):

                        dayTimes.append(i) # fill 'dayTimes' array

                        receiptProjectCursor.execute( # grab list of all times based on 'appendDate'
                            'select purchase_time from purchase_table inner join base_fields_table on purchase_table.day_id = base_fields_table.day_id where base_fields_table.purchase_date = (%s) order by purchase_date offset (%s) limit 1',
                            ((appendDate), (i),)
                        )
                        dayTimes[i] = str(receiptProjectCursor.fetchall()) # assign contents to 'dayTimes'

                        dayTimes[i] = str(re.sub( # restructure 'dayTimes'
                            '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§.,«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(dayTimes[i]),
                            count=len(str(dayTimes[i]))
                        ))

                        dayTimes[i] = dayTimes[i].split(" ") # split 'dayTimes' hour and minutes

                        if (int(dayTimes[i][0]) > 12 ): # if 'dayTimes' hour greater than 12, remove 12 and add 'PM'

                            dayTimes[i][0] = int(dayTimes[i][0]) - 12

                            if (len(dayTimes[i][1]) == 1): # if length of 'dayTimes' minutes 1, add '0' to beginning

                                dayTimes[i][1] = "0" + str(dayTimes[i][1]) + " PM"

                            else: # if length of 'dayTimes' minutes not 1, proceed

                                dayTimes[i][1] = str(dayTimes[i][1]) + " PM"

                        else: # if 'dayTimes' hour not greater than 12, add 'AM'

                            if (len(dayTimes[i][1]) == 1): # if length of 'dayTimes' minutes 1, add '0' to beginning

                                dayTimes[i][1] = "0" + str(dayTimes[i][1]) + " AM"

                            else: # if length of 'dayTimes' minutes not 1, proceed

                                dayTimes[i][1] = str(dayTimes[i][1]) + " AM"

                        dayTimes[i] = str(dayTimes[i][0]) + ":" + str(dayTimes[i][1]) # concatenate 'dayTimes' hour and minutes

                        dayNames.append(i) # fill 'dayNames' array

                        receiptProjectCursor.execute( # grab list of names based on 'appendDate'
                            'select establishment_name from location_table inner join base_fields_table on location_table.day_id = base_fields_table.day_id where base_fields_table.purchase_date = (%s) order by purchase_date offset (%s) limit 1',
                            ((appendDate), (i),)
                        )
                        dayNames[i] = str(receiptProjectCursor.fetchall()) # assign contents to 'dayNames'

                        dayNames[i] = str(re.sub( # restructure 'dayNames'
                            '[@_!$\[\]%^#&*()<>?/\|}{~:;¿§.,«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(dayNames[i]),
                            count=len(str(dayNames[i]))
                        ))

                        name = (str(i + 1) + ". " + str(dayNames[i].title()) + ", " + str(dayTimes[i])) # concatenate objects to form 'appendDataEntryButton' title

                        gui.appendDataEntryButton = ctk.CTkButton(
                            master=gui.searchBox,
                            text=f'{name}',
                            hover=True,
                            text_color="#A5C9CA",
                            fg_color="#292D2E",
                            hover_color="#395B64",
                            command=lambda i=i: gui.appendDataInput(appendDate, dayNames[i], dayTimes[i])
                        )
                        gui.appendDataEntryButton.grid(row=i, column=0, columnspan=1, pady=4, padx=4, sticky="wn")  # align 'appendDataEntryButton' Button in 'appendDataFrame'

                    ##### RE-ENABLE 'appendDataButton' BUTTON IN 'appendDataFrame' #####

                    gui.appendDataButton.configure(  # reconfigure 'appendDataButton' to 're-enable'
                        text_color="#395B64",
                        fg_color="#A5C9CA",
                        hover_color="#E7F6F2"
                    )

                    ##### 'appendDataStatusLabel' SUCCESS LABEL IN 'appendDataFrame' #####

                    gui.appendDataStatusLabel.configure(  # reconfigure 'appendDataStatusLabel' for query success
                        text="Entry(s) Found",
                        text_color="#A5C9CA",
                    )

            ##### REFRESH PAGE IF UNSUCCESSFUL #####

            else: # if there is no past data associated with 'appendDate'

                ##### RESET 'searchBox' IN 'appendDataFrame' #####

                del gui.searchBox # delete 'searchBox' in 'appendDataFrame'

                gui.searchBox = ctk.CTkFrame(  # construct 'searchBox' frame in 'appendDataFrame'
                    master=gui.appendDataFrame,
                    border_width=2,
                    corner_radius=8,
                    border_color="#395B64"
                )
                gui.searchBox.grid(row=2, column=0, columnspan=6, rowspan=7, pady=0, padx=10, sticky="nsew")  # align 'searchBox' frame in 'appendDataFrame'

                gui.searchBox.columnconfigure(0, weight=1)  # configure 'searchBox' grid x axis
                gui.searchBox.rowconfigure(100, weight=1)  # configure 'searchBox' grid y axis

                ##### DISABLE 'appendDataButton' BUTTON IN 'appendDataFrame' #####

                gui.appendDataButton.configure( # reconfigure 'appendDataButton' to 'disable'
                    text_color="#C6A49B",
                    fg_color="#5A3635",
                    hover_color="#18090D"
                )

                ##### 'appendDataStatusLabel' ERROR LABEL IN 'appendDataFrame' #####

                gui.appendDataStatusLabel.configure( # reconfigure 'appendDataStatusLabel' for query failure
                    text="No Entries",
                    text_color="#5A3635",
                )

    ########## 'appendDataInput' FUNCTION IN 'appendDataInputPage' ##########
    #    The appendDateInput function, when called, displays a page that    #
    # allows the user to change the data of a specific day by taking inputs #
    #     and transmitting those inputs to the appendDataEntry function.    #
    #########################################################################

    def appendDataInput(gui, date, name, time):

        ##### CREATE 'appendDayID' IN 'appendDataInput' #####

        receiptProjectCursor.execute(  # grab 'day_id' based on 'date'
            'select day_id from base_fields_table where purchase_date = (%s)',
            ((date),)
        )
        appendDayID = str(receiptProjectCursor.fetchall())  # assign contents to 'appendDayID'

        appendDayID = str(re.sub(  # restructure 'appendDayID'
            '[@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°,℃℉€¥£¢¡®©_+]', "", str(appendDayID),
            count=len(str(appendDayID))
        ))

        ##### CREATE 'appendHour', 'appendMinute', AND 'appendTime' IN 'appendDataInput' #####

        if (time[-2:] == "PM"):

            appendHour = int(time.split(":")[0]) + 12

        elif (time[-2:] == "AM"):

            if (len(time.split(":")[0]) == 1):

                appendHour = "0" + time.split(":")[0]

            else:

                appendHour = time.split(":")[0]

        appendMinute = time.split(":")[1][:2]

        appendTime = str(appendHour) + ":" + str(appendMinute) + ":00"

        ##### CREATE 'appendPurchaseID' IN 'appendDataInput' #####

        receiptProjectCursor.execute(  # grab 'purchase_id' based on 'date'
            'select purchase_id from purchase_table where day_id = (%s) and purchase_time = (%s)',
            ((appendDayID), (appendTime),)
        )
        appendPurchaseID = str(receiptProjectCursor.fetchall())  # assign contents to 'appendDayID'

        appendPurchaseID = str(re.sub(  # restructure 'appendPurchaseID'
            '[@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°,℃℉€¥£¢¡®©_+]', "", str(appendPurchaseID),
            count=len(str(appendPurchaseID))
        ))

        ##### CONSTRUCT APPEND DATA GRID #####

        gui.grid_columnconfigure(1, weight=1)  # configure grid x axis
        gui.grid_rowconfigure(0, weight=1)  # configure grid y axis

        ##### 'addDataFrame' FRAME IN 'appendDataInputFrame #####

        gui.appendDataInputFrame = ctk.CTkFrame(  # construct 'appendDataInputFrame' frame
            master=gui,
            border_width=2,
            corner_radius=8,
            fg_color="#395B64",
            border_color="#395B64"
        )
        gui.appendDataInputFrame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)  # align 'appendDataInputFrame' frame

        ##### 'appendDataLabel' LABEL IN 'appendDataInputFrame' #####

        gui.appendDataLabel = ctk.CTkLabel(  # construct 'appendDataLabel' frame in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            text="Append: " + str(name.title()) + ", at " + str(time) + " on " + str(date),
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.appendDataLabel.grid(row=0, column=0, columnspan=6, rowspan=1, pady=11, padx=10,
                                 sticky="nsew")  # align 'appendDataLabel' frame in 'appendDataInputFrame'

        ##### 'appendDataBackButton' BUTTON IN 'appendDataInputFrame' #####

        gui.appendDataBackButton = ctk.CTkButton( # construct 'appendEnterDataButton' button in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            text="back",
            hover=True,
            width=120,
            height=32,
            corner_radius=8,
            text_color="#395B64",
            fg_color="#A5C9CA",
            hover_color="#E7F6F2",
            command=gui.appendDataPage
        )
        gui.appendDataBackButton.grid(row=1, column=1, columnspan=1, pady=10, padx=0,
                                       sticky="ws") # align 'appendEnterDataButton' button in 'appendDataInputFrame'

        ##### 'appendDataDeleteButton' BUTTON IN 'appendDataInputFrame' #####

        gui.appendDataDeleteButton = ctk.CTkButton( # construct 'appendEnterDataButton' button in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            text="delete entry",
            hover=True,
            width=120,
            height=32,
            corner_radius=8,
            text_color="#C6A49B",
            fg_color="#5A3635",
            hover_color="#18090D",
            command=lambda: gui.appendDataEntry(appendDayID, appendPurchaseID, True, 1)
        )
        gui.appendDataDeleteButton.grid(row=1, column=2, columnspan=1, pady=10, padx=0,
                                       sticky="es") # align 'appendEnterDataButton' button in 'appendDataInputFrame'

        ##### 'appendPurchaseTimeLabel' LABEL IN 'appendDataInputFrame' #####

        gui.appendPurchaseTimeLabel = ctk.CTkLabel(
            # construct 'appendPurchaseTimeLabel' label in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            text="Time (hh:mm AM/PM):",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.appendPurchaseTimeLabel.grid(row=2, column=0, columnspan=1, pady=10, padx=10,
                                         sticky="w") # align 'appendPurchaseTimeLabel' label in 'appendDataInputFrame'

        ##### 'appendPurchaseHourOption' OPTION IN 'appendDataInputFrame' #####

        gui.appendPurchaseHourOption = ctk.CTkOptionMenu(
            # construct 'appendPurchaseHourOption' entry in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            values=["hour", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.appendPurchaseHourOption.grid(row=2, column=1, columnspan=1, pady=9, padx=10,
                                          sticky="we")  # align 'appendPurchaseHourOption' entry in 'appendDataInputFrame'

        ##### 'appendPurchaseMinuteOption' OPTION IN 'appendDataInputFrame' #####

        gui.appendPurchaseMinuteOption = ctk.CTkOptionMenu(
            # construct 'appendPurchaseMinuteOption' option in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            values=["minute", "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14",
                    "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                    "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46",
                    "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.appendPurchaseMinuteOption.grid(row=2, column=2, columnspan=1, pady=9, padx=10,
                                            sticky="w")  # align 'appendPurchaseMinuteOption' option in 'appendDataInputFrame'

        ##### 'appendPurchaseMeridiemOption' OPTION IN 'appendDataInputFrame' #####

        gui.appendPurchaseMeridiemOption = ctk.CTkOptionMenu(
            # construct 'appendPurchaseMeridiemOption' option in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            values=["meridiem", "AM", "PM"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.appendPurchaseMeridiemOption.grid(row=2, column=3, columnspan=1, pady=9, padx=10,
                                              sticky="w")  # align 'appendPurchaseMeridiemOption' option in 'appendDataInputFrame'

        ##### 'appendEstablishmentNameEntry' ENTRY IN 'appendDataInputFrame' #####

        gui.appendEstablishmentNameEntry = ctk.CTkEntry(
            # construct 'appendEstablishmentNameEntry' entry in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            width=120,
            placeholder_text="Establishment Name (leave blank if empty):",
            border_width=2,
            border_color="",
            text_color="#E7F6F2"
        )
        gui.appendEstablishmentNameEntry.grid(row=3, column=0, columnspan=4, pady=9, padx=10,
                                              sticky="we")  # align 'appendEstablishmentNameEntry' entry in 'appendDataInputFrame'

        ##### 'appendPurchaseAmountEntry' ENTRY IN 'appendDataInputFrame' #####

        gui.appendPurchaseAmountEntry = ctk.CTkEntry(
            # construct 'appendPurchaseAmountEntry' entry in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            width=120,
            placeholder_text="Purchase Amount (leave blank if empty):",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.appendPurchaseAmountEntry.grid(row=4, column=0, columnspan=4, pady=9, padx=10,
                                           sticky="we")  # align 'appendPurchaseAmountEntry' entry in 'appendDataInputFrame'

        ##### 'appendPurchaseTaxEntry' ENTRY IN 'appendDataInputFrame' #####

        gui.appendPurchaseTaxEntry = ctk.CTkEntry(  # construct 'appendPurchaseTaxEntry' entry in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            width=120,
            placeholder_text="Purchase Tax Percentage (leave blank if empty):",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.appendPurchaseTaxEntry.grid(row=5, column=0, columnspan=4, pady=9, padx=10,
                                        sticky="we")  # align 'appendPurchaseTaxEntry' entry in 'appendDataInputFrame'

        ##### 'appendPurchaseCurrencyEntry' ENTRY IN 'appendDataInputFrame' #####

        gui.appendPurchaseCurrencyEntry = ctk.CTkEntry(
            # construct 'appendPurchaseCurrencyEntry' ENTRY IN 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            width=120,
            placeholder_text="Purchase Currency (leave blank if empty):",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.appendPurchaseCurrencyEntry.grid(row=6, column=0, columnspan=4, pady=9, padx=10,
                                             sticky="we")  # align 'appendPurchaseCurrencyEntry' ENTRY IN 'appendDataInputFrame'

        ##### 'appendEmployeeNameEntry' ENTRY IN 'appendDataInputFrame' #####

        gui.appendEmployeeNameEntry = ctk.CTkEntry(
            # construct 'appendEmployeeNameEntry' entry in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            width=120,
            placeholder_text="Employee Name (leave blank if empty):",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.appendEmployeeNameEntry.grid(row=7, column=0, columnspan=4, pady=9, padx=10,
                                         sticky="we")  # align 'appendEmployeeNameEntry' entry in 'appendDataInputFrame'

        ##### 'appendEstablishmentNumAndStreetEntry' ENTRY IN 'appendDataInputFrame' #####

        gui.appendEstablishmentNumAndStreetEntry = ctk.CTkEntry(
            # construct 'appendEstablishmentNumAndStreetEntry' entry in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            width=100,
            placeholder_text="Num & Street:",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.appendEstablishmentNumAndStreetEntry.grid(row=8, column=0, columnspan=1, pady=9, padx=10,
                                                      sticky="we")  # align 'appendEstablishmentNumAndStreetEntry' entry in 'appendDataInputFrame'

        ##### 'appendEstablishmentCityEntry' ENTRY IN 'appendDataInputFrame' #####

        gui.appendEstablishmentCityEntry = ctk.CTkEntry(
            # construct 'appendEstablishmentCityEntry' entry in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            width=100,
            placeholder_text="City:",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.appendEstablishmentCityEntry.grid(row=8, column=1, columnspan=1, pady=9, padx=10,
                                              sticky="we")  # align 'appendEstablishmentCityEntry' entry in 'appendDataInputFrame'

        ##### 'appendEstablishmentStateEntry' ENTRY IN 'appendDataInputFrame' #####

        gui.appendEstablishmentStateEntry = ctk.CTkEntry(
            # construct 'appendEstablishmentStateEntry' entry in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            width=100,
            placeholder_text="State:",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.appendEstablishmentStateEntry.grid(row=8, column=2, columnspan=1, pady=9, padx=10,
                                               sticky="we")  # align 'appendEstablishmentStateEntry' entry in 'appendDataInputFrame'

        ##### 'appendEstablishmentZIPEntry' ENTRY IN 'appendDataInputFrame' #####

        gui.appendEstablishmentZIPEntry = ctk.CTkEntry(
            # construct 'appendEstablishmentZIPEntry' entry in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            width=100,
            placeholder_text="ZIP:",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.appendEstablishmentZIPEntry.grid(row=8, column=3, columnspan=1, pady=9, padx=10,
                                             sticky="we")  # align 'appendEstablishmentZIPEntry' entry in 'appendDataInputFrame'

        ##### 'appendPurchaseTypeLabel' LABEL IN 'appendDataInputFrame' #####

        gui.appendPurchaseTypeLabel = ctk.CTkLabel(
            # construct 'appendPurchaseTypeLabel' label in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            text="Purchase Type:",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.appendPurchaseTypeLabel.grid(row=9, column=0, columnspan=1, pady=10, padx=0,
                                         sticky="ws")  # align 'appendPurchaseTypeLabel' label in 'appendDataInputFrame'

        ##### 'appendPurchaseTypeOption' OPTION IN 'appendDataInputFrame' #####

        gui.appendPurchaseTypeOption = ctk.CTkOptionMenu(
            # construct 'appendPurchaseTypeOption' option in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            values=[
                "none", "grocery", "gas/automobile", "healthcare", "school", "restaurant", "entertainment", "alcohol",
                "hair-care", "projects", "rent/home", "miscellaneous", "salary", "investments", "gift"
            ],
            text_color="#395B64",
            hover=True,
            width=120,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.appendPurchaseTypeOption.grid(row=9, column=1, columnspan=1, pady=10, padx=0,
                                          sticky="ws")  # align 'appendPurchaseTypeOption' option in 'appendDataInputFrame'

        ##### 'appendEnterDataButton' BUTTON IN 'appendDataInputFrame' #####

        gui.appendEnterDataButton = ctk.CTkButton(  # construct 'appendEnterDataButton' button in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            text="enter",
            hover=True,
            width=120,
            height=32,
            corner_radius=8,
            text_color="#395B64",
            fg_color="#A5C9CA",
            hover_color="#E7F6F2",
            command=lambda: gui.appendDataEntry(appendDayID, appendPurchaseID, False, 0)
        )
        gui.appendEnterDataButton.grid(row=9, column=2, columnspan=1, pady=10, padx=0,
                                       sticky="es")  # align 'appendEnterDataButton' button in 'appendDataInputFrame'

        ##### 'appendEnterDataStatusLabel' LABEL IN 'appendDataInputFrame' #####

        gui.appendEnterDataStatusLabel = ctk.CTkLabel(
            # construct 'appendEnterDataStatusLabel' label in 'appendDataInputFrame'
            master=gui.appendDataInputFrame,
            text="",
            text_color="#395B64",
            text_font=("Roboto Medium", -15)
        )
        gui.appendEnterDataStatusLabel.grid(row=9, column=3, columnspan=1, pady=10, padx=0,
                                            sticky="es")  # align 'appendEnterDataStatusLabel' label in 'appendDataInputFrame'

        ##### CONSTRUCT 'appendDataInput' GRID #####

        gui.appendDataInputFrame.columnconfigure((0, 1), weight=1)  # configure 'appendDataInputFrame' grid x axis
        gui.appendDataInputFrame.columnconfigure(2, weight=0)  # configure 'appendDataInputFrame' grid x axis
        gui.appendDataInputFrame.rowconfigure((0, 1, 2, 3), weight=1)  # configure 'appendDataInputFrame' grid y axis
        gui.appendDataInputFrame.rowconfigure(9, weight=10)  # configure 'appendDataInputFrame' grid y axis



    ########## 'appendDataEntry' FUNCTION ##########
    #   The inputEnteredData function is used to   #
    #   send data entered in the appendDataInput   #
    #  page to the Receipt_Project_v3.0 database.  #
    ################################################

    def appendDataEntry(gui, appendDayID, appendPurchaseID, delete, deleteCount):

        ##### DELETE DATA IN 'Receipt_Project_v3.0' #####

        if (delete == True): # if 'delete' is true, proceed

            if (deleteCount == 2): # if 'deleteCount' is 2, delete entry and refresh 'appendDataPage'

                ##### DELETE 'purchase_table' DATA BASED ON 'appendPurchaseID' #####

                receiptProjectCursor.execute( # delete 'purchase_table' data where 'purchase_id' is 'appendPurchaseID'
                    'delete from purchase_table where purchase_id = (%s)',
                    ((appendPurchaseID),)
                )
                receipt_project.commit()  # submit query to 'Receipt_Project_v3.0'

                ##### DELETE 'location_table' DATA BASED ON 'appendPurchaseID' #####

                receiptProjectCursor.execute( # delete 'location_table' data where 'purchase_id' is 'appendPurchaseID'
                    'delete from location_table where purchase_id = (%s)',
                    ((appendPurchaseID),)
                )
                receipt_project.commit()  # submit query to 'Receipt_Project_v3.0'

                ##### FIND 'purchase_count' BASED ON 'appendDayID' #####

                receiptProjectCursor.execute(  # grab 'purchase_count' based on 'appendDayID'
                    'select purchase_count from base_fields_table where day_id = (%s)',
                    ((appendDayID),)
                )
                appendPurchaseCount = str(receiptProjectCursor.fetchall())  # assign contents to 'appendDayCount'

                appendPurchaseCount = int(re.sub( # restructure 'appendPurchaseCount'
                    '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°,℃℉€¥£¢¡®©_+]', "", str(appendPurchaseCount),
                    count=len(str(appendPurchaseCount))
                ))

                ##### UPDATE 'purchase_count' BASED ON 'appendDayID' #####

                if (appendPurchaseCount == 1 or appendPurchaseCount == 0): # if 'appendPurchaseCount' is 1, set 'purchase_count' to 0

                    receiptProjectCursor.execute( # set 'purchase_count' to 0 based on 'appendDayID'
                        'delete from base_fields_table where day_id = (%s)',
                        ((appendDayID),)
                    )
                    receipt_project.commit()  # submit query to 'Receipt_Project_v3.0'

                else: # if 'appendPurchaseCount' is not 1, remove 1 from 'purchase_count' value

                    receiptProjectCursor.execute( # set subtract 1 from 'purchase_count' based on 'appendDayID'
                        'update base_fields_table set purchase_count = (%s) where day_id = (%s)',
                        ((int(appendPurchaseCount) - 1), (appendDayID),)
                    )
                    receipt_project.commit() # submit query to 'Receipt_Project_v3.0'

                gui.appendDataPage() # recursive call 'appendDataPage' to reload the page

                ##### 'appendDataStatusLabel' ERROR LABEL IN 'appendDataFrame' #####

                gui.appendDataStatusLabel.configure(  # reconfigure 'appendDataStatusLabel' for query failure
                    text="Entry Deleted",
                    text_color="#A5C9CA",
                )

            else: # if 'deleteCount' is not 2, throw 'appendDataDeleteLabel' warning in 'appendDataInput'

                ##### 'appendDataDeleteLabel' WARNING LABEL IN 'appendDataInput' #####

                gui.appendDataDeleteLabel = ctk.CTkLabel(  # construct 'appendDataLabel' frame in 'appendDataInputFrame'
                    master=gui.appendDataInputFrame,
                    text="Are You Sure?",
                    text_color="#5A3635",
                    text_font=("Roboto Medium", -15)
                )
                gui.appendDataDeleteLabel.grid(row=1, column=3, columnspan=1, rowspan=1, pady=0, padx=0,
                                         sticky="nsew")  # align 'appendDataLabel' frame in 'appendDataInputFrame'

                ##### RECONFIGURE 'appendDataDeleteButton' BUTTON IN 'appendDataInput' #####

                gui.appendDataDeleteButton.configure( # construct 'appendEnterDataButton' button in 'appendDataInput'
                    text="press again",
                    text_color="#C6A49B",
                    fg_color="#5A3635",
                    hover_color="#18090D",
                    command=lambda: gui.appendDataEntry(appendDayID, appendPurchaseID, True, 2)
                )

        ##### UPDATE DATA IN 'Receipt_Project_v3.0' #####

        else: # if 'delete' is false, proceed

            ##### REFRESH PAGE IF UNSUCCESSFUL #####

            if (  # if all fields empty, throw 'appendEnterDataButton' error
                    (str(gui.appendPurchaseHourOption.get()) == 'hour') and (
                    str(gui.appendPurchaseMinuteOption.get()) == 'minute') and
                    (str(gui.appendPurchaseMeridiemOption.get()) == 'meridiem') and
                    (str(gui.appendPurchaseAmountEntry.get()) == None or str(gui.appendPurchaseAmountEntry.get()) == '') and
                    (str(gui.appendPurchaseTaxEntry.get()) == None or str(gui.appendPurchaseTaxEntry.get()) == '') and
                    (str(gui.appendPurchaseCurrencyEntry.get()) == None or str(
                        gui.appendPurchaseCurrencyEntry.get()) == '') and
                    (str(gui.appendEstablishmentNumAndStreetEntry.get()) == None or str(
                        gui.appendEstablishmentNumAndStreetEntry.get()) == '') and
                    (str(gui.appendEstablishmentCityEntry.get()) == None or str(
                        gui.appendEstablishmentCityEntry.get()) == '') and
                    (str(gui.appendEstablishmentStateEntry.get()) == None or str(
                        gui.appendEstablishmentStateEntry.get()) == '') and
                    (str(gui.appendEstablishmentZIPEntry.get()) == None or str(
                        gui.appendEstablishmentZIPEntry.get()) == '') and
                    (str(gui.appendPurchaseTypeOption.get()) == 'none')
            ):

                ##### DISABLE 'appendEnterDataButton' BUTTON #####

                gui.appendEnterDataButton.configure(  # reconfigure 'appendEnterDataButton' to 'disable'
                    text_color="#C6A49B",
                    fg_color="#5A3635",
                    hover_color="#18090D"
                )

                ##### 'appendEnterDataStatusLabel' ERROR LABEL #####

                gui.appendEnterDataStatusLabel.configure(  # reconfigure 'appendEnterDataStatusLabel' to prompt fields
                    text="No Data Found",
                    text_color="#5A3635"
                )

            ##### REFRESH 'appendEnterDataButton' BUTTON AND 'appendEnterDataStatusLabel' LABEL IF EMPTY #####

            elif (  # if all fields empty except 'purchaseDateEntry', proceed
                    (str(gui.appendPurchaseHourOption.get()) == 'hour') and (
                            str(gui.appendPurchaseMinuteOption.get()) == 'minute') and
                    (str(gui.appendPurchaseMeridiemOption.get()) == 'meridiem') and
                    (str(gui.appendPurchaseAmountEntry.get()) == None or str(gui.appendPurchaseAmountEntry.get()) == '') and
                    (str(gui.appendPurchaseTaxEntry.get()) == None or str(gui.appendPurchaseTaxEntry.get()) == '') and
                    (str(gui.appendPurchaseCurrencyEntry.get()) == None or str(
                        gui.appendPurchaseCurrencyEntry.get()) == '') and
                    (str(gui.appendEstablishmentNumAndStreetEntry.get()) == None or str(
                        gui.appendEstablishmentNumAndStreetEntry.get()) == '') and
                    (str(gui.appendEstablishmentCityEntry.get()) == None or str(
                        gui.appendEstablishmentCityEntry.get()) == '') and
                    (str(gui.appendEstablishmentStateEntry.get()) == None or str(
                        gui.appendEstablishmentStateEntry.get()) == '') and
                    (str(gui.appendEstablishmentZIPEntry.get()) == None or str(
                        gui.appendEstablishmentZIPEntry.get()) == '') and
                    (str(gui.appendPurchaseTypeOption.get()) == 'none')
            ):

                ##### DISABLE 'appendEnterDataButton' BUTTON #####

                gui.appendEnterDataButton.configure(  # reconfigure 'appendEnterDataButton' to 'disable'
                    text_color="#C6A49B",
                    fg_color="#5A3635",
                    hover_color="#18090D"
                )

                ##### 'appendEnterDataStatusLabel' ERROR LABEL #####

                gui.appendEnterDataStatusLabel.configure(  # reconfigure 'appendEnterDataStatusLabel' to prompt fields
                    text="No Data Found",
                    text_color="#5A3635",
                )

            ##### REFRESH 'appendEnterDataButton' BUTTON AND 'appendEnterDataStatusLabel' LABEL IF SUCCESSFUL #####

            elif (  # if fields are correctly filled in, test data for purity
                    (str(gui.appendPurchaseHourOption.get()) != 'hour') and (
                            str(gui.appendPurchaseMinuteOption.get()) != 'minute') and
                    (str(gui.appendPurchaseMeridiemOption.get()) != 'meridiem') and
                    (str(gui.appendPurchaseAmountEntry.get()) != None or str(gui.appendPurchaseAmountEntry.get()) != '') and
                    (str(gui.appendPurchaseTaxEntry.get()) != None or str(gui.appendPurchaseTaxEntry.get()) != '') and
                    (str(gui.appendPurchaseCurrencyEntry.get()) != None or str(
                        gui.appendPurchaseCurrencyEntry.get()) != '') and
                    (str(gui.appendEstablishmentNumAndStreetEntry.get()) != None or str(
                        gui.appendEstablishmentNumAndStreetEntry.get()) != '') and
                    (str(gui.appendEstablishmentCityEntry.get()) != None or str(
                        gui.appendEstablishmentCityEntry.get()) != '') and
                    (str(gui.appendEstablishmentStateEntry.get()) != None or str(
                        gui.appendEstablishmentStateEntry.get()) != '') and
                    (str(gui.appendEstablishmentZIPEntry.get()) != None or str(
                        gui.appendEstablishmentZIPEntry.get()) != '') and
                    (str(gui.appendPurchaseTypeOption.get()) != 'none')
            ):

                if ( # if item costs money, let 'appendPurchaseAmount' and 'appendPurchaseTax' be negative
                    str(gui.appendPurchaseTypeOption.get()) != 'salary' and
                    str(gui.appendPurchaseTypeOption.get()) != 'investments' and
                    str(gui.appendPurchaseTypeOption.get()) != 'gift'
                ):

                    try:  # if data present, grab data and convert it

                        appendEstablishmentName = str(gui.appendEstablishmentNameEntry.get()).lower()

                        # calculate 'appendPurchaseTime'
                        if (gui.appendPurchaseMeridiemOption.get() == "PM" and int(
                                gui.appendPurchaseHourOption.get()) < 12):  # if meridiem 'PM', add 12 hours to 'appendPurchaseHour'
                            appendPurchaseHour = str(int(gui.appendPurchaseHourOption.get()) + 12)

                        else:
                            appendPurchaseHour = gui.appendPurchaseHourOption.get()

                        appendPurchaseTime = appendPurchaseHour + ':' + gui.appendPurchaseMinuteOption.get() + ':' + '00'

                        # sort through provided 'appendPurchaseAmount' data
                        appendPurchaseAmount = str(gui.appendPurchaseAmountEntry.get())
                        appendPurchaseAmount = float("-" + str(
                            re.sub('[A-Za-z@_!$%^#&*()<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", appendPurchaseAmount,
                                   count=len(appendPurchaseAmount))
                        ))

                        # sort through provided 'appendPurchaseTax' data
                        appendPurchaseTax = str(gui.appendPurchaseTaxEntry.get())
                        appendPurchaseTax = float("-" + str(
                            re.sub('[A-Za-z@_!$%^#&*()<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", appendPurchaseTax,
                                   count=len(appendPurchaseTax))
                        ))

                        # make 'appendPurchaseCurrency' lowercase
                        appendPurchaseCurrency = str(gui.appendPurchaseCurrencyEntry.get()).lower()

                        # if 'appendEmployeeNameEntry' is blank, return none type
                        if (gui.appendEmployeeNameEntry.get() == None or gui.appendEmployeeNameEntry.get() == ''):
                            appendEmployeeName = None

                        # if 'appendEmployeeName' not blank, make contents lower case
                        else:
                            appendEmployeeName = str(gui.appendEmployeeNameEntry.get()).lower()

                        # make lowercase
                        appendEstablishmentNumAndStreet = str(gui.appendEstablishmentNumAndStreetEntry.get()).lower()
                        appendEstablishmentCity = str(gui.appendEstablishmentCityEntry.get()).lower()
                        appendEstablishmentState = str(gui.appendEstablishmentStateEntry.get()).lower()
                        appendEstablishmentZIP = int(gui.appendEstablishmentZIPEntry.get())
                        appendPurchaseType = str(gui.appendPurchaseTypeOption.get()).lower()
                        appendPurchaseTotal = appendPurchaseAmount

                        transmitAppendedData(
                            # call 'transmitAppendedData' functionality from 'transmit_appended_data.py'
                            appendEstablishmentName, appendPurchaseTime, appendPurchaseAmount,
                            appendPurchaseTax, appendPurchaseCurrency,
                            appendEmployeeName, appendEstablishmentNumAndStreet, appendEstablishmentCity,
                            appendEstablishmentState, appendEstablishmentZIP,
                            appendPurchaseType, appendPurchaseTotal, appendPurchaseID
                        )

                        gui.appendDataPage()  # recursive call 'appendDataPage' to reload the page

                        ##### 'appendEnterDataStatusLabel' SUCCESS LABEL #####

                        gui.appendDataStatusLabel.configure(
                            # reconfigure 'appendEnterDataStatusLabel' to prompt fields
                            text="Data Updated",
                            text_color="#A5C9CA",
                        )

                    except:  # if incorrect data present, throw enterDataButton error

                        ##### DISABLE 'appendEnterDataButton' BUTTON #####

                        gui.appendEnterDataButton.configure(  # reconfigure 'appendEnterDataButton' to 'disable'
                            text_color="#C6A49B",
                            fg_color="#5A3635",
                            hover_color="#18090D"
                        )

                        ##### 'appendEnterDataStatusLabel' ERROR LABEL #####

                        gui.appendEnterDataStatusLabel.configure(
                            # reconfigure 'appendEnterDataStatusLabel' to prompt fields
                            text="Faulty Input",
                            text_color="#5A3635",
                        )

                elif ( # if item makes money, let 'appendPurchaseAmount' and 'appendPurchaseTax' be positive
                    str(gui.appendPurchaseTypeOption.get()) == 'salary' or
                    str(gui.appendPurchaseTypeOption.get()) == 'investments' or
                    str(gui.appendPurchaseTypeOption.get()) == 'gift'
                ):

                    try:  # if data present, grab data and convert it

                        appendEstablishmentName = str(gui.appendEstablishmentNameEntry.get()).lower()

                        # calculate 'appendPurchaseTime'
                        if (gui.appendPurchaseMeridiemOption.get() == "PM" and int(
                                gui.appendPurchaseHourOption.get()) < 12):  # if meridiem 'PM', add 12 hours to 'appendPurchaseHour'
                            appendPurchaseHour = str(int(gui.appendPurchaseHourOption.get()) + 12)

                        else:
                            appendPurchaseHour = gui.appendPurchaseHourOption.get()

                        appendPurchaseTime = appendPurchaseHour + ':' + gui.appendPurchaseMinuteOption.get() + ':' + '00'

                        # sort through provided 'appendPurchaseAmount' data
                        appendPurchaseAmount = str(gui.appendPurchaseAmountEntry.get())
                        appendPurchaseAmount = float(
                            re.sub('[A-Za-z@_!$%^#&*()<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", appendPurchaseAmount,
                                   count=len(appendPurchaseAmount))
                        )

                        # sort through provided 'appendPurchaseTax' data
                        appendPurchaseTax = str(gui.appendPurchaseTaxEntry.get())
                        appendPurchaseTax = float(
                            re.sub('[A-Za-z@_!$%^#&*()<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", appendPurchaseTax,
                                   count=len(appendPurchaseTax))
                        )

                        # make 'appendPurchaseCurrency' lowercase
                        appendPurchaseCurrency = str(gui.appendPurchaseCurrencyEntry.get()).lower()

                        # if 'appendEmployeeNameEntry' is blank, return none type
                        if (gui.appendEmployeeNameEntry.get() == None or gui.appendEmployeeNameEntry.get() == ''):
                            appendEmployeeName = None

                        # if 'appendEmployeeName' not blank, make contents lower case
                        else:
                            appendEmployeeName = str(gui.appendEmployeeNameEntry.get()).lower()

                        # make lowercase
                        appendEstablishmentNumAndStreet = str(gui.appendEstablishmentNumAndStreetEntry.get()).lower()
                        appendEstablishmentCity = str(gui.appendEstablishmentCityEntry.get()).lower()
                        appendEstablishmentState = str(gui.appendEstablishmentStateEntry.get()).lower()
                        appendEstablishmentZIP = int(gui.appendEstablishmentZIPEntry.get())
                        appendPurchaseType = str(gui.appendPurchaseTypeOption.get()).lower()
                        appendPurchaseTotal = appendPurchaseAmount

                        transmitAppendedData(  # call 'transmitAppendedData' functionality from 'transmit_appended_data.py'
                            appendEstablishmentName, appendPurchaseTime, appendPurchaseAmount,
                            appendPurchaseTax, appendPurchaseCurrency,
                            appendEmployeeName, appendEstablishmentNumAndStreet, appendEstablishmentCity,
                            appendEstablishmentState, appendEstablishmentZIP,
                            appendPurchaseType, appendPurchaseTotal, appendPurchaseID
                        )

                        gui.appendDataPage()  # recursive call 'appendDataPage' to reload the page

                        ##### 'appendEnterDataStatusLabel' SUCCESS LABEL #####

                        gui.appendDataStatusLabel.configure(  # reconfigure 'appendEnterDataStatusLabel' to prompt fields
                            text="Data Updated",
                            text_color="#A5C9CA",
                        )

                    except:  # if incorrect data present, throw enterDataButton error

                        ##### DISABLE 'appendEnterDataButton' BUTTON #####

                        gui.appendEnterDataButton.configure(  # reconfigure 'appendEnterDataButton' to 'disable'
                            text_color="#C6A49B",
                            fg_color="#5A3635",
                            hover_color="#18090D"
                        )

                        ##### 'appendEnterDataStatusLabel' ERROR LABEL #####

                        gui.appendEnterDataStatusLabel.configure(  # reconfigure 'appendEnterDataStatusLabel' to prompt fields
                            text="Faulty Input",
                            text_color="#5A3635",
                        )

            ##### REFRESH 'appendEnterDataButton' BUTTON AND 'appendEnterDataStatusLabel' LABEL IF UNSUCCESSFUL #####

            else:  # if some but not all data entered (i.e. appendPurchaseDateEntry and appendPurchaseCurrencyEntry filled in but nothing else), throw appendEnterDataButton error

                ##### DISABLE 'appendEnterDataButton' BUTTON #####

                gui.appendEnterDataButton.configure(  # reconfigure 'appendEnterDataButton' to 'disable'
                    text_color="#C6A49B",
                    fg_color="#5A3635",
                    hover_color="#18090D"
                )

                ##### 'enterDataStatusLabel' ERROR LABEL #####

                gui.appendEnterDataStatusLabel.configure(  # reconfigure enterDataStatusLabel to prompt fields
                    text="Missing Fields",
                    text_color="#5A3635",
                )



    ########## 'addDataPage' FUNCTION ##########
    #   The addDataPage function is used to,   #
    #  when called, display the add data page, #
    #  and calls the inputEnteredData function #
    #        with its enterDataButton.         #
    ############################################

    def addDataPage(gui):

        ##### CONSTRUCT ADD DATA GRID #####

        gui.grid_columnconfigure(1, weight=1) # configure grid x axis
        gui.grid_rowconfigure(0, weight=1) # configure grid y axis

        ##### 'addDataFrame' FRAME #####

        gui.addDataFrame = ctk.CTkFrame( # construct 'addDataFrame' frame
            master=gui,
            border_width=2,
            corner_radius=8,
            fg_color="#395B64",
            border_color="#395B64"
        )
        gui.addDataFrame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20) # align 'addDataFrame' frame

        ##### 'addDataLabel' LABEL IN 'addDataFrame' #####

        gui.addDataLabel = ctk.CTkLabel( # construct 'addDataLabel' frame in 'addDataFrame'
            master=gui.addDataFrame,
            text="Add Data:",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.addDataLabel.grid(row=0, column=0, columnspan=6, rowspan=1, pady=11, padx=10, sticky="nsew") # align 'addDataLabel' frame in 'addDataFrame'

        ##### 'purchaseCalendarLabel' LABEL IN 'addDataFrame' #####

        gui.purchaseCalendarLabel = ctk.CTkLabel( # construct 'purchaseCalendarLabel' label in 'addDataFrame'
            master=gui.addDataFrame,
            text="Date (dd/mm/yyyy):",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.purchaseCalendarLabel.grid(row=1, column=0, columnspan=1, pady=10, padx=10, sticky="w") # align 'purchaseCalendarLabel' label in 'addDataFrame'

        ##### 'purchaseDayOption' OPTION IN 'addDataFrame' #####

        gui.purchaseDayOption = ctk.CTkOptionMenu( # construct 'purchaseDayOption' option in 'addDataFrame'
            master=gui.addDataFrame,
            values=["day", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
                    "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.purchaseDayOption.grid(row=1, column=1, columnspan=1, pady=9, padx=10, sticky="we") # align 'purchaseDayOption' option in 'addDataFrame'

        ##### 'purchaseMonthOption' OPTION IN 'addDataFrame' #####

        gui.purchaseMonthOption = ctk.CTkOptionMenu( # construct 'purchaseMonthOption' option in 'addDataFrame'
            master=gui.addDataFrame,
            values=["month", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.purchaseMonthOption.grid(row=1, column=2, columnspan=1, pady=9, padx=10, sticky="w") # align 'purchaseMonthOption' option in 'addDataFrame'

        ##### 'purchaseYearEntry' OPTION IN 'addDataFrame' #####

        gui.purchaseYearOption = ctk.CTkOptionMenu( # construct 'purchaseYearOption' option in 'addDataFrame'
            master=gui.addDataFrame,
            values=["year", "2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030",
                    "2031", "2032", "2033", "2034", "2035", "2036", "2037", "2038", "2039", "2040", "2041", "2042",
                    "2043", "2044", "2045", "2046", "2047", "2048", "2049", "2050", "2051", "2052", "2053", "2054",
                    "2055", "2056", "2057", "2058", "2059", "2060", "2061", "2062", "2063", "2064", "2065", "2066",
                    "2067", "2068", "2069", "2070", "2071", "2072", "2073", "2074", "2075", "2076", "2077", "2078",
                    "2079", "2080", "2081", "2082", "2083", "2084", "2085", "2086", "2087", "2088", "2089", "2090",
                    "2091", "2092", "2093", "2094", "2095", "2096", "2097", "2098", "2099", "2100", "2101", "2102",
                    "2103", "2104", "2105", "2106", "2107", "2108", "2109", "2110", "2111", "2112", "2113", "2114",
                    "2115", "2116", "2117", "2118", "2119", "2120"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.purchaseYearOption.grid(row=1, column=3, columnspan=1, pady=9, padx=10, sticky="w") # align 'purchaseYearOption' option in 'addDataFrame'

        ##### 'purchaseTimeLabel' LABEL IN 'addDataFrame' #####

        gui.purchaseTimeLabel = ctk.CTkLabel( # construct 'purchaseTimeLabel' label in 'addDataFrame'
            master=gui.addDataFrame,
            text="Time (hh:mm AM/PM):",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.purchaseTimeLabel.grid(row=2, column=0, columnspan=1, pady=10, padx=10, sticky="w") # align 'purchaseTimeLabel' label in 'addDataFrame'

        ##### 'purchaseHourOption' OPTION IN 'addDataFrame' #####

        gui.purchaseHourOption = ctk.CTkOptionMenu( # construct 'purchaseHourOption' entry in 'addDataFrame'
            master=gui.addDataFrame,
            values=["hour", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.purchaseHourOption.grid(row=2, column=1, columnspan=1, pady=9, padx=10, sticky="we") # align 'purchaseHourOption' entry in 'addDataFrame'

        ##### 'purchaseMinuteOption' OPTION IN 'addDataFrame' #####

        gui.purchaseMinuteOption = ctk.CTkOptionMenu( # construct 'purchaseMinuteOption' option in 'addDataFrame'
            master=gui.addDataFrame,
            values=["minute", "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14",
                    "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                    "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46",
                    "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.purchaseMinuteOption.grid(row=2, column=2, columnspan=1, pady=9, padx=10, sticky="w") # align 'purchaseMinuteOption' option in 'addDataFrame'

        ##### 'purchaseMeridiemOption' OPTION IN 'addDataFrame' #####

        gui.purchaseMeridiemOption = ctk.CTkOptionMenu( # construct 'purchaseMeridiemOption' option in 'addDataFrame'
            master=gui.addDataFrame,
            values=["meridiem", "AM", "PM"],
            text_color="#395B64",
            hover=True,
            width=100,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.purchaseMeridiemOption.grid(row=2, column=3, columnspan=1, pady=9, padx=10, sticky="w") # align 'purchaseMeridiemOption' option in 'addDataFrame'

        ##### 'establishmentNameEntry' ENTRY IN 'addDataFrame' #####

        gui.establishmentNameEntry = ctk.CTkEntry( # construct 'establishmentNameEntry' entry in 'addDataFrame'
            master=gui.addDataFrame,
            width=120,
            placeholder_text="Establishment Name (leave blank if empty):",
            border_width=2,
            border_color="",
            text_color="#E7F6F2"
        )
        gui.establishmentNameEntry.grid(row=3, column=0, columnspan=4, pady=9, padx=10, sticky="we") # align 'establishmentNameEntry' entry in 'addDataFrame'

        ##### 'purchaseAmountEntry' ENTRY IN 'addDataFrame' #####

        gui.purchaseAmountEntry = ctk.CTkEntry( # construct 'purchaseAmountEntry' entry in 'addDataFrame'
            master=gui.addDataFrame,
            width=120,
            placeholder_text="Purchase Amount (leave blank if empty):",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.purchaseAmountEntry.grid(row=4, column=0, columnspan=4, pady=9, padx=10, sticky="we") # align 'purchaseAmountEntry' entry in 'addDataFrame'

        ##### 'purchaseTaxEntry' ENTRY IN 'addDataFrame' #####

        gui.purchaseTaxEntry = ctk.CTkEntry( # construct 'purchaseTaxEntry' entry in 'addDataFrame'
            master=gui.addDataFrame,
            width=120,
            placeholder_text="Purchase Tax Percentage (leave blank if empty):",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.purchaseTaxEntry.grid(row=5, column=0, columnspan=4, pady=9, padx=10, sticky="we") # align 'purchaseTaxEntry' entry in 'addDataFrame'

        ##### 'purchaseCurrencyEntry' ENTRY IN 'addDataFrame' #####

        gui.purchaseCurrencyEntry = ctk.CTkEntry( # construct 'purchaseCurrencyEntry' ENTRY IN 'addDataFrame'
            master=gui.addDataFrame,
            width=120,
            placeholder_text="Purchase Currency (leave blank if empty):",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.purchaseCurrencyEntry.grid(row=6, column=0, columnspan=4, pady=9, padx=10, sticky="we") # align 'purchaseCurrencyEntry' ENTRY IN 'addDataFrame'

        ##### 'employeeNameEntry' ENTRY IN 'addDataFrame' #####

        gui.employeeNameEntry = ctk.CTkEntry( # construct 'employeeNameEntry' entry in 'addDataFrame'
            master=gui.addDataFrame,
            width=120,
            placeholder_text="Employee Name (leave blank if empty):",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.employeeNameEntry.grid(row=7, column=0, columnspan=4, pady=9, padx=10, sticky="we") # align 'employeeNameEntry' entry in 'addDataFrame'

        ##### 'establishmentNumAndStreetEntry' ENTRY IN 'addDataFrame' #####

        gui.establishmentNumAndStreetEntry = ctk.CTkEntry( # construct 'establishmentNumAndStreetEntry' entry in 'addDataFrame'
            master=gui.addDataFrame,
            width=100,
            placeholder_text="Num & Street:",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.establishmentNumAndStreetEntry.grid(row=8, column=0, columnspan=1, pady=9, padx=10, sticky="we") # align 'establishmentNumAndStreetEntry' entry in 'addDataFrame'

        ##### 'establishmentCityEntry' ENTRY IN 'addDataFrame' #####

        gui.establishmentCityEntry = ctk.CTkEntry( # construct 'establishmentCityEntry' entry in 'addDataFrame'
            master=gui.addDataFrame,
            width=100,
            placeholder_text="City:",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.establishmentCityEntry.grid(row=8, column=1, columnspan=1, pady=9, padx=10, sticky="we") # align 'establishmentCityEntry' entry in 'addDataFrame'

        ##### 'establishmentStateEntry' ENTRY IN 'addDataFrame' #####

        gui.establishmentStateEntry = ctk.CTkEntry( # construct 'establishmentStateEntry' entry in 'addDataFrame'
            master=gui.addDataFrame,
            width=100,
            placeholder_text="State:",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.establishmentStateEntry.grid(row=8, column=2, columnspan=1, pady=9, padx=10, sticky="we") # align 'establishmentStateEntry' entry in 'addDataFrame'

        ##### 'establishmentZIPEntry' ENTRY IN 'addDataFrame' #####

        gui.establishmentZIPEntry = ctk.CTkEntry( # construct 'establishmentZIPEntry' entry in 'addDataFrame'
            master=gui.addDataFrame,
            width=100,
            placeholder_text="ZIP:",
            border_width=2,
            border_color="",
            text_color="#E7F6F2",
            validate='key'
        )
        gui.establishmentZIPEntry.grid(row=8, column=3, columnspan=1, pady=9, padx=10, sticky="we") # align 'establishmentZIPEntry' entry in 'addDataFrame'

        ##### 'purchaseTypeLabel' LABEL IN 'addDataFrame' #####

        gui.purchaseTypeLabel = ctk.CTkLabel( # construct 'purchaseTypeLabel' label in 'addDataFrame'
            master=gui.addDataFrame,
            text="Purchase Type:",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.purchaseTypeLabel.grid(row=9, column=0, columnspan=1, pady=10, padx=0, sticky="ws") # align 'purchaseTypeLabel' label in 'addDataFrame'

        ##### 'purchaseTypeOption' OPTION IN 'addDataFrame' #####

        gui.purchaseTypeOption = ctk.CTkOptionMenu( # construct 'purchaseTypeOption' option in 'addDataFrame'
            master=gui.addDataFrame,
            values=[
                "none", "grocery", "gas/automobile", "healthcare", "school", "restaurant", "entertainment", "alcohol",
                "hair-care", "projects", "rent/home", "miscellaneous", "salary", "investments", "gift"
            ],
            text_color="#395B64",
            hover=True,
            width=120,
            height=32,
            corner_radius=8,
            button_hover_color="#E7F6F2",
            button_color="#A5C9CA",
            fg_color="#A5C9CA"
        )
        gui.purchaseTypeOption.grid(row=9, column=1, columnspan=1, pady=10, padx=0, sticky="ws") # align 'purchaseTypeOption' option in 'addDataFrame'

        ##### 'enterDataButton' BUTTON IN 'addDataFrame' #####

        gui.enterDataButton = ctk.CTkButton( # construct 'enterDataButton' button in 'addDataFrame'
            master=gui.addDataFrame,
            text="enter",
            hover=True,
            width=120,
            height=32,
            corner_radius=8,
            text_color="#395B64",
            fg_color="#A5C9CA",
            hover_color="#E7F6F2",
            command=gui.inputEnteredData
        )
        gui.enterDataButton.grid(row=9, column=2, columnspan=1, pady=10, padx=0, sticky="es") # align 'enterDataButton' button in 'addDataFrame'

        ##### 'enterDataStatusLabel' LABEL IN 'addDataFrame' #####

        gui.enterDataStatusLabel = ctk.CTkLabel( # construct 'enterDataStatusLabel' label in 'addDataFrame'
            master=gui.addDataFrame,
            text="",
            text_color="#395B64",
            text_font=("Roboto Medium", -15)
        )
        gui.enterDataStatusLabel.grid(row=9, column=3, columnspan=1, pady=10, padx=0, sticky="es") # align 'enterDataStatusLabel' label in 'addDataFrame'

        ##### CONSTRUCT 'addDataFrame' GRID #####

        gui.addDataFrame.columnconfigure((0, 1), weight=1) # configure 'addDataFrame' grid x axis
        gui.addDataFrame.columnconfigure(2, weight=0) # configure 'addDataFrame' grid x axis
        gui.addDataFrame.rowconfigure((0, 1, 2, 3), weight=1) # configure 'addDataFrame' grid y axis
        gui.addDataFrame.rowconfigure(9, weight=10) # configure 'addDataFrame' grid y axis



    ########## 'inputEnteredData' FUNCTION ##########
    # The inputEnteredData function is used to send #
    #    data entered in the addDataPage to the     #
    #        Receipt_Project_v3.0 database.         #
    #################################################

    def inputEnteredData(gui):

        ##### REFRESH PAGE IF UNSUCCESSFUL #####

        if ( # if all fields empty, throw 'enterDataButton' error
                (str(gui.purchaseDayOption.get()) == 'day') and (str(gui.purchaseMonthOption.get()) == 'month') and
                (str(gui.purchaseYearOption.get()) == 'year') and
                (str(gui.purchaseHourOption.get()) == 'hour') and (str(gui.purchaseMinuteOption.get()) == 'minute') and
                (str(gui.purchaseMeridiemOption.get()) == 'meridiem') and
                (str(gui.purchaseAmountEntry.get()) == None or str(gui.purchaseAmountEntry.get()) == '') and
                (str(gui.purchaseTaxEntry.get()) == None or str(gui.purchaseTaxEntry.get()) == '') and
                (str(gui.purchaseCurrencyEntry.get()) == None or str(gui.purchaseCurrencyEntry.get()) == '') and
                (str(gui.establishmentNumAndStreetEntry.get()) == None or str(
                    gui.establishmentNumAndStreetEntry.get()) == '') and
                (str(gui.establishmentCityEntry.get()) == None or str(gui.establishmentCityEntry.get()) == '') and
                (str(gui.establishmentStateEntry.get()) == None or str(gui.establishmentStateEntry.get()) == '') and
                (str(gui.establishmentZIPEntry.get()) == None or str(gui.establishmentZIPEntry.get()) == '') and
                (str(gui.purchaseTypeOption.get()) == 'none')
        ):
            ##### DISABLE 'enterDataButton' BUTTON #####

            gui.enterDataButton.configure(  # reconfigure 'enterDataButton' to 'disable'
                text_color="#C6A49B",
                fg_color="#5A3635",
                hover_color="#18090D"
            )

            ##### 'enterDataStatusLabel' ERROR LABEL #####

            gui.enterDataStatusLabel.configure(  # reconfigure 'enterDataStatusLabel' to prompt fields
                text="No Data Found",
                text_color="#5A3635",
            )

        ##### REFRESH 'enterDataButton' BUTTON AND 'enterDataStatusLabel' LABEL IF SUCCESSFUL #####

        elif (  # if all fields empty except 'purchaseDateEntry', proceed
                (str(gui.purchaseDayOption.get()) != 'day') and (str(gui.purchaseMonthOption.get()) != 'month') and
                (str(gui.purchaseYearOption.get()) != 'year') and
                (str(gui.purchaseHourOption.get()) == 'hour') and (str(gui.purchaseMinuteOption.get()) == 'minute') and
                (str(gui.purchaseMeridiemOption.get()) == 'meridiem') and
                (str(gui.purchaseAmountEntry.get()) == None or str(gui.purchaseAmountEntry.get()) == '') and
                (str(gui.purchaseTaxEntry.get()) == None or str(gui.purchaseTaxEntry.get()) == '') and
                (str(gui.purchaseCurrencyEntry.get()) == None or str(gui.purchaseCurrencyEntry.get()) == '') and
                (str(gui.establishmentNumAndStreetEntry.get()) == None or str(
                    gui.establishmentNumAndStreetEntry.get()) == '') and
                (str(gui.establishmentCityEntry.get()) == None or str(gui.establishmentCityEntry.get()) == '') and
                (str(gui.establishmentStateEntry.get()) == None or str(gui.establishmentStateEntry.get()) == '') and
                (str(gui.establishmentZIPEntry.get()) == None or str(gui.establishmentZIPEntry.get()) == '') and
                (str(gui.purchaseTypeOption.get()) == 'none')
        ):

            ##### FILL EMPTY FIELDS #####

            establishmentName = None

            # calculate 'purchaseDate'
            purchaseDate = str(gui.purchaseYearOption.get()) + "/" + str(gui.purchaseMonthOption.get()) + "/" + str(
                gui.purchaseDayOption.get())

            purchaseTime = None
            purchaseAmount = None
            purchaseTax = None
            purchaseCurrency = None
            employeeName = None
            establishmentNumAndStreet = None
            establishmentCity = None
            establishmentState = None
            establishmentZIP = None
            purchaseType = None
            purchasePresent = False
            purchaseCount = None
            purchaseTotal = None

            try: # if correct date entered

                transmitEnteredData(  # call 'transmitEnteredData' functionality from 'transmit_entered_date.py'
                    establishmentName, purchaseDate, purchaseTime, purchaseAmount, purchaseTax, purchaseCurrency,
                    employeeName, establishmentNumAndStreet, establishmentCity, establishmentState, establishmentZIP,
                    purchaseType, purchasePresent, purchaseCount, purchaseTotal
                )

                ##### REFRESH PAGE IF SUCCESSFUL #####

                gui.addDataPage()  # recursive call addDataPage to reload the page

                ##### 'enterDataStatusLabel' SUCCESS LABEL #####

                gui.enterDataStatusLabel.configure(  # reconfigure enterDataStatusLabel to prompt fields
                    text="Data Uploaded",
                    text_color="#A5C9CA",
                )

            except: # if incorrect date entered

                ##### DISABLE 'enterDataButton' BUTTON #####

                gui.enterDataButton.configure(  # reconfigure enterDataButton to 'disable'
                    text_color="#C6A49B",
                    fg_color="#5A3635",
                    hover_color="#18090D"
                )

                ##### 'enterDataStatusLabel' ERROR LABEL #####

                gui.enterDataStatusLabel.configure(  # reconfigure enterDataStatusLabel to prompt fields
                    text="Incorrect Date",
                    text_color="#5A3635",
                )

        ##### REFRESH 'enterDataButton' BUTTON AND 'enterDataStatusLabel' LABEL IF SUCCESSFUL #####

        elif ( # if fields are correctly filled in, test data for purity
                (str(gui.purchaseDayOption.get()) != 'day') and (str(gui.purchaseMonthOption.get()) != 'month') and
                (str(gui.purchaseYearOption.get()) != 'year') and
                (str(gui.purchaseHourOption.get()) != 'hour') and (str(gui.purchaseMinuteOption.get()) != 'minute') and
                (str(gui.purchaseMeridiemOption.get()) != 'meridiem') and
                (str(gui.purchaseAmountEntry.get()) != None or str(gui.purchaseAmountEntry.get()) != '') and
                (str(gui.purchaseTaxEntry.get()) != None or str(gui.purchaseTaxEntry.get()) != '') and
                (str(gui.purchaseCurrencyEntry.get()) != None or str(gui.purchaseCurrencyEntry.get()) != '') and
                (str(gui.establishmentNumAndStreetEntry.get()) != None or str(gui.establishmentNumAndStreetEntry.get()) != '') and
                (str(gui.establishmentCityEntry.get()) != None or str(gui.establishmentCityEntry.get()) != '') and
                (str(gui.establishmentStateEntry.get()) != None or str(gui.establishmentStateEntry.get()) != '') and
                (str(gui.establishmentZIPEntry.get()) != None or str(gui.establishmentZIPEntry.get()) != '') and
                (str(gui.purchaseTypeOption.get()) != 'none')
        ):

            if (  # if item costs money, let 'appendPurchaseAmount' and 'appendPurchaseTax' be negative
                    str(gui.purchaseTypeOption.get()) != 'salary' and
                    str(gui.purchaseTypeOption.get()) != 'investments' and
                    str(gui.purchaseTypeOption.get()) != 'gift'
            ):

                try:  # if data present, grab data and convert it

                    # calculate 'purchaseDate'
                    purchaseDate = str(gui.purchaseYearOption.get()) + "/" + str(
                        gui.purchaseMonthOption.get()) + "/" + str(
                        gui.purchaseDayOption.get())

                    establishmentName = str(gui.establishmentNameEntry.get()).lower()

                    # calculate 'purchaseTime'
                    if (gui.purchaseMeridiemOption.get() == "PM" and int(
                            gui.purchaseHourOption.get()) < 12):  # if meridiem 'PM', add 12 hours to 'purchaseHour'
                        purchaseHour = str(int(gui.purchaseHourOption.get()) + 12)

                    else:
                        purchaseHour = gui.purchaseHourOption.get()

                    purchaseTime = purchaseHour + ':' + gui.purchaseMinuteOption.get() + ':' + '00'

                    # sort through provided 'purchaseAmount' data
                    purchaseAmount = str(gui.purchaseAmountEntry.get())
                    purchaseAmount = float("-" + str(
                        re.sub('[A-Za-z@_!$%^#&*()<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", purchaseAmount,
                               count=len(purchaseAmount))
                    ))

                    # sort through provided 'purchaseTax' data
                    purchaseTax = str(gui.purchaseTaxEntry.get())
                    purchaseTax = float("-" + str(
                        re.sub('[A-Za-z@_!$%^#&*()<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", purchaseTax,
                               count=len(purchaseTax))
                    ))

                    # make 'purchaseCurrency' lowercase
                    purchaseCurrency = str(gui.purchaseCurrencyEntry.get()).lower()

                    # if 'employeeNameEntry' is blank, return none type
                    if (gui.employeeNameEntry.get() == None or gui.employeeNameEntry.get() == ''):
                        employeeName = None

                    # if 'employeeName' not blank, make contents lower case
                    else:
                        employeeName = str(gui.employeeNameEntry.get()).lower()

                    # make lowercase
                    establishmentNumAndStreet = str(gui.establishmentNumAndStreetEntry.get()).lower()
                    establishmentCity = str(gui.establishmentCityEntry.get()).lower()
                    establishmentState = str(gui.establishmentStateEntry.get()).lower()
                    establishmentZIP = int(gui.establishmentZIPEntry.get())
                    purchaseType = str(gui.purchaseTypeOption.get()).lower()
                    purchasePresent = True
                    purchaseCount = 1
                    purchaseTotal = purchaseAmount

                    transmitEnteredData(  # call 'transmitEnteredData' functionality from 'transmit_entered_data.py'
                        establishmentName, purchaseDate, purchaseTime, purchaseAmount, purchaseTax, purchaseCurrency,
                        employeeName, establishmentNumAndStreet, establishmentCity, establishmentState,
                        establishmentZIP,
                        purchaseType, purchasePresent, purchaseCount, purchaseTotal
                    )

                    gui.addDataPage()  # recursive call 'addDataPage' to reload the page

                    ##### 'enterDataStatusLabel' SUCCESS LABEL #####

                    gui.enterDataStatusLabel.configure(  # reconfigure enterDataStatusLabel to prompt fields
                        text="Data Uploaded",
                        text_color="#A5C9CA",
                    )

                except:  # if incorrect data present, throw enterDataButton error

                    ##### DISABLE 'enterDataButton' BUTTON #####

                    gui.enterDataButton.configure(  # reconfigure enterDataButton to 'disable'
                        text_color="#C6A49B",
                        fg_color="#5A3635",
                        hover_color="#18090D"
                    )

                    ##### 'enterDataStatusLabel' ERROR LABEL #####

                    gui.enterDataStatusLabel.configure(  # reconfigure enterDataStatusLabel to prompt fields
                        text="Faulty Input",
                        text_color="#5A3635",
                    )

            elif (  # if item makes money, let 'appendPurchaseAmount' and 'appendPurchaseTax' be positive
                    str(gui.purchaseTypeOption.get()) != 'salary' or
                    str(gui.purchaseTypeOption.get()) != 'investments' or
                    str(gui.purchaseTypeOption.get()) != 'gift'
            ):

                try: # if data present, grab data and convert it

                    # calculate 'purchaseDate'
                    purchaseDate = str(gui.purchaseYearOption.get()) + "/" + str(gui.purchaseMonthOption.get()) + "/" + str(
                        gui.purchaseDayOption.get())

                    establishmentName = str(gui.establishmentNameEntry.get()).lower()

                    # calculate 'purchaseTime'
                    if (gui.purchaseMeridiemOption.get() == "PM" and int(
                            gui.purchaseHourOption.get()) < 12):  # if meridiem 'PM', add 12 hours to 'purchaseHour'
                        purchaseHour = str(int(gui.purchaseHourOption.get()) + 12)

                    else:
                        purchaseHour = gui.purchaseHourOption.get()

                    purchaseTime = purchaseHour + ':' + gui.purchaseMinuteOption.get() + ':' + '00'

                    # sort through provided 'purchaseAmount' data
                    purchaseAmount = str(gui.purchaseAmountEntry.get())
                    purchaseAmount = float(
                        re.sub('[A-Za-z@_!$%^#&*()<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", purchaseAmount,
                               count=len(purchaseAmount))
                    )

                    # sort through provided 'purchaseTax' data
                    purchaseTax = str(gui.purchaseTaxEntry.get())
                    purchaseTax = float(
                        re.sub('[A-Za-z@_!$%^#&*()<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", purchaseTax,
                               count=len(purchaseTax))
                    )

                    # make 'purchaseCurrency' lowercase
                    purchaseCurrency = str(gui.purchaseCurrencyEntry.get()).lower()

                    # if 'employeeNameEntry' is blank, return none type
                    if (gui.employeeNameEntry.get() == None or gui.employeeNameEntry.get() == ''):
                        employeeName = None

                    # if 'employeeName' not blank, make contents lower case
                    else:
                        employeeName = str(gui.employeeNameEntry.get()).lower()

                    # make lowercase
                    establishmentNumAndStreet = str(gui.establishmentNumAndStreetEntry.get()).lower()
                    establishmentCity = str(gui.establishmentCityEntry.get()).lower()
                    establishmentState = str(gui.establishmentStateEntry.get()).lower()
                    establishmentZIP = int(gui.establishmentZIPEntry.get())
                    purchaseType = str(gui.purchaseTypeOption.get()).lower()
                    purchasePresent = True
                    purchaseCount = 1
                    purchaseTotal = purchaseAmount

                    transmitEnteredData( # call 'transmitEnteredData' functionality from 'transmit_entered_data.py'
                        establishmentName, purchaseDate, purchaseTime, purchaseAmount, purchaseTax, purchaseCurrency,
                        employeeName, establishmentNumAndStreet, establishmentCity, establishmentState, establishmentZIP,
                        purchaseType, purchasePresent, purchaseCount, purchaseTotal
                    )

                    gui.addDataPage()  # recursive call 'addDataPage' to reload the page

                    ##### 'enterDataStatusLabel' SUCCESS LABEL #####

                    gui.enterDataStatusLabel.configure(  # reconfigure enterDataStatusLabel to prompt fields
                        text="Data Uploaded",
                        text_color="#A5C9CA",
                    )

                except:  # if incorrect data present, throw enterDataButton error

                    ##### DISABLE 'enterDataButton' BUTTON #####

                    gui.enterDataButton.configure(  # reconfigure enterDataButton to 'disable'
                        text_color="#C6A49B",
                        fg_color="#5A3635",
                        hover_color="#18090D"
                    )

                    ##### 'enterDataStatusLabel' ERROR LABEL #####

                    gui.enterDataStatusLabel.configure(  # reconfigure enterDataStatusLabel to prompt fields
                        text="Faulty Input",
                        text_color="#5A3635",
                    )

        ##### REFRESH 'enterDataButton' BUTTON AND 'enterDataStatusLabel' LABEL IF UNSUCCESSFUL #####

        else: # if some but not all data entered (i.e. purchaseDateEntry and purchaseCurrencyEntry filled in but nothing else), throw enterDataButton error

            ##### DISABLE 'enterDataButton' BUTTON #####

            gui.enterDataButton.configure(  # reconfigure enterDataButton to 'disable'
                text_color="#C6A49B",
                fg_color="#5A3635",
                hover_color="#18090D"
            )

            ##### 'enterDataStatusLabel' ERROR LABEL #####

            gui.enterDataStatusLabel.configure(  # reconfigure enterDataStatusLabel to prompt fields
                text="Missing Fields",
                text_color="#5A3635",
            )



    ############### 'returnHomePage' FUNCTION ###############
    # The returnHomePage function is used to re-display the #
    #             home page of the application.             #
    #########################################################

    def returnHomePage(gui):

        ############### LABEL FUNCTIONALITY ###############
        # The point of the label functionality is to use  #
        #  the mentioned psycopg2 cursor in order to get  #
        #     the last entry date, as well as use the     #
        #   datetime library in order to get the current  #
        #                      date.                      #
        ###################################################

        ##### CURRENT DATE #####

        getCurrentDate = datetime.datetime.now().date()  # get the current date and assign contents to 'getCurrentDate'

        ##### LAST ENTRY #####

        receiptProjectCursor.execute(
            'select max(purchase_date) from base_fields_table')  # grab date of last entry from 'Receipt_Project_v3.0'

        getLastEntry = str(receiptProjectCursor.fetchall()[0][0])  # assign contents of SQL query to 'getLastEntry'

        ##### 'homePage' FRAME #####

        gui.homePage = ctk.CTkFrame( # construct 'homePage' frame
            master=gui,
            border_width=2,
            corner_radius=8,
            fg_color="#395B64",
            border_color="#395B64"
        )
        gui.homePage.grid(row=0, column=1, sticky="nswe", padx=20, pady=20) # align 'homePage' frame

        ##### 'homePage' GRID #####

        gui.homePage.rowconfigure((0, 1, 2, 3), weight=1)
        gui.homePage.rowconfigure(7, weight=10)
        gui.homePage.columnconfigure((0, 1), weight=1)
        gui.homePage.columnconfigure(2, weight=0)

        ##### 'graphLabel' LABEL IN 'homePage' #####

        gui.graphLabel = ctk.CTkLabel(  # construct 'graphLabel' label in 'homePage'
            master=gui.homePage,
            text="Last Quarter:",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.graphLabel.grid(row=0, column=0, columnspan=6, rowspan=1, pady=15, padx=10,
                            sticky="nsew")  # align 'graphLabel' label in 'homePage'

        ##### 'graphBox' FRAME IN 'homePage' #####

        gui.graphBox = ctk.CTkFrame(  # construct 'graphBox' frame in 'homePage' frame
            master=gui.homePage,
            border_width=2,
            corner_radius=8,
            border_color="#395B64"
        )
        gui.graphBox.grid(row=1, column=0, columnspan=6, rowspan=7, pady=0, padx=10,
                          sticky="nsew")  # align 'graphBox' frame in 'homePage'

        ##### 'graphBox' GRID IN 'homePage' #####

        gui.graphBox.rowconfigure(0, weight=1)  # configure 'graphBox' grid x axis
        gui.graphBox.columnconfigure(0, weight=1)  # configure 'graphBox' grid y axis

        ##### 'totalMovingAverageGraph' GRAPH IN 'graphBox' #####

        makeQuarterlyMovingAverage() # call 'makeQuarterlyMovingAverage' from 'make_quarterly_moving_average.py' for 'quarterlyMovingAverageGraph.png'

        gui.quarterlyMovingAverageGraphImage = ImageTk.PhotoImage( # create 'quarterlyMovingAverageGraphImage' image
            Image.open(
                '/Users/matthewbeck/Desktop/Projects/Receipt_Project_v3.0/quarterlyMovingAverageGraph.png'
            )
        )

        gui.quarterlyMovingAverageGraph = ctk.CTkLabel( # construct 'quarterlyMovingAverageGraph' graph in 'graphBox'
            master=gui.graphBox,
            image=gui.quarterlyMovingAverageGraphImage
        )
        gui.quarterlyMovingAverageGraph.quarterlyMovingAverageGraphImage = gui.quarterlyMovingAverageGraphImage # display 'quarterlyMovingAverageGraphImage' image
        gui.quarterlyMovingAverageGraph.grid(column=0, row=0, sticky="nwe", padx=15, pady=15) # align 'quarterlyMovingAverageGraph' graph in 'graphBox'

        ##### 'currentDateLabel' LABEL IN 'homePage' #####

        gui.currentDateLabel = ctk.CTkLabel(  # construct 'currentDateLabel' label in 'graphBox'
            master=gui.homePage,
            text="Current Date:",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.currentDateLabel.grid(row=8, column=0, columnspan=1, pady=10, padx=0,
                                  sticky="w")  # align 'currentDateLabel' label in 'graphBox' frame

        ##### 'currentDate' LABEL IN 'homePage' #####

        gui.currentDate = ctk.CTkLabel(  # construct 'currentDate' label in 'graphBox'
            master=gui.homePage,
            text=getCurrentDate,
            text_color="#E7F6F2"
        )
        gui.currentDate.grid(row=8, column=2, columnspan=1, pady=10, padx=0,
                             sticky="w")  # align 'currentDate' label in 'graphBox'

        ##### 'lastEntryLabel' LABEL IN 'homePage' #####

        gui.lastEntryLabel = ctk.CTkLabel(  # construct 'lastEntryLabel' label in 'homePage'
            master=gui.homePage,
            text="Last Entry:",
            text_color="#A5C9CA",
            text_font=("Roboto Medium", -15)
        )
        gui.lastEntryLabel.grid(row=8, column=3, columnspan=1, pady=10, padx=0,
                                sticky="e")  # align 'lastEntryLabel' label in 'homePage'

        ##### 'lastEntry' LABEL IN 'homePage' #####

        gui.lastEntry = ctk.CTkLabel( # construct 'lastEntry' label in 'homePage'
            master=gui.homePage,
            text=getLastEntry,
            text_color="#E7F6F2"
        )
        gui.lastEntry.grid(row=8, column=4, columnspan=1, pady=10, padx=0, sticky="e") # align 'lastEntry' label in 'homePage'

##### RUN THE GUI #####

if __name__ == "__main__":
    runApp = MainGUI()
    runApp.mainloop()