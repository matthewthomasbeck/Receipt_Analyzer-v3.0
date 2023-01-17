############### IMPORT NECESSARY RECOURSES ###############
#  Import psycopg2 in order to get needed functions to   #
#         establish link between Python and SQL.         #
##########################################################

import psycopg2 as pg2 # import psycopg2 to communicate with 'Receipt_Project_v3.0' database



############### TRANSMIT DATA FUNCTIONALITY ###############
# The transmitEnteredData function is utilized within the #
# home_page.py central file and is used to transmit data  #
#   from the gui to the 'Receipt_Project_v3.0' database.  #
###########################################################

def transmitEnteredData (
    establishmentName, purchaseDate, purchaseTime, purchaseAmount, purchaseTax, purchaseCurrency, employeeName,
    establishmentNumAndStreet, establishmentCity, establishmentState, establishmentZIP, purchaseType, purchasePresent,
    purchaseCount, purchaseTotal
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



    ########## FILL NEW FIELDS FUNCTIONALITY ##########
    #  The fillNewFields function is used to transmit #
    #    information to the 'Receipt_Project_v3.0'    #
    # database in the case that there is no duplicate #
    #                      dates.                     #
    ###################################################

    def fillNewFields(): # function to fill fields provided no duplicate 'purchase_date' found

        ##### FILL 'purchase_date', 'purchase_present', 'purchase_count' #####

        receiptProjectCursor.execute( # insert new 'purchaseDate' into 'Receipt_Project_v3.0' database
            'insert into base_fields_table(purchase_date, purchase_present, purchase_count, total_spent) values (%s, %s, %s, %s)',
            (purchaseDate, purchasePresent, purchaseCount, purchaseTotal)
        )
        receipt_project.commit() # submit query to 'Receipt_Project_v3.0'

        ##### GRAB 'day_id' FROM 'base_fields_table' #####

        receiptProjectCursor.execute( # select 'day_id' correlated with 'purchase_date' and store into 'dayID'
            'select day_id from base_fields_table where purchase_date = (%s)',
            ((purchaseDate,))  # <---- this one tuple brought me so much pain :)
        )
        dayID = str(receiptProjectCursor.fetchall()[0][0]) # assign contents to 'dayID'

        ##### FILL 'day_id' IN 'purchase_table' #####

        receiptProjectCursor.execute( # create new 'day_id' in 'purchase_table' based on 'dayID'
            'insert into purchase_table(day_id) values (%s)',
            ((dayID),)
        )
        receipt_project.commit() # submit query to 'Receipt_Project_v3.0'

        ##### FILL 'purchase_time', 'purchase_amount', 'purchase_tax', 'purchase_currency', 'purchase_type', 'employee_name' INTO 'purchase_table' #####

        receiptProjectCursor.execute( # insert new 'purchaseTime', 'purchaseAmount', 'purchaseTax', 'purchaseCurrency', 'purchaseType', 'employeeName' into 'Receipt_Project_v3.0' database
            'update purchase_table set purchase_time = (%s), purchase_amount = (%s), purchase_tax = (%s), purchase_currency = (%s), purchase_type = (%s), employee_name = (%s) where day_id = (%s)',
            (purchaseTime, purchaseAmount, purchaseTax, purchaseCurrency, purchaseType, employeeName,
             dayID)
        )
        receipt_project.commit()  # submit query to 'Receipt_Project_v3.0'

        ##### GRAB 'purchase_id' FROM 'purchase_table' #####

        receiptProjectCursor.execute( # select 'purchase_id' correlated with 'day_id' and store into 'purchaseID'
            'select purchase_id from purchase_table where day_id = (%s)',
            ((dayID),)
        )
        purchaseID = str(receiptProjectCursor.fetchall()[0][0]) # assign contents to 'purchaseID'

        ##### FILL 'day_id' AND 'purchase_id' INTO 'location_table' #####

        receiptProjectCursor.execute( # create new 'purchase_table' day id based on 'dayID'
            'insert into location_table(day_id, purchase_id) values (%s, %s)',
            (dayID, purchaseID)
        )
        receipt_project.commit() # submit query to 'Receipt_Project_v3.0'

        ##### FILL 'establishment_name', 'establishment_address', 'establishment_city', 'establishment_region', 'establishment_zip' INTO 'location_table' #####

        receiptProjectCursor.execute( # insert new 'establishmentName', 'establishmentNumAndStreet', 'establishmentCity', 'establishmentState', 'establishmentZIP' into 'Receipt_Project_v3.0' database
            'update location_table set establishment_name = (%s), establishment_address = (%s), establishment_city = (%s), establishment_region = (%s), establishment_zip = (%s) where purchase_id = (%s)',
            (establishmentName, establishmentNumAndStreet, establishmentCity, establishmentState, establishmentZIP, purchaseID)
        )
        receipt_project.commit() # submit query to 'Receipt_Project_v3.0'



    ########## IF DATA DETECTED ##########
    #    If the 'Receipt_Project_v3.0'   #
    #   database is not empty, proceed.  #
    ######################################

    if (purchasePresent == True): # if all fields correctly filled in, transmit data to 'Receipt_Project_v3.0'

        ##### ATTEMPT TO FIND DATE DUPLICATES #####

        try: # try to create a list of all dates

            ##### ALTER 'purchaseDate' TO COMPARE WITH 'allDates' VALUES #####

            receiptProjectCursor.execute( # grab list of all dates in 'Receipt_Project_v3.0' database
                'select purchase_date from base_fields_table where extract(year from purchase_date) = (%s)',
                ((purchaseDate.split('/')[0]),)
            )
            allDates = str(receiptProjectCursor.fetchall()) # assign contents to 'allDates'

            if (purchaseDate.split('/')[1][0] == '0'):  # if month date begins with 0, remove 0
                monthDate = purchaseDate.split('/')[1][1]  # store value into 'monthDate'

            elif (purchaseDate.split('/')[1][0] != '0'):  # if month date does not begin with 0, change nothing
                monthDate = purchaseDate.split('/')[1]  # store value into 'monthDate'

            if (purchaseDate.split('/')[2][0] == '0'):  # if day date begins with 0, remove 0
                dayDate = purchaseDate.split('/')[2][1]  # store value into 'dayDate'

            elif (purchaseDate.split('/')[2][0] != '0'):  # if day date does not begin with 0, change nothing
                dayDate = purchaseDate.split('/')[2]  # store value into 'dayDate'

            compareDate = str( # concatenate 'purchaseDate' values to make a comparison date
                '(datetime.date(' + purchaseDate.split('/')[0] + ', ' + monthDate + ', ' + dayDate + '),)'
            )



            ########## IF 'compareDate' IN 'allDates' ##########
            #  If there is a past instance of a date, proceed. #
            ####################################################

            if (compareDate in allDates): # if not first instance of 'purchaseDate'

                ##### UPDATE 'purchase_count' IN 'base_fields_table' #####

                receiptProjectCursor.execute( # find previous 'purchase_count', index by +1, and store into 'purchaseCount'
                    'select purchase_count from base_fields_table where purchase_date = (%s)',
                    ((purchaseDate,))
                )
                purchaseCount = str(int(receiptProjectCursor.fetchall()[0][0]) + 1) # assign contents to 'purchaseCount'

                receiptProjectCursor.execute( # update 'purchase_count' if 'purchase_date' day already has a purchase
                    'update base_fields_table set purchase_count = (%s) where purchase_date = (%s)',
                    (purchaseCount, (purchaseDate,))
                )
                receipt_project.commit() # submit query to 'Receipt_Project_v3.0'

                ##### GRAB ID FROM 'base_fields_table' #####

                receiptProjectCursor.execute( # select 'day_id' correlated with 'purchase_date' and store into 'dayID'
                    'select day_id from base_fields_table where purchase_date = (%s)',
                    ((purchaseDate,))
                )
                dayID = str(receiptProjectCursor.fetchall()[0][0]) # assign contents to 'dayID'

                ##### FILL 'day_id' IN 'purchase_table' #####

                receiptProjectCursor.execute( # create new 'purchase_table' day id based on 'dayID'
                    'insert into purchase_table(day_id) values (%s)',
                    ((dayID),)
                )
                receipt_project.commit() # submit query to 'Receipt_Project_v3.0'

                ##### GRAB ID FROM 'purchase_table' #####

                receiptProjectCursor.execute( # select 'day_id' correlated with 'purchase_date' and store into 'dayID'
                    'select max(purchase_id) from purchase_table where day_id = (%s)',
                    ((dayID),)
                )
                purchaseID = str(receiptProjectCursor.fetchall()[0][0]) # assign contents to 'purchaseID'

                ##### FILL 'purchase_time', 'purchase_amount', 'purchase_tax', 'purchase_currency', 'purchase_type', 'employee_name' INTO 'purchase_table' #####

                receiptProjectCursor.execute( # insert 'purchaseTime' into 'Receipt_Project_v3.0' database
                    'update purchase_table set purchase_time = (%s), purchase_amount = (%s), purchase_tax = (%s), purchase_currency = (%s), purchase_type = (%s), employee_name = (%s) where purchase_id = (%s)',
                    (purchaseTime, purchaseAmount, purchaseTax, purchaseCurrency, purchaseType, employeeName,
                     purchaseID)
                )
                receipt_project.commit() # submit query to 'Receipt_Project_v3.0'

                ##### FILL 'day_id' AND 'purchase_id' INTO 'location_table' #####

                receiptProjectCursor.execute( # create new 'purchase_table' day id based on 'dayID'
                    'insert into location_table(day_id, purchase_id) values (%s, %s)',
                    (dayID, purchaseID)
                )
                receipt_project.commit() # submit query to 'Receipt_Project_v3.0'

                ##### FILL 'establishment_name', 'establishment_address', 'establishment_city', 'establishment_region', 'establishment_zip' INTO 'location_table' #####

                receiptProjectCursor.execute( # insert 'establishmentName' into 'Receipt_Project_v3.0' database
                    'update location_table set establishment_name = (%s), establishment_address = (%s), establishment_city = (%s), establishment_region = (%s), establishment_zip = (%s) where purchase_id = (%s)',
                    (establishmentName, establishmentNumAndStreet, establishmentCity, establishmentState, establishmentZIP, purchaseID)
                )
                receipt_project.commit() # submit query to 'Receipt_Project_v3.0'

                ##### GRAB 'total_spent' FROM 'base_fields_table' AND UPDATE 'total_spent' #####

                receiptProjectCursor.execute( # select 'day_id' correlated with 'purchase_date' and store into 'dayID'
                    'select total_spent from base_fields_table where day_id = (%s)',
                    ((dayID),)
                )
                oldTotal = receiptProjectCursor.fetchall()[0][0] # assign contents to 'oldTotal'
                newTotal = float(purchaseAmount) + float(oldTotal) # assign contents to 'newTotal'

                receiptProjectCursor.execute( # assign value of 'newTotal' to 'total_spent' in 'base_fields_table'
                    'update base_fields_table set total_spent = (%s) where day_id = (%s)',
                    (newTotal, dayID)
                )
                receipt_project.commit() # submit query to 'Receipt_Project_v3.0'

                ##### FILL 'establishment_name', 'establishment_address', 'establishment_city', 'establishment_region', 'establishment_zip' INTO 'location_table' #####

                receiptProjectCursor.execute( # insert 'establishmentName' into 'Receipt_Project_v3.0' database
                    'update location_table set establishment_name = (%s), establishment_address = (%s), establishment_city = (%s), establishment_region = (%s), establishment_zip = (%s) where purchase_id = (%s)',
                    (establishmentName, establishmentNumAndStreet, establishmentCity, establishmentState, establishmentZIP, purchaseID)
                )
                receipt_project.commit() # submit query to 'Receipt_Project_v3.0'




            ########## IF 'compareDate' NOT IN 'allDates' ##########
            #     If no past instance of a date found, proceed.    #
            ########################################################

            else: # if first instance of 'purchaseDate'

                fillNewFields() # call 'fillNewFields' function provided no duplicate 'purchase_date'



        ########## IF NO DATA DETECTED ##########
        #     If the 'Receipt_Project_v3.0'     #
        #      database is empty, proceed.      #
        #########################################

        except: # if list failure (no data found), 'purchase_date' duplicates impossible

            fillNewFields() # call 'fillNewFields' function  provided no duplicate 'purchase_date'




    ########## IF ENTERED DATA EMPTY ##########
    #  If day entered in home_page.py has no  #
    #              data, proceed.             #
    ###########################################

    elif (purchasePresent == False):

        ##### FILL 'purchase_date', 'purchase_present', 'purchase_count' #####

        receiptProjectCursor.execute( # insert new 'purchaseDate' into 'Receipt_Project_v3.0' database
            'insert into base_fields_table(purchase_date, purchase_present, purchase_count, total_spent) values (%s, %s, %s, %s)',
            (purchaseDate, False, None, None)
        )
        receipt_project.commit() # submit query to 'Receipt_Project_v3.0'



    ########## CLOSE CONNECTIONS ##########
    #      Close the connections to       #
    # 'Receipt_Project_v3.0' database in  #
    #     order to prevent data leaks.    #
    #######################################

    # IF THESE TWO COMMANDS BELOW CAUSE A PROBLEM, DELETE THEM

    receiptProjectCursor.close() # close the cursor to 'Receipt_Project_v3.0' database
    receipt_project.close() # close the connection to 'Receipt_Project_v3.0' database