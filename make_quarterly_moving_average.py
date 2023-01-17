############### IMPORT NECESSARY RECOURSES ###############
#  Throughout this document, several libraries are used  #
# in order to import necessary functions to make graphs, #
#         communicate with SQL, and filter data.         #
##########################################################

import psycopg2 as pg2 # import psycopg2 to communicate with 'Receipt_Project_v3.0' database
import matplotlib.pyplot as plt # import matplotlib to display data
import numpy as np # import numpy to restructure data
import re # import re regular expressions for data filter
import seaborn as sns # import seaborn for graph styles
import os # import os to delete past graph images



############### IMPORT DATA FROM 'Receipt_Project_v3.0' ###############
#     In order to 'decongest' the file, all data relevant to the      #
#        different plots will be declared as global variables.        #
#######################################################################

##### CREATE LINK BETWEEN PYTHON AND SQL SERVER #####

receipt_project = pg2.connect( # connect python to 'Receipt_Project_v3.0' database
    host='localhost',
    database='Receipt_Project_v3.0',
    user='',
    password=''
)
receiptProjectCursor = receipt_project.cursor() # create cursor to input commands

##### GRAB 'total_spent' FROM 'Receipt_Project_v3.0' #####

receiptProjectCursor.execute( # grab 'total_spent' from 'base_fields_table' for data set
    'select total_spent from base_fields_table order by purchase_date'
)
purchaseTotals = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'purchaseTotals'

##### RESTRUCTURE 'purchaseTotals' ARRAY #####

for i in range(len(purchaseTotals)): # restructure 'purchaseTotals' to remove null values and special characters

    if (purchaseTotals[i] == None): # replace null values with 0
        purchaseTotals[i] = 0

    else: # pass for all non-null values
        pass

    purchaseTotals[i] = float(re.sub( # filter 'purchaseTotals' to remove special characters
        '[@_!$%^#&*()<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(purchaseTotals[i]),
        count=len(str(purchaseTotals[i]))
    ))

##### CLOSE CONNECTION TO 'Receipt_Project_v3.0' #####

receiptProjectCursor.close() # stop communication with 'Receipt_Project_v3.0' database
receipt_project.close() # close the connection to prevent data leaks



############### 'makeMovingAverage' FUNCTION ###############
#    The makeMovingAverage function is used to create a    #
#       moving average based on provided parameters.       #
############################################################

def makeMovingAverage(x, w):

    return np.convolve(x, np.ones(w), 'same') / w # return moving average



############### 'makeQuarterlyMovingAverage' FUNCTION ###############
#  The makeQuarterlyMovingAverage function creates a model that is  #
#   used to analyze how average daily spending has changed in the   #
#                             past year.                            #
#####################################################################

def makeQuarterlyMovingAverage():

    ##### CREATE 'quarterlyMovingAverageGraph' RESOURCES #####

    quarterlyTotals = purchaseTotals[-90:] # grab last 90 days of data from 'purchaseTotals'

    quarterlyMovingAverage = makeMovingAverage(quarterlyTotals, int(np.sqrt(len(quarterlyTotals))) * 2) # create 'quarterlyMovingAverage'

    quarterlyMovingAverageIndex = [] # create empty array as 'quarterlyMovingAverageIndex' index

    for i in range(len(quarterlyMovingAverage)): # fill empty array to length of 'quarterlyMovingAverage'
        quarterlyMovingAverageIndex.append(i + 1)

    quarterlyMovingAverageTrend = makeMovingAverage(quarterlyMovingAverage, int(np.sqrt(len(quarterlyMovingAverage))) * 4) # create 'quarterlyMovingAverageTrend'

    quarterlyAverage = " Rolling Average Trend:"

    ##### PLOT 'quarterlyMovingAverageGraph' GRAPH #####

    sns.set( # configure 'quarterlyMovingAverageGraph' graph
        rc={'axes.facecolor': '#292D2E', 'figure.facecolor': '#292D2E', 'grid.color': '#395B64',
            'axes.edgecolor': '#292D2E', 'text.color': '#A5C9CA', 'xtick.color': '#A5C9CA',
            'ytick.color': '#A5C9CA', 'figure.figsize':(5.5, 3.5)}
    )

    quarterlyMovingAverageGraph = sns.lineplot( # create 'quarterlyMovingAverageGraph' average line
        quarterlyMovingAverageIndex, quarterlyMovingAverage, color='#A5C9CA'
    ).set(title=quarterlyAverage)

    quarterlyMovingAverageGraph = sns.lineplot( # create 'quarterlyMovingAverageGraph' trend line
        quarterlyMovingAverageIndex, quarterlyMovingAverageTrend, color='#E7F6F2'
    )

    if ( # if 'quarterlyMovingAverage' negative, proceed

        (round(float(re.sub(
            '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(quarterlyMovingAverage[-1:]),
            count=len(str(quarterlyMovingAverage))
        )), 2)) < 0
    ):

        quarterlyMovingAverageGraph.annotate( # annotate 'quarterlyMovingAverage' line
            xy=(max(quarterlyMovingAverageIndex), quarterlyMovingAverage[-1:]), text=("-$" + str(-1 * (round(float(re.sub(
            '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(quarterlyMovingAverage[-1:]),
            count=len(str(quarterlyMovingAverage))
            )), 2)))),
            color='#A5C9CA', size=8
        )

    else: # if 'quarterlyMovingAverage' positive, proceed

        quarterlyMovingAverageGraph.annotate( # annotate 'quarterlyMovingAverage' line
            xy=(max(quarterlyMovingAverageIndex), quarterlyMovingAverage[-1:]), text=("$" + str(round(float(re.sub(
            '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(quarterlyMovingAverage[-1:]),
            count=len(str(quarterlyMovingAverage))
            )), 2))),
            color='#A5C9CA', size=8
        )

    if ( # if 'quarterlyMovingAverageTrend' negative, proceed

        (round(float(re.sub(
            '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(quarterlyMovingAverageTrend[-1:]),
            count=len(str(quarterlyMovingAverageTrend))
        )), 2)) < 0
    ):

        quarterlyMovingAverageGraph.annotate( # annotate 'quarterlyMovingAverageTrend' line
            xy=(max(quarterlyMovingAverageIndex), quarterlyMovingAverageTrend[-1:]), text=("-$" + str(-1 * (round(float(re.sub(
            '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(quarterlyMovingAverageTrend[-1:]),
            count=len(str(quarterlyMovingAverageTrend))
            )), 2)))),
            color='#E7F6F2', size=8
        )

    else: # if 'quarterlyMovingAverageTrend' positive, proceed

        quarterlyMovingAverageGraph.annotate( # annotate 'quarterlyMovingAverageTrend' line
            xy=(max(quarterlyMovingAverageIndex), quarterlyMovingAverageTrend[-1:]), text=("$" + str(round(float(re.sub(
            '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(quarterlyMovingAverageTrend[-1:]),
            count=len(str(quarterlyMovingAverageTrend))
            )), 2))),
            color='#E7F6F2', size=8
        )

    plt.legend( # create legend
        labels=["Avg.", "Trend"],
        fontsize=8,
        loc='upper left'
    )

    ##### SAVE 'quarterlyMovingAverageGraph.png' FILE #####

    if os.path.exists('/Users/matthewbeck/Desktop/Projects/Receipt_Project_v3.0/quarterlyMovingAverageGraph.png'): # if file path exists, delete 'quarterlyMovingAverageGraph.png'
        os.remove('/Users/matthewbeck/Desktop/Projects/Receipt_Project_v3.0/quarterlyMovingAverageGraph.png')

    else:  # if file path does not exist, pass
        pass

    plt.savefig('/Users/matthewbeck/Desktop/Projects/Receipt_Project_v3.0/quarterlyMovingAverageGraph.png')  # save 'quarterlyMovingAverageGraph' graph as 'quarterlyMovingAverageGraph.png'

    plt.cla() # clear 'quarterlyMovingAverageGraph' when complete