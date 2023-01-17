############### IMPORT NECESSARY RECOURSES ###############
#  Import psycopg2 in order to get needed functions to   #
#         establish link between Python and SQL.         #
##########################################################

import psycopg2 as pg2 # import psycopg2 to communicate with 'Receipt_Project_v3.0' database



############### 'transmitAppendedData' FUNCTION ###############
# The transmitAppendedData function takes information entered #
#  in home_page.py and updates Receipt_Project_v3.0 data in   #
#              accordance to provided parameters.             #
###############################################################

def transmitAppendedData (
    appendEstablishmentName, appendPurchaseTime, appendPurchaseAmount, appendPurchaseTax, appendPurchaseCurrency, appendEmployeeName,
    appendEstablishmentNumAndStreet, appendEstablishmentCity, appendEstablishmentState, appendEstablishmentZIP, appendPurchaseType,
    appendPurchaseTotal, appendPurchaseID
):



    ########## CREATE LINK BETWEEN PYTHON AND SQL SERVER ##########
    #  The following code is used to create a cursor in order to  #
    #    communicate with the 'Receipt_Project_v3.0' database.    #
    ###############################################################

    receipt_project = pg2.connect(  # connect python to 'Receipt_Project_v3.0' database
        host='localhost',
        database='Receipt_Project_v3.0',
        user='',
        password=''
    )
    receiptProjectCursor = receipt_project.cursor()  # create cursor to input commands

    #### UPDATE 'purchase_table' IN 'Receipt_Project_v3.0' #####

    receiptProjectCursor.execute( # update all contents of 'purchase_table' in 'Receipt_Project_v3.0'
        'update purchase_table set purchase_time = (%s), purchase_amount = (%s), purchase_tax = (%s), purchase_currency = (%s), purchase_type = (%s), employee_name = (%s) from purchase_table where purchase_id = (%s)',
        ((appendPurchaseTime), (appendPurchaseAmount), (appendPurchaseTax), (appendPurchaseCurrency), (appendPurchaseType), (appendEmployeeName), (appendPurchaseID),)
    )

    #### UPDATE 'location_table' IN 'Receipt_Project_v3.0' #####

    receiptProjectCursor.execute( # update all contents of 'location_table' in 'Receipt_Project_v3.0'
        'update location_table set establishment_name = (%s), establishment_address = (%s), establishment_city = (%s), establishment_region = (%s), establishment_zip = (%s) from location_table where purchase_id = (%s)',
        ((appendEstablishmentName), (appendEstablishmentNumAndStreet), (appendEstablishmentCity), (appendEstablishmentState), (appendEstablishmentZIP), (appendPurchaseID),)
    )



    ########## CLOSE CONNECTIONS ##########
    #      Close the connections to       #
    # 'Receipt_Project_v3.0' database in  #
    #     order to prevent data leaks.    #
    #######################################

    # IF THESE TWO COMMANDS BELOW CAUSE A PROBLEM, DELETE THEM

    receiptProjectCursor.close() # close the cursor to 'Receipt_Project_v3.0' database
    receipt_project.close() # close the connection to 'Receipt_Project_v3.0' database