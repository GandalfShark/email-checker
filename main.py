# updated email checker for python class
import requests, glob
import key as k
from time import sleep

"""
Create a Python script that will meet the constraints below. The program:
I. should run continuously until the user chooses to “quit”: #DONE
II. must perform an HTTP GET request to a website #DONE
III. must access JSON data from a website #DONE
IV. must be able to convert that JSON data to a string #DONE
V. must be able to save a string to a file #DONE
VI. must be able to retrieve data from a file #DONE
VII. needs to include at least 1 user-generated module #DONE
VIII. must have a user interface designed using F-strings #DONE
IX. must include one “Easter Egg” #DONE
"""
# color text code from "geeks for geeks", modified for readability

def pr_green(green_text):
    print("\033[92m {}\033[00m" .format(green_text))


def pr_yellow(yellow_text):
    print("\033[93m {}\033[00m" .format(yellow_text))


def is_it_email(email_or_not):
    if '@' in email_or_not:
        return True
    else:
        pr_yellow('\n    Error, Not a valid email')
        return False
    # make sure that the input at least looks like an email


def file_out(email, response_in):
    with open(f'{email}.txt', 'w') as file1:
        file1.write(response_in.text)
    print('** Report written to file. ** ')
    # create a file with the name "someemail@email.com.txt"


def rep_check_call(email):
    email = email
    if (email + '.txt') in checked_mails:
        pr_yellow('E-Mail has been checked:\n')
        with open(email + '.txt', 'r') as file:
            print(file.read())
            # retrieve the date from the file an output it to screen
            sleep(2)
            return

    url = 'https://emailrep.io/' + email
    # as specified in API docs query must be done via HTTPS
    headers = {"Key": k.the_key, "User-Agent": 'Email info School Project'}
    # provide the API key as instructed in docs for the API, with description of project
    response = requests.get(url, headers=headers)

    try:
        if (response.json())['status'] == 'fail':
            pr_yellow('Error accessing API.\nLimit of calls may be reached.')
            return None
    except KeyError:
        pass
        # the json data will only have the key 'status' if the call fails
        # this should handle the error

    while True:
        full_report = input('''' 
        F - for a full report & file output
        S - for a short report\n: ''')
        if full_report in ['f', 'F']:
            print(response.text)
            file_out(email_add, response)
            break
            # print the json data from emailrep.io as a text dump to the screen
        elif full_report in ['s', 'S']:
            short = response.json()
            # print(short)
            pr_yellow(f'--- report for {email_add} ---')
            pr_green('EMAIl:' + short['email'])
            pr_yellow('MALICIOUS:' + str(short['details']['malicious_activity']))
            pr_green('BREACHED DATA:' + str(short['details']['data_breach']))
            pr_yellow('LEAKED CREDS:' + str(short['details']['credentials_leaked']))
            pr_green('DISPOSABLE: ' + str(short['details']['disposable']))
            pr_yellow('DELIVERABLE: ' + str(short['details']['deliverable']))
            more = input('''
M - print more to screen details 
W - write details to file
any other key to continue ''')
            if more in ['m', 'M']:
                print(response.text)
                break
            if more in ['w', 'W']:
                file_out(email_add, response)
                break
            # just pull out some values, give the option to
            break


def title():
    pr_green("""
    --------------------------
    |  E.MAIL INFO CHECKER   |
    | is it pwnd or sketchy? |
    --------------------------

emails checked:
    """)


checked_email_list = []
while True:
    title()
    checked_mails = (glob.glob('*@*'))
    for _ in checked_mails:
        rev = _.strip('.txt')
        pr_yellow(rev)
    # regular expression search to look for @ containing file names
    # removal of .txt for readability in menu
    email_add = input("""
enter an email to check or
enter "quit" or "exit" to quit

""")
    if email_add in ['quit', 'exit', 'Exit', 'Quit', 'Q', 'q', 'die']:
        if email_add == 'die':
            pr_yellow(f'oh noes, I {email_add} now.')
        break
        # quit the loop if the user wants to exit
    if email_add == 'Norge':
        pr_green('Jeg kan spise glas. Det gjør meg ikke vondt.')
        # Easter egg as per assignment. Returns "I can eat glass and it will not hurt me"
        # this is a reference to the classic web page. Archive link below:
        # https://web.archive.org/web/20040201212958/http://hcs.harvard.edu/~igp/glass.html
        continue
    if is_it_email(email_add):
        rep_check_call(email_add)
        # make sure the input contains an @ then run the API call function
print('Goodbye.')

