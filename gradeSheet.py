import json
import gspread
import sys
import argparse
import operator
import os
from oauth2client.client import SignedJwtAssertionCredentials

STATIC_COLUMNS = [ 'Last Name', 'First Name', 'Username', 'Student ID',
                    'Section', 'TOTAL', '']
SPREADSHEET='CS100 Schedule & Grades'

# hack type exception thrown
def get_first_json(str):
    if str is not None:
        for file in os.listdir('.'):
            if file.endswith('.json'):
                return file
        raise argparse.ArgumentTypeError('Cannot find json file in directory')

def set_up_argparse():
    parser = argparse.ArgumentParser(description='Input grades to Google'
            ' Spreadsheets')
    parser.add_argument('credential', metavar='C', nargs='?', type=get_first_json,
            default='',
            help='location of oAuth2 credential file')
    parser.add_argument('-g', '--group', metavar='G', type=int,
            default=1,
            help='the size of a group (defaults to 1)')
    parser.add_argument('-s', '--spreadsheet', metavar='S', type=str,
            default=SPREADSHEET,
            help='spreadsheet file name')
    return parser.parse_args()

def login_with_key(creds):
    json_key = json.load(open(creds))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'],
        json_key['private_key'].encode(), scope)
    print ('Authenticating ... \n')
    return gspread.authorize(credentials)

def get_relevant_columns(wks):
    section_list = wks.row_values(1)
    column_dict = dict(zip(section_list, list(range(1, len(section_list)))))
    for col in STATIC_COLUMNS : # remove all unneeded columns
        del column_dict[col]
    print ("\nEditing Columns:")
    for i in column_dict:
        print (i)
    return column_dict

def get_student_info(wks, row):
    return "%s %s %s (%s)" % (wks.cell(row, 2).value, wks.cell(row,1).value,
            wks.cell(row,3).value, wks.cell(row,4).value)

def prompt_for_student(wks):
    while 1:
        student_name = input('Enter student name: ')
        cell_list = wks.findall(student_name)
        selected_student = None

        if len(cell_list) > 1 :
            print ("There are more than one student with that name:")
            print ( cell_list )
            for i in range(len(cell_list)):
                print ("%d. %s" % (i, get_student_info(wks, cell_list[i].row)))
            selection = -1
            while selection < 0 or selection > len(cell_list):
                selection = int(input("Select the student "))
            selected_student_row = cell_list[selection].row
            break;
        elif len(cell_list) == 0 :
            print ("There are no students with that name")
        else:
            selected_student_row = cell_list[0].row
            break;

    print ("%s selected" % get_student_info(wks, selected_student_row))
    return selected_student_row

def main(argv):
    args = set_up_argparse()
    gc = login_with_key(args.credential)
    print (args.spreadsheet)
    wks = gc.open(args.spreadsheet).get_worksheet(3)

    print ("\nSelecting worksheet %s" % wks.title)

    column_dict = get_relevant_columns(wks)

    while(1):
        selected_student_rows = []

        # prompt for g number of students
        for i in range(args.group):
            print ("\nStudent %d" % (i + 1))
            selected_student_rows.append(prompt_for_student(wks))

        # prompt for grade in an orderly mannner
        grade_dict = {}
        for key in sorted(column_dict, key=column_dict.__getitem__):
            grade_dict[key] = (input("\n%s: " % key))
        print (grade_dict)
        for column in grade_dict:
            for student in selected_student_rows:
                wks.update_cell(student, column_dict[column], grade_dict[column])
        print ("Update Successful!")

if __name__ == "__main__":
    main(sys.argv)
