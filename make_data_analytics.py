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



############### 'makeMovingAverage' FUNCTION ###############
#    The makeMovingAverage function is used to create a    #
#       moving average based on provided parameters.       #
############################################################

def makeMovingAverage(x, w):

    return np.convolve(x, np.ones(w), 'same') / w # return moving average



############### 'restructureData' FUNCTION ###############
# The restructureData function is used to 'clean up' the #
#  various arrays made before using them to make graphs  #
#                   for 'home_page.py'.                  #
##########################################################

def restructureData(array, period):

    for i in range(len(array)):  # restructure 'array' to remove null values and special characters

        if (array[i] == None):  # replace null values with 0
            array[i] = 0

        else:  # pass for all non-null values
            pass

        try: # if array numeric, proceed

            array[i] = float(re.sub( # filter 'array' to remove special characters
                '[@_!$%^#&*()<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(array[i]),
                count=len(str(array[i]))
            ))

        except: # if array alphanumeric, proceed

            pass

    if (period == 0): # shorten or keep array length the same based on 'period' from 'home_page.py'

        array = array[-0:]

    elif (period == 365):

        array = array[-365:]

    elif (period == 90):

        array = array[-90:]

    elif (period == 30):

        array = array[-30:]

    return array # return restructured 'array'



############### 'createDataAnalytics' FUNCTION ###############
#     The createDataAnalytics function is used to create     #
#  customized matplotlib graphs based on provided criterion  #
#                    from 'home_page.py'.                    #
##############################################################

def makeDataAnalytics(period, compareOne, compareTwo, compareType):



    ########## CREATE LINK BETWEEN PYTHON AND SQL SERVER ##########
    #   In order to communicate with the 'Receipt_Project_v3.0'   #
    #             server, a link must be established.             #
    ###############################################################

    receipt_project = pg2.connect(  # connect python to 'Receipt_Project_v3.0' database
        host='localhost',
        database='Receipt_Project_v3.0',
        user='',
        password=''
    )
    receiptProjectCursor = receipt_project.cursor()  # create cursor to input commands



    ########## SORT THROUGH PARAMETERS FROM 'home_page.py' ##########
    #   Below is the code that determines what data will be shown,  #
    #  and if that data will be compared with other data findings   #
    #        based on parameters provided by 'home_page.py'.        #
    #################################################################

    ##### SORT THROUGH 'period' FROM 'home_page.py' #####

    if (period == "annual"): # if 'annual', limit 'analysisData' array to last 365 values

        period = 365

    elif (period == "quarterly"): # if 'quarterly', limit 'analysisData' array to last 90 values

        period = 90

    elif (period == "month"): # if 'month', limit 'analysisData' array to last 30 values

        period = 30

    elif (period == 'total'): # if 'total', do not restrict 'analysisData'

        period = 0

    ##### IF 'compareOne' LOCATION-BASED #####

    if (compareOne == "location" or compareOne == "city" or compareOne == "state"): # if 'type' is location-based, proceed

        ##### CALCULATE 'location' #####

        if (compareOne == "location"): # if 'compareOne == 'location'', proceed

            ##### FIND 'dayList' DAYS IN 'location' #####

            if (period != 0): # if period not 'total', limit data

                receiptProjectCursor.execute(
                    'select day_id from base_fields_table order by day_id desc limit (%s)',
                    ((period,))
                )
                dayList = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'dayList'

            else: # if period 'total', do not limit data

                receiptProjectCursor.execute(
                    'select day_id from base_fields_table order by day_id desc'
                )
                dayList = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'dayList'

            ##### FIND TOTAL 'dayList' NAMES AND 'purchase_id' IN 'location' #####

            visitList = [] # create 'visitList' array

            nameList = [] # create 'nameList' array

            for i in range(len(dayList)):

                dayList[i] = re.sub( # restructure 'dayList'
                    '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(dayList[i]),
                    count=len(str(dayList[i]))
                )

                receiptProjectCursor.execute( # find number of purchases based on 'dayList'
                    'select count(purchase_id) from purchase_table where day_id = (%s)',
                    ((dayList[i]),)
                )
                loopCount = receiptProjectCursor.fetchall() # store contents in 'loopCount'

                loopCount = int(re.sub( # restructure 'loopCount'
                    '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§,«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(loopCount),
                    count=len(str(loopCount))
                ))

                for j in range(loopCount):

                    visitList.append(len(visitList) + 1) # fill 'visitList'

                    nameList.append(len(nameList) + 1) # fill 'nameList'

                    receiptProjectCursor.execute( # find 'purchase_id' based on 'dayList' and 'loopCount'
                        'select purchase_id from purchase_table where day_id = (%s) order by purchase_id offset (%s) limit 1',
                        ((dayList[i]), (j),)
                    )
                    visitList[len(visitList) - 1] = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'visitList'

                    visitList[len(visitList) - 1] = re.sub( # restructure 'visitList'
                        '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(visitList[len(visitList) - 1]),
                        count=len(str(visitList[len(visitList) - 1]))
                    )

                    receiptProjectCursor.execute( # find names based on 'visitList'
                        'select establishment_name from location_table where purchase_id = (%s)',
                        ((visitList[len(visitList) - 1]),)
                    )
                    nameList[len(nameList) - 1] = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'nameList'

            nameList = restructureData(nameList, period) # restructure 'nameList' array

            ##### CALCULATE FINAL 'newNameList' AND 'newVisitList' IN 'location' #####

            for i in range(len(nameList)):

                k = 0 # set 'key' value

                for j in range(len(nameList)):

                    if (nameList[i] != nameList[j]): # if name duplicate not found, pass

                        pass

                    elif (nameList[i] == nameList[j]): # if name duplicate found, proceed

                        if (nameList[i] == nameList[j] and k == 0): # if name duplicate and 'key' unchanged, proceed

                            k = 1 # change 'key' value

                        elif (nameList[i] == nameList[j] and k == 1): # if name duplicate and 'key' changed, remove value

                            visitList[j] = 0

                k = 0 # reset 'key' value

            visitList = [x for x in visitList if not isinstance(x, int)] # remove all integers in 'visitList'

            newNameList = [] # declare 'newNameList' array

            dayList = [] # empty 'dayList' array

            for i in range(len(visitList)):

                newNameList.append(i) # fill 'newNameList' array

                dayList.append(0) # fill 'dayList' array

                receiptProjectCursor.execute( # grab names based on 'visitList'
                    'select establishment_name from location_table where purchase_id = (%s)',
                    ((visitList[i]),)
                )
                newNameList[i] = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'newNameList'

            for i in range(len(newNameList)):

                for j in range(len(nameList)):

                    if (newNameList[i] == nameList[j]): # if name in 'newNameList' duplicate, add to visit value

                        dayList[i] = dayList[i] + 1

                    else:

                        pass

                newNameList[i] = re.sub( # restructure 'newNameList'
                    '[@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(newNameList[i]),
                    count=len(str(newNameList[i]))
                )

                if (len(newNameList[i].split(" ")) > 1): # if 'newNameList' parts more than 1, split 'newNameList'

                    newName = newNameList[i].split(" ")

                    for j in range(len(newName)):

                        if (j == len(newName) - 1): # if 'newName' part last part, proceed

                            if (len(newName[j]) > 5): # if name longer than 5, take only first 5 characters

                                newName[j] = str(newName[j][0:5]) + "."

                            else: # if name not longer than 5, pass

                                pass

                        else: # reduce 'newName' part to first letter capitalized with period

                            newName[j] = str(newName[j][0]) + "."

                    newNameList[i] = ' '.join(newName) # rejoin 'newName' into 'newNameList'

                else: # if 'newNameList' parts only 1, proceed

                    if (len(newNameList[i]) >= 7): # if 'newNameList' length longer than 7, take only first 6 characters

                        newNameList[i] = str(newNameList[i][0:6]) + "."

                    else: # if 'newNameList' length not longer than 7, pass

                        pass

                dayList[i] = int(re.sub( # restructure 'dayList'
                    '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(dayList[i]),
                    count=len(str(dayList[i]))
                ))

            nameList = newNameList # set 'newNameList' contents to 'nameList'

            visitList = dayList # set 'dayList' contents to 'visitList'

            ##### LIMIT 'newNameList' AND 'newVisitList' IN 'location' #####

            newNameList = [] # empty 'newNameList' array

            newVisitList = [] # empty 'newVisitList' array

            for i in range(len(nameList)):

                if (visitList[i] >= (int((sum(visitList) ** 0.5))) / 2.5): # if value in 'visitList' greater than total sum squared divided by 2, fill 'newVisitList' and 'newNameList'

                    newVisitList.append(visitList[i])

                    newNameList.append(nameList[i].title())

                else: # if value in 'visitList' less than total sum squared divided by 2, pass

                    pass

        ##### CALCULATE 'city' #####

        elif (compareOne == "city"): # if 'compareOne == 'city'', proceed

            ##### FIND 'dayList' DAYS IN 'city' #####

            if (period != 0): # if period not 'total', limit data

                receiptProjectCursor.execute(
                    'select day_id from base_fields_table order by day_id desc limit (%s)',
                    ((period,))
                )
                dayList = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'dayList'

            else: # if period 'total', do not limit data

                receiptProjectCursor.execute(
                    'select day_id from base_fields_table order by day_id desc'
                )
                dayList = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'dayList'

            ##### FIND TOTAL 'dayList' NAMES AND 'purchase_id' IN 'city' #####

            visitList = [] # create 'visitList' array

            nameList = [] # create 'nameList' array

            for i in range(len(dayList)):

                dayList[i] = re.sub( # restructure 'dayList'
                    '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(dayList[i]),
                    count=len(str(dayList[i]))
                )

                receiptProjectCursor.execute( # find number of purchases based on 'dayList'
                    'select count(purchase_id) from purchase_table where day_id = (%s)',
                    ((dayList[i]),)
                )
                loopCount = receiptProjectCursor.fetchall() # store contents in 'loopCount'

                loopCount = int(re.sub( # restructure 'loopCount'
                    '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§,«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(loopCount),
                    count=len(str(loopCount))
                ))

                for j in range(loopCount):

                    visitList.append(len(visitList) + 1) # fill 'visitList'

                    nameList.append(len(nameList) + 1) # fill 'nameList'

                    receiptProjectCursor.execute( # find 'purchase_id' based on 'dayList' and 'loopCount'
                        'select purchase_id from purchase_table where day_id = (%s) order by purchase_id offset (%s) limit 1',
                        ((dayList[i]), (j),)
                    )
                    visitList[len(visitList) - 1] = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'visitList'

                    visitList[len(visitList) - 1] = re.sub( # restructure 'visitList'
                        '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(visitList[len(visitList) - 1]),
                        count=len(str(visitList[len(visitList) - 1]))
                    )

                    receiptProjectCursor.execute( # find names based on 'visitList'
                        'select establishment_city from location_table where purchase_id = (%s)',
                        ((visitList[len(visitList) - 1]),)
                    )
                    nameList[len(nameList) - 1] = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'nameList'

            nameList = restructureData(nameList, period) # restructure 'nameList' array

            ##### CALCULATE FINAL 'newNameList' AND 'newVisitList' IN 'city' #####

            for i in range(len(nameList)):

                k = 0 # set 'key' value

                for j in range(len(nameList)):

                    if (nameList[i] != nameList[j]): # if name duplicate not found, pass

                        pass

                    elif (nameList[i] == nameList[j]): # if name duplicate found, proceed

                        if (nameList[i] == nameList[j] and k == 0): # if name duplicate and 'key' unchanged, proceed

                            k = 1 # change 'key' value

                        elif (nameList[i] == nameList[j] and k == 1): # if name duplicate and 'key' changed, remove value

                            visitList[j] = 0

                k = 0 # reset 'key' value

            visitList = [x for x in visitList if not isinstance(x, int)] # remove all integers in 'visitList'

            newNameList = [] # declare 'newNameList' array

            dayList = [] # empty 'dayList' array

            for i in range(len(visitList)):

                newNameList.append(i) # fill 'newNameList' array

                dayList.append(0) # fill 'dayList' array

                receiptProjectCursor.execute( # grab names based on 'visitList'
                    'select establishment_city from location_table where purchase_id = (%s)',
                    ((visitList[i]),)
                )
                newNameList[i] = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'newNameList'

            for i in range(len(newNameList)):

                for j in range(len(nameList)):

                    if (newNameList[i] == nameList[j]): # if name in 'newNameList' duplicate, add to visit value

                        dayList[i] = dayList[i] + 1

                    else:

                        pass

                newNameList[i] = re.sub( # restructure 'newNameList'
                    '[@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(newNameList[i]),
                    count=len(str(newNameList[i]))
                )

                if (len(newNameList[i].split(" ")) > 1): # if 'newNameList' parts more than 1, split 'newNameList'

                    newName = newNameList[i].split(" ")

                    for j in range(len(newName)):

                        if (j == len(newName) - 1): # if 'newName' part last part, proceed

                            if (len(newName[j]) > 5): # if name longer than 5, take only first 5 characters

                                newName[j] = str(newName[j][0:5]) + "."

                            else: # if name not longer than 5, pass

                                pass

                        else: # reduce 'newName' part to first letter capitalized with period

                            newName[j] = str(newName[j][0]) + "."

                    newNameList[i] = ' '.join(newName) # rejoin 'newName' into 'newNameList'

                else: # if 'newNameList' parts only 1, proceed

                    if (len(newNameList[i]) >= 7): # if 'newNameList' length longer than 7, take only first 6 characters

                        newNameList[i] = str(newNameList[i][0:6]) + "."

                    else: # if 'newNameList' length not longer than 7, pass

                        pass

                dayList[i] = int(re.sub( # restructure 'dayList'
                    '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(dayList[i]),
                    count=len(str(dayList[i]))
                ))

            nameList = newNameList # set 'newNameList' contents to 'nameList'

            visitList = dayList # set 'dayList' contents to 'visitList'

            ##### LIMIT 'newNameList' AND 'newVisitList' IN 'city' #####

            newNameList = [] # empty 'newNameList' array

            newVisitList = [] # empty 'newVisitList' array

            for i in range(len(nameList)):

                if (visitList[i] >= (int((sum(visitList) ** 0.5))) / 6.5): # if value in 'visitList' greater than total sum squared divided by 6.5, fill 'newVisitList' and 'newNameList'

                    newVisitList.append(visitList[i])

                    newNameList.append(nameList[i].title())

                else: # if value in 'visitList' less than total sum squared divided by 6.5, pass

                    pass

        ##### CALCULATE 'state' #####

        else: # if 'compareOne == 'state'', proceed

            ##### FIND 'dayList' DAYS IN 'state' #####

            if (period != 0): # if period not 'total', limit data

                receiptProjectCursor.execute(
                    'select day_id from base_fields_table order by day_id desc limit (%s)',
                    ((period,))
                )
                dayList = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'dayList'

            else: # if period 'total', do not limit data

                receiptProjectCursor.execute(
                    'select day_id from base_fields_table order by day_id desc'
                )
                dayList = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'dayList'

            ##### FIND TOTAL 'dayList' NAMES AND 'purchase_id' IN 'state' #####

            visitList = [] # create 'visitList' array

            nameList = [] # create 'nameList' array

            for i in range(len(dayList)):

                dayList[i] = re.sub( # restructure 'dayList'
                    '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(dayList[i]),
                    count=len(str(dayList[i]))
                )

                receiptProjectCursor.execute( # find number of purchases based on 'dayList'
                    'select count(purchase_id) from purchase_table where day_id = (%s)',
                    ((dayList[i]),)
                )
                loopCount = receiptProjectCursor.fetchall() # store contents in 'loopCount'

                loopCount = int(re.sub( # restructure 'loopCount'
                    '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§,«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(loopCount),
                    count=len(str(loopCount))
                ))

                for j in range(loopCount):

                    visitList.append(len(visitList) + 1) # fill 'visitList'

                    nameList.append(len(nameList) + 1) # fill 'nameList'

                    receiptProjectCursor.execute( # find 'purchase_id' based on 'dayList' and 'loopCount'
                        'select purchase_id from purchase_table where day_id = (%s) order by purchase_id offset (%s) limit 1',
                        ((dayList[i]), (j),)
                    )
                    visitList[len(visitList) - 1] = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'visitList'

                    visitList[len(visitList) - 1] = re.sub( # restructure 'visitList'
                        '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(visitList[len(visitList) - 1]),
                        count=len(str(visitList[len(visitList) - 1]))
                    )

                    receiptProjectCursor.execute( # find names based on 'visitList'
                        'select establishment_region from location_table where purchase_id = (%s)',
                        ((visitList[len(visitList) - 1]),)
                    )
                    nameList[len(nameList) - 1] = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'nameList'

            nameList = restructureData(nameList, period) # restructure 'nameList' array

            ##### CALCULATE FINAL 'newNameList' AND 'newVisitList' IN 'state' #####

            for i in range(len(nameList)):

                k = 0 # set 'key' value

                for j in range(len(nameList)):

                    if (nameList[i] != nameList[j]): # if name duplicate not found, pass

                        pass

                    elif (nameList[i] == nameList[j]): # if name duplicate found, proceed

                        if (nameList[i] == nameList[j] and k == 0): # if name duplicate and 'key' unchanged, proceed

                            k = 1 # change 'key' value

                        elif (nameList[i] == nameList[j] and k == 1): # if name duplicate and 'key' changed, remove value

                            visitList[j] = 0

                k = 0 # reset 'key' value

            visitList = [x for x in visitList if not isinstance(x, int)] # remove all integers in 'visitList'

            newNameList = [] # declare 'newNameList' array

            dayList = [] # empty 'dayList' array

            for i in range(len(visitList)):

                newNameList.append(i) # fill 'newNameList' array

                dayList.append(0) # fill 'dayList' array

                receiptProjectCursor.execute( # grab names based on 'visitList'
                    'select establishment_region from location_table where purchase_id = (%s)',
                    ((visitList[i]),)
                )
                newNameList[i] = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'newNameList'

            for i in range(len(newNameList)):

                for j in range(len(nameList)):

                    if (newNameList[i] == nameList[j]): # if name in 'newNameList' duplicate, add to visit value

                        dayList[i] = dayList[i] + 1

                    else:

                        pass

                newNameList[i] = re.sub( # restructure 'newNameList'
                    '[@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(newNameList[i]),
                    count=len(str(newNameList[i]))
                )

                if (len(newNameList[i].split(" ")) > 1): # if 'newNameList' parts more than 1, split 'newNameList'

                    newName = newNameList[i].split(" ")

                    for j in range(len(newName)):

                        if (j == len(newName) - 1): # if 'newName' part last part, proceed

                            if (len(newName[j]) > 5): # if name longer than 5, take only first 5 characters

                                newName[j] = str(newName[j][0:5]) + "."

                            else: # if name not longer than 5, pass

                                pass

                        else: # reduce 'newName' part to first letter capitalized with period

                            newName[j] = str(newName[j][0]) + "."

                    newNameList[i] = ' '.join(newName) # rejoin 'newName' into 'newNameList'

                else: # if 'newNameList' parts only 1, proceed

                    if (len(newNameList[i]) >= 7): # if 'newNameList' length longer than 7, take only first 6 characters

                        newNameList[i] = str(newNameList[i][0:6]) + "."

                    else: # if 'newNameList' length not longer than 7, pass

                        pass

                dayList[i] = int(re.sub( # restructure 'dayList'
                    '[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(dayList[i]),
                    count=len(str(dayList[i]))
                ))

            nameList = newNameList # set 'newNameList' contents to 'nameList'

            visitList = dayList # set 'dayList' contents to 'visitList'

            ##### LIMIT 'newNameList' AND 'newVisitList' IN 'state' #####

            newNameList = [] # empty 'newNameList' array

            newVisitList = [] # empty 'newVisitList' array

            for i in range(len(nameList)):

                if (visitList[i] >= (int((sum(visitList) ** 0.5))) / 20): # if value in 'visitList' greater than total sum squared divided by 20, fill 'newVisitList' and 'newNameList'

                    newVisitList.append(visitList[i])

                    newNameList.append(nameList[i].title())

                else: # if value in 'visitList' less than total sum squared divided by 20, pass

                    pass

    ##### IF 'compareOne' PURCHASE-BASED #####

    elif (compareOne != "location" and compareOne != "city" and compareOne != "state"): # if 'type' is purchase-based, proceed

        if (compareTwo == "none"): # if 'compareTwo == 'none'', proceed

            compareData = False # set 'compareData' to 'False' as it's not needed

            if (compareOne == "all"): # if no 'compareTwo' and 'compareOne == 'all'', proceed

                ##### GRAB DATA FOR 'analysisData' ARRAY FROM 'Receipt_Project_v3.0' #####

                receiptProjectCursor.execute( # grab all data from 'base_fields_table' for data set
                    'select total_spent from base_fields_table order by day_id'
                )
                analysisData = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'analysisData'

            else: # if no 'compareTwo' and 'compareOne != 'all'', proceed

                ##### GRAB DATA FOR 'compareOneDays' ARRAY FROM 'Receipt_Project_v3.0' #####

                receiptProjectCursor.execute( # grab specific data from 'purchase_table' for data set
                    'select distinct(day_id) from purchase_table where purchase_table.purchase_type = (%s) order by day_id',
                    ((compareOne),)
                )
                compareOneDays = receiptProjectCursor.fetchall() # store contents in 'compareOneDays'

                for i in range(len(compareOneDays)):

                    compareOneDays[i] = int( # filter and convert contents in 'compareOneDays'
                        re.sub('[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;,¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(compareOneDays[i]),
                        count=len(str(compareOneDays[i])))
                    )

                ##### CALCULATE 'compareOneData' ARRAY FROM 'Receipt_Project_v3.0' #####

                compareOneData = [] # create empty 'compareOneData' array

                for i in range(len(compareOneDays)):

                    compareOneData.append(i + 1) # fill 'compareOneData' array

                    receiptProjectCursor.execute( # grab specific data from 'purchase_table' for data set
                        'select sum(purchase_amount) from purchase_table where day_id = (%s)',
                        ((compareOneDays[i]),)
                    )

                    compareOneData[i] = str(list(np.asarray(receiptProjectCursor.fetchall()).flatten())) # store contents in 'compareOneData'

                    compareOneData[i] = float( # filter and convert contents in 'compareOneData'
                        re.sub('[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", compareOneData[i],
                        count=len(compareOneData[i]))
                    )

                ##### CALCULATE 'analysisData' ARRAY FROM 'Receipt_Project_v3.0' #####

                receiptProjectCursor.execute(  # grab all data from 'base_fields_table' for data set
                    'select day_id from base_fields_table order by day_id'
                )
                analysisData = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'analysisData'

                for i in range(len(analysisData)):

                    for j in range(len(compareOneDays)):

                        if (analysisData[i] == compareOneDays[j]): # if 'day_id' in 'analysisData' is in 'compareOneDays', replace 'analysisData' with 'compareOneData'

                            analysisData[i] = compareOneData[j]

                    if (analysisData[i] % int(analysisData[i]) == 0): # if 'day_id' in 'analysisData' not in 'compareOneDays', replace 'analysisData' with 0

                        analysisData[i] = 0

        elif (compareTwo != "none"): # if 'compareTwo != 'none'', proceed

            if (compareOne == "all"): # if 'compareTwo != 'none'' and 'compareOne == 'all'', proceed

                ##### GRAB DATA FOR 'analysisData' ARRAY FROM 'Receipt_Project_v3.0' #####

                receiptProjectCursor.execute( # grab all data from 'base_fields_table' for data set
                    'select total_spent from base_fields_table order by day_id'
                )
                analysisData = list(np.asarray(receiptProjectCursor.fetchall()).flatten()) # store contents in 'analysisData'

                ##### GRAB DATA FOR 'compareTwoDays' ARRAY FROM 'Receipt_Project_v3.0' #####

                receiptProjectCursor.execute(  # grab specific data from 'purchase_table' for data set
                    'select distinct(day_id) from purchase_table where purchase_table.purchase_type = (%s) order by day_id',
                    ((compareTwo),)
                )
                compareTwoDays = receiptProjectCursor.fetchall()  # store contents in 'compareTwoDays'

                for i in range(len(compareTwoDays)):
                    compareTwoDays[i] = int(  # filter and convert contents in 'compareTwoDays'
                        re.sub('[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;,¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(compareTwoDays[i]),
                               count=len(str(compareTwoDays[i])))
                    )

                ##### CALCULATE 'compareTwoData' ARRAY FROM 'Receipt_Project_v3.0' #####

                compareTwoData = []  # create empty 'compareTwoData' array

                for i in range(len(compareTwoDays)):
                    compareTwoData.append(i + 1)  # fill 'compareTwoData' array

                    receiptProjectCursor.execute(  # grab specific data from 'purchase_table' for data set
                        'select sum(purchase_amount) from purchase_table where day_id = (%s)',
                        ((compareTwoDays[i]),)
                    )

                    compareTwoData[i] = str(
                        list(np.asarray(
                            receiptProjectCursor.fetchall()).flatten()))  # store contents in 'compareTwoData'

                    compareTwoData[i] = float(  # filter and convert contents in 'compareTwoData'
                        re.sub('[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", compareTwoData[i],
                               count=len(compareTwoData[i]))
                    )

                ##### CALCULATE 'compareData' ARRAY FROM 'Receipt_Project_v3.0' #####

                receiptProjectCursor.execute(  # grab all data from 'base_fields_table' for data set
                    'select day_id from base_fields_table order by day_id'
                )
                compareData = list(
                    np.asarray(receiptProjectCursor.fetchall()).flatten())  # store contents in 'compareData'

                for i in range(len(compareData)):

                    for j in range(len(compareTwoDays)):

                        if (compareData[i] == compareTwoDays[
                            j]):  # if 'day_id' in 'compareData' is in 'compareTwoDays', replace 'compareData' with 'compareTwoData'

                            compareData[i] = compareTwoData[j]

                    if (compareData[i] % int(compareData[
                                                 i]) == 0):  # if 'day_id' in 'compareData' not in 'compareTwoDays', replace 'compareData' with 0

                        compareData[i] = 0

            else: # if 'compareTwo != 'none'' and 'compareOne != 'all'', proceed

                ##### GRAB DATA FOR 'compareOneDays' ARRAY FROM 'Receipt_Project_v3.0' #####

                receiptProjectCursor.execute(  # grab specific data from 'purchase_table' for data set
                    'select distinct(day_id) from purchase_table where purchase_table.purchase_type = (%s) order by day_id',
                    ((compareOne),)
                )
                compareOneDays = receiptProjectCursor.fetchall()  # store contents in 'compareOneDays'

                for i in range(len(compareOneDays)):
                    compareOneDays[i] = int(  # filter and convert contents in 'compareOneDays'
                        re.sub('[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;,¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(compareOneDays[i]),
                               count=len(str(compareOneDays[i])))
                    )

                ##### CALCULATE 'compareOneData' ARRAY FROM 'Receipt_Project_v3.0' #####

                compareOneData = []  # create empty 'compareOneData' array

                for i in range(len(compareOneDays)):
                    compareOneData.append(i + 1)  # fill 'compareOneData' array

                    receiptProjectCursor.execute(  # grab specific data from 'purchase_table' for data set
                        'select sum(purchase_amount) from purchase_table where day_id = (%s)',
                        ((compareOneDays[i]),)
                    )

                    compareOneData[i] = str(list(
                        np.asarray(receiptProjectCursor.fetchall()).flatten()))  # store contents in 'compareOneData'

                    compareOneData[i] = float(  # filter and convert contents in 'compareOneData'
                        re.sub('[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", compareOneData[i],
                               count=len(compareOneData[i]))
                    )

                ##### CALCULATE 'analysisData' ARRAY FROM 'Receipt_Project_v3.0' #####

                receiptProjectCursor.execute(  # grab all data from 'base_fields_table' for data set
                    'select day_id from base_fields_table order by day_id'
                )
                analysisData = list(
                    np.asarray(receiptProjectCursor.fetchall()).flatten())  # store contents in 'analysisData'

                for i in range(len(analysisData)):

                    for j in range(len(compareOneDays)):

                        if (analysisData[i] == compareOneDays[j]):  # if 'day_id' in 'analysisData' is in 'compareOneDays', replace 'analysisData' with 'compareOneData'

                            analysisData[i] = compareOneData[j]

                    if (analysisData[i] % int(analysisData[i]) == 0):  # if 'day_id' in 'analysisData' not in 'compareOneDays', replace 'analysisData' with 0

                        analysisData[i] = 0

                ##### GRAB DATA FOR 'compareTwoDays' ARRAY FROM 'Receipt_Project_v3.0' #####

                receiptProjectCursor.execute(  # grab specific data from 'purchase_table' for data set
                    'select distinct(day_id) from purchase_table where purchase_table.purchase_type = (%s) order by day_id',
                    ((compareTwo),)
                )
                compareTwoDays = receiptProjectCursor.fetchall()  # store contents in 'compareTwoDays'

                for i in range(len(compareTwoDays)):
                    compareTwoDays[i] = int(  # filter and convert contents in 'compareTwoDays'
                        re.sub('[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;,¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(compareTwoDays[i]),
                               count=len(str(compareTwoDays[i])))
                    )

                ##### CALCULATE 'compareTwoData' ARRAY FROM 'Receipt_Project_v3.0' #####

                compareTwoData = [] # create empty 'compareTwoData' array

                for i in range(len(compareTwoDays)):
                    compareTwoData.append(i + 1)  # fill 'compareTwoData' array

                    receiptProjectCursor.execute(  # grab specific data from 'purchase_table' for data set
                        'select sum(purchase_amount) from purchase_table where day_id = (%s)',
                        ((compareTwoDays[i]),)
                    )

                    compareTwoData[i] = str(
                        list(np.asarray(
                            receiptProjectCursor.fetchall()).flatten()))  # store contents in 'compareTwoData'

                    compareTwoData[i] = float(  # filter and convert contents in 'compareTwoData'
                        re.sub('[A-Za-z@_!$\[\]%^#&*()<>?/\|}{~:;¿§«»\'ω⊙¤°℃℉€¥£¢¡®©_+]', "", compareTwoData[i],
                               count=len(compareTwoData[i]))
                    )

                ##### CALCULATE 'compareData' ARRAY FROM 'Receipt_Project_v3.0' #####

                receiptProjectCursor.execute(  # grab all data from 'base_fields_table' for data set
                    'select day_id from base_fields_table order by day_id'
                )
                compareData = list(
                    np.asarray(receiptProjectCursor.fetchall()).flatten())  # store contents in 'compareData'

                for i in range(len(compareData)):

                    for j in range(len(compareTwoDays)):

                        if (compareData[i] == compareTwoDays[j]): # if 'day_id' in 'compareData' is in 'compareTwoDays', replace 'compareData' with 'compareTwoData'

                            compareData[i] = compareTwoData[j]

                    if (compareData[i] % int(compareData[i]) == 0): # if 'day_id' in 'compareData' not in 'compareTwoDays', replace 'compareData' with 0

                        compareData[i] = 0

        ##### RESTRUCTURE 'analysisData' ARRAY #####

        analysisData = restructureData(analysisData, period) # call 'restructureData' function to filter data

        ##### RESTRUCTURE 'compareData' ARRAY #####

        if(compareData != False): # if 'compareData' created, proceed

            compareData = restructureData(compareData, period) # call 'restructureData' function to filter data

        else: # if 'compareData' not created, pass

            pass



    ########## CREATE 'dataAnalytics' GRAPH ##########
    # Based on criterion provided by 'home_page.py', #
    #  the makeDataAnalytics function will create a  #
    #                customized graph.               #
    ##################################################

    if (compareType == "avg"): # if 'avg', make rolling average plot

        ##### CREATE 'dataAnalytics' 'analysisData' RESOURCES #####

        movingAverage = makeMovingAverage(analysisData, int(np.sqrt(len(analysisData))) * 2)  # create 'movingAverage'

        movingAverageIndex = [] # create empty array as 'movingAverageIndex' index

        for i in range(len(movingAverage)):  # fill empty array to length of 'movingAverage'
            movingAverageIndex.append(i + 1)

        movingAverageTrend = makeMovingAverage(movingAverage, int(np.sqrt(len(movingAverage))) * 4)  # create 'movingAverageTrend'

        title = "Rolling Average Trend:"

        ##### FORMAT 'dataAnalyticsGraph' AVERAGE GRAPH #####

        sns.set( # configure 'dataAnalyticsGraph' graph
            rc={'axes.facecolor': '#292D2E', 'figure.facecolor': '#292D2E', 'grid.color': '#395B64',
                'axes.edgecolor': '#292D2E', 'text.color': '#A5C9CA', 'xtick.color': '#A5C9CA',
                'ytick.color': '#A5C9CA', 'figure.figsize': (5.5, 3.5)}
        )

        ##### IF 'compareData' FROM 'compareTwo' NOT FALSE #####

        if (compareData != False): # if 'compareData' not false, proceed

            ##### CREATE 'dataAnalytics' 'compareData' RESOURCES #####

            compareMovingAverage = makeMovingAverage(compareData, int(np.sqrt(
                len(compareData))) * 2) # create 'compareMovingAverage'

            compareMovingAverageTrend = makeMovingAverage(compareMovingAverage, int(np.sqrt(
                len(compareMovingAverage))) * 4) # create 'compareMovingAverageTrend'

            title = "Rolling Average Trends:"

            ##### PLOT 'dataAnalyticsGraph' AVERAGE GRAPH #####

            dataAnalyticsGraph = sns.lineplot( # create 'dataAnalyticsGraph' average line
                movingAverageIndex, movingAverage, color='#A5C9CA'
            ).set(title=title)

            dataAnalyticsGraph = sns.lineplot( # create 'dataAnalyticsGraph' comparison average line
                movingAverageIndex, compareMovingAverage, color='#FFCB42'
            )

            dataAnalyticsGraph = sns.lineplot( # create 'dataAnalyticsGraph' trend line
                movingAverageIndex, movingAverageTrend, color='#E7F6F2'
            )

            if ( # if 'movingAverage' negative, proceed

                    (round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(movingAverage[-1:]),
                        count=len(str(movingAverage))
                    )), 2)) < 0
            ):

                dataAnalyticsGraph.annotate(  # annotate 'movingAverage' line
                    xy=(max(movingAverageIndex), movingAverage[-1:]),
                    text=("-$" + str(-1 * (round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(movingAverage[-1:]),
                        count=len(str(movingAverage))
                    )), 2)))),
                    color='#A5C9CA', size=8
                )

            else:  # if 'movingAverage' positive, proceed

                dataAnalyticsGraph.annotate(  # annotate 'movingAverage' line
                    xy=(max(movingAverageIndex), movingAverage[-1:]),
                    text=("$" + str(round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(movingAverage[-1:]),
                        count=len(str(movingAverage))
                    )), 2))),
                    color='#A5C9CA', size=8
                )

            if ( # if 'movingAverageTrend' negative, proceed

                    (round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(movingAverageTrend[-1:]),
                        count=len(str(movingAverageTrend))
                    )), 2)) < 0
            ):

                dataAnalyticsGraph.annotate(  # annotate 'movingAverageTrend' line
                    xy=(max(movingAverageIndex), movingAverageTrend[-1:]),
                    text=("-$" + str(-1 * (round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(movingAverageTrend[-1:]),
                        count=len(str(movingAverageTrend))
                    )), 2)))),
                    color='#E7F6F2', size=8
                )

            else:  # if 'movingAverageTrend' positive, proceed

                dataAnalyticsGraph.annotate(  # annotate 'movingAverageTrend' line
                    xy=(max(movingAverageIndex), movingAverageTrend[-1:]),
                    text=("$" + str(round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(movingAverageTrend[-1:]),
                        count=len(str(movingAverageTrend))
                    )), 2))),
                    color='#E7F6F2', size=8
                )

            dataAnalyticsGraph = sns.lineplot( # create 'dataAnalyticsGraph' comparison trend line
                movingAverageIndex, compareMovingAverageTrend, color='#FFF4CF'
            )

            if ( # if 'compareMovingAverage' negative, proceed

                    (round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(compareMovingAverage[-1:]),
                        count=len(str(compareMovingAverage))
                    )), 2)) < 0
            ):

                dataAnalyticsGraph.annotate(  # annotate 'compareMovingAverage' line
                    xy=(max(movingAverageIndex), compareMovingAverage[-1:]),
                    text=("-$" + str(-1 * (round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(compareMovingAverage[-1:]),
                        count=len(str(compareMovingAverage))
                    )), 2)))),
                    color='#FFCB42', size=8
                )

            else:  # if 'compareMovingAverage' positive, proceed

                dataAnalyticsGraph.annotate(  # annotate 'compareMovingAverage' line
                    xy=(max(movingAverageIndex), compareMovingAverage[-1:]),
                    text=("$" + str(round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(compareMovingAverage[-1:]),
                        count=len(str(compareMovingAverage))
                    )), 2))),
                    color='#FFCB42', size=8
                )

            if ( # if 'compareMovingAverageTrend' negative, proceed

                    (round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(compareMovingAverageTrend[-1:]),
                        count=len(str(compareMovingAverageTrend))
                    )), 2)) < 0
            ):

                dataAnalyticsGraph.annotate(  # annotate 'compareMovingAverageTrend' line
                    xy=(max(movingAverageIndex), compareMovingAverageTrend[-1:]),
                    text=("-$" + str(-1 * (round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(compareMovingAverageTrend[-1:]),
                        count=len(str(compareMovingAverageTrend))
                    )), 2)))),
                    color='#FFF4CF', size=8
                )

            else:  # if 'compareMovingAverageTrend' positive, proceed

                dataAnalyticsGraph.annotate(  # annotate 'compareMovingAverageTrend' line
                    xy=(max(movingAverageIndex), compareMovingAverageTrend[-1:]),
                    text=("$" + str(round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(compareMovingAverageTrend[-1:]),
                        count=len(str(compareMovingAverageTrend))
                    )), 2))),
                    color='#FFF4CF', size=8
                )

            plt.legend( # create legend
                labels=[
                    compareOne.title() + " Avg.", compareTwo.title() + " Avg.",
                    compareOne.title() + " Trend", compareTwo.title() + " Trend"
                ],
                fontsize=8,
                loc='upper left'
            )

        ##### IF 'compareData' FROM 'compareTwo' NONE TYPE #####

        else: # if 'compareData' none type, proceed

            ##### PLOT 'dataAnalyticsGraph' AVERAGE GRAPH #####

            dataAnalyticsGraph = sns.lineplot( # create 'dataAnalyticsGraph' average line
                movingAverageIndex, movingAverage, color='#A5C9CA'
            ).set(title=title)

            dataAnalyticsGraph = sns.lineplot( # create 'dataAnalyticsGraph' trend line
                movingAverageIndex, movingAverageTrend, color='#E7F6F2'
            )

            if ( # if 'movingAverage' negative, proceed

                    (round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(movingAverage[-1:]),
                        count=len(str(movingAverage))
                    )), 2)) < 0
            ):

                dataAnalyticsGraph.annotate(  # annotate 'movingAverage' line
                    xy=(max(movingAverageIndex), movingAverage[-1:]),
                    text=("-$" + str(-1 * (round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(movingAverage[-1:]),
                        count=len(str(movingAverage))
                    )), 2)))),
                    color='#A5C9CA', size=8
                )

            else:  # if 'movingAverage' positive, proceed

                dataAnalyticsGraph.annotate(  # annotate 'movingAverage' line
                    xy=(max(movingAverageIndex), movingAverage[-1:]),
                    text=("$" + str(round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(movingAverage[-1:]),
                        count=len(str(movingAverage))
                    )), 2))),
                    color='#A5C9CA', size=8
                )

            if ( # if 'movingAverageTrend' negative, proceed

                    (round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(movingAverageTrend[-1:]),
                        count=len(str(movingAverageTrend))
                    )), 2)) < 0
            ):

                dataAnalyticsGraph.annotate(  # annotate 'movingAverageTrend' line
                    xy=(max(movingAverageIndex), movingAverageTrend[-1:]),
                    text=("-$" + str(-1 * (round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(movingAverageTrend[-1:]),
                        count=len(str(movingAverageTrend))
                    )), 2)))),
                    color='#E7F6F2', size=8
                )

            else:  # if 'movingAverageTrend' positive, proceed

                dataAnalyticsGraph.annotate(  # annotate 'movingAverageTrend' line
                    xy=(max(movingAverageIndex), movingAverageTrend[-1:]),
                    text=("$" + str(round(float(re.sub(
                        '[@_!$%^#&*()\[\]<>?/\|}{~:;¿§«»ω⊙¤°℃℉€¥£¢¡®©_+]', "", str(movingAverageTrend[-1:]),
                        count=len(str(movingAverageTrend))
                    )), 2))),
                    color='#E7F6F2', size=8
                )

            plt.legend( # create legend
                labels=[compareOne.title() + " Avg.", compareOne.title() + " Trend"],
                fontsize=8,
                loc='upper left'
            )

    elif (compareType == "reg"): # if 'reg', make regression plot

        ##### FORMAT 'dataAnalyticsGraph' REGRESSION GRAPH #####

        sns.set( # configure 'dataAnalyticsGraph' graph
            rc={'axes.facecolor': '#292D2E', 'figure.facecolor': '#292D2E', 'grid.color': '#395B64',
                'axes.edgecolor': '#292D2E', 'text.color': '#A5C9CA', 'xtick.color': '#A5C9CA',
                'ytick.color': '#A5C9CA', 'figure.figsize': (5.5, 3.5)}
        )

        ##### CREATE 'dataAnalytics' 'analysisData' RESOURCES #####

        regressionPlotIndex = [] # create empty array as 'purchaseTotals' index

        for i in range(len(analysisData)): # fill empty array
            regressionPlotIndex.append(i + 1)

        title = "Regression Trajectory:"

        ##### IF 'compareData' FROM 'compareTwo' NOT FALSE #####

        if (compareData != False):

            ##### CREATE 'dataAnalytics' 'compareData' RESOURCES #####

            title = "Regression Trajectories:"

            ##### PLOT 'dataAnalyticsGraph' REGRESSION GRAPH #####

            dataAnalyticsGraph = sns.regplot( # plot 'analysisData' points and trajectory line
                regressionPlotIndex, analysisData, scatter_kws={'color': '#A5C9CA'},
                line_kws={'color': '#E7F6F2'}
            ).set(title=title)

            dataAnalyticsGraph = sns.regplot( # plot 'compareData' points and trajectory line
                regressionPlotIndex, compareData, scatter_kws={'color': '#FFCB42'},
                line_kws={'color': '#FFF4CF'}
            )

            plt.legend( # create legend
                labels=[
                    compareOne.title() + " Data", compareOne.title() + " Traj", compareOne.title() + " Pred.",
                    compareTwo.title() + " Data", compareTwo.title() + " Traj.", compareTwo.title() + " Pred.",
                ],
                fontsize=8,
                loc='upper left'
            )

        ##### IF 'compareData' FROM 'compareTwo' FALSE #####

        else: # if 'compareData' false, proceed

            ##### PLOT 'dataAnalyticsGraph' REGRESSION GRAPH #####

            dataAnalyticsGraph = sns.regplot( # plot 'analysisData' points
                regressionPlotIndex, analysisData, scatter_kws={'color': '#A5C9CA'},
                line_kws={'color': '#E7F6F2'}
            ).set(title=title)

            plt.legend( # create legend
                labels=[compareOne.title() + " Data", compareOne.title() + " Traj", compareOne.title() + " Pred.",],
                fontsize=8,
                loc='upper left'
            )

    elif (compareType == "bar"): # if 'type == 'bar'', make bar plot

        ##### FORMAT 'dataAnalyticsGraph' BAR GRAPH #####

        sns.set( # configure 'dataAnalyticsGraph' graph
            rc={'axes.facecolor': '#292D2E', 'figure.facecolor': '#292D2E', 'grid.color': '#395B64',
                'axes.edgecolor': '#292D2E', 'text.color': '#A5C9CA', 'xtick.color': '#A5C9CA',
                'ytick.color': '#A5C9CA', 'figure.figsize': (5.5, 3.5)}
        )

        ##### CREATE 'dataAnalytics' 'analysisData' RESOURCES #####

        if (compareOne == "location"):

            compareOne = "Locations"

        elif (compareOne == "city"):

            compareOne = "Cities"

        elif (compareOne == "state"):

            compareOne = "States"

        if (period == 0):

            title = "Total Visited " + compareOne

        else:

            if (period == 30):

                period = "Month"

            elif (period == 90):

                period = "Quarter"

            elif (period == 365):

                period = "Year"

            title = "Visited " + compareOne + " Last " + str(period)

        ##### PLOT 'dataAnalyticsGraph' BAR GRAPH #####

        dataAnalyticsGraph = sns.barplot(x=newNameList, y=newVisitList).set(title=title)



    ########## SAVE 'dataAnalyticsGraph.png' FILE ##########
    # Below is the code where 'dataAnalyticsGraph.png' is  #
    #    continually 'recycled' in order to provide new    #
    #                        graphs.                       #
    ########################################################

    if os.path.exists('/Users/matthewbeck/Desktop/Projects/Receipt_Project_v3.0/dataAnalyticsGraph.png'): # if file path exists, delete 'dataAnalyticsGraph.png'
        os.remove('/Users/matthewbeck/Desktop/Projects/Receipt_Project_v3.0/dataAnalyticsGraph.png')

    else: # if file path does not exist, pass
        pass

    plt.savefig('/Users/matthewbeck/Desktop/Projects/Receipt_Project_v3.0/dataAnalyticsGraph.png') # save 'dataAnalyticsGraph' graph as 'dataAnalyticsGraph.png'

    plt.cla() # clear 'dataAnalyticsGraph' when complete



    ############### CLOSE CONNECTIONS ###############
    #           Close the connections to            #
    #  'Receipt_Project_v3.0' database in order to  #
    #              prevent data leaks.              #
    #################################################

    receiptProjectCursor.close()  # stop communication with 'Receipt_Project_v3.0' database
    receipt_project.close()  # close the connection to prevent data leaks