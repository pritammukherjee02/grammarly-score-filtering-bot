import time
from requests.exceptions import ReadTimeout
from grammarly.grammarly import Grammarly
#from spreadsheet.spreadsheet import append_grammarly_score_to_spreadsheet, append_onetext_data_to_spreadsheet
from spreadsheet.spreadsheet2 import append_data_to_spreadsheet
import grammarly.constants as const

from onetext.one_text import OneText
#from quetext.quetext import Quetext

import glob
import os
import shutil

print('Welcome to Grammarly filter bot')

#The 2D list that will contain the scores and file names and which will ultimately be uploaded to Google spreadsheets
database = []

choiceForIncludeGrammarly = input('Do you want to include Grammarly scores? (Y/N): ')
includeGrammarly = True
if choiceForIncludeGrammarly == 'Y' or choiceForIncludeGrammarly == 'y':
    includeGrammarly = True
else: includeGrammarly = False

choiceForIncludeOneText = input('Do you want to include One Text scores? (Y/N): ')
includeOneText = True
if choiceForIncludeOneText == 'Y' or choiceForIncludeOneText == 'y':
    includeOneText = True
else: includeOneText = False

if includeGrammarly == False and includeOneText == False:
    print('You have chosen no test to perform.')
    quit()

if includeGrammarly:
    with Grammarly() as bot:

        toContinue = True
        while toContinue:
            numberOfEntries = 0
            bot.land_first_page()
            bot.give_credentials_and_login()
            bot.open_demo_file()
            #Getting all the files in a directory
            #Change the directory location to the folder to store all the files
            list_of_files = glob.glob(const.PATH_TO_CONTENT_FOLDER_PARENT_DIR + 'content/*.txt')
            passing_mark = input('What should the passing mark be for this batch of writings? (0-99): ')
            count = 0

            for file_name in list_of_files:
                string = ""
                file = open(file_name, 'r')
                string += file.read()
                bot.input_data_to_field(data=string)
                passed = bot.get_score_and_check(passing_mark=int(passing_mark))
                if passed[0]:
                    #append_grammarly_score_to_spreadsheet(os.path.basename(file.name), passed[1])
                    database.append([os.path.basename(file.name), str(passed[1])])
                    count = count + 1
                    numberOfEntries+=1
                    shutil.copy(const.PATH_TO_CONTENT_FOLDER_PARENT_DIR + 'content/' + os.path.basename(file.name), const.PATH_TO_CONTENT_FOLDER_PARENT_DIR + '/cache/grammarlyQualifiers')
            
            #Grammarly Plagiarism
            count = 0
            bot.land_premium_account_page()
            list_of_files = glob.glob(const.PATH_TO_CONTENT_FOLDER_PARENT_DIR + 'cache/grammarlyQualifiers/*.txt')
            initial = True
            for file_name in list_of_files:
                string = ""
                file = open(file_name, 'r')
                string += file.read()
                bot.input_data_to_field_in_premium_account(data=string)
                score = bot.click_on_plagiarism_and_get_score(initial=initial)
                database[count].append(score)
                count += 1
                initial = False


            if includeOneText:
                with OneText() as OT:
                    OT.land_first_page()
                    list_of_files = glob.glob(const.PATH_TO_CONTENT_FOLDER_PARENT_DIR + 'cache/grammarlyQualifiers/*.txt')

                    count = 0
                    for file_name in list_of_files:
                        string = ""
                        file = open(file_name, 'r')
                        string += file.read()
                        OT.input_data_to_field(data=string)
                        result = OT.check_for_plagiarism()
                        database[count].append(result)
                        count+=1
                        #append_onetext_data_to_spreadsheet(result)
            else:
                list_of_files = glob.glob(const.PATH_TO_CONTENT_FOLDER_PARENT_DIR + 'cache/grammarlyQualifiers/*.txt')
                count = 0
                for file_name in list_of_files:
                    database[count].append('-')
                    count+=1

            #Add all the individual modules here one by one. Only Grammarly needs to stay open so it needed seperate treatment
            '''
            with Quetext() as QT:
                QT.land_first_page()
                list_of_files = glob.glob(const.PATH_TO_CONTENT_FOLDER_PARENT_DIR + 'cache/grammarlyQualifiers/*.txt')

                for file_name in list_of_files:
                    string = ""
                    file = open(file_name, 'r')
                    string += file.read()
                    QT.input_data_to_field_and_submit(data=string)
                    result = QT.get_plagiarism_percent_score()
                    result = int(result.strip('%'))
                    if result <= 18:
                        #append_quetext_data_to_spreadsheet(result)
                        print(file_name + ' Passed the Quetext test')
            '''

            print(database)
            try:
                append_data_to_spreadsheet(database)
            except ReadTimeout:
                append_data_to_spreadsheet(database)
                '''
                retry_count = 0
                while retry_count < 5:
                    print('Google spreadsheets API timed out retrying...')
                    append_data_to_spreadsheet(database)
                    retry_count+=1
                    time.sleep(3)
                    '''
            #time.sleep(45)
            inputChoice = input('Do you want to do it again with different files in the same directory? (Y/N): ')
            if inputChoice == 'Y' or inputChoice == 'y':
                toContinue = True
            else:
                toContinue = False
else:
    toContinue = True
    while toContinue:
        numberOfEntries = 0
        if includeOneText:
            with OneText() as OT:
                OT.land_first_page()
                list_of_files = glob.glob(const.PATH_TO_CONTENT_FOLDER_PARENT_DIR + 'content/*.txt')
                #passing_mark = input('What should the passing mark be for this batch of writings? (0-99): ')

                for file_name in list_of_files:
                    string = ""
                    file = open(file_name, 'r')
                    string += file.read()
                    numberOfEntries+=1
                    OT.input_data_to_field(data=string)
                    result = OT.check_for_plagiarism()
                    database.append([os.path.basename(file.name), '-', '-', result])
                    #append_onetext_data_to_spreadsheet(result)

        #Add the individual modules here one by one
        '''
        with Quetext() as QT:
            QT.land_first_page()
            list_of_files = glob.glob(const.PATH_TO_CONTENT_FOLDER_PARENT_DIR + 'content/*.txt')

            for file_name in list_of_files:
                string = ""
                file = open(file_name, 'r')
                string += file.read()
                QT.input_data_to_field_and_submit(data=string)
                result = QT.get_plagiarism_percent_score()
                print(result)
                #print(result.strip('%').strip(''))
                #print(float(result.strip('%')))
                #result = int(float(result.strip('%')))
                #if result <= 18:
                    #append_quetext_data_to_spreadsheet(result)
                print(file_name + ' Passed the Quetext test')
        '''

        print(database)
        append_data_to_spreadsheet(database)
        #time.sleep(5*numberOfEntries)
        inputChoice = input('Do you want to do it again with different files in the same directory? (Y/N): ')
        if inputChoice == 'Y' or inputChoice == 'y':
            toContinue = True
        else:
            toContinue = False
        

