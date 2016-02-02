# CS100_scripts

## Requirements
###OAuth2 Authorization
The following link has all the necessary information to get OAuth credentials
http://gspread.readthedocs.org/en/latest/oauth2.html

###Python3+ and modules
```
pip install --upgrade oauth2client
pip install PyOpenSSL
```

## Usage
Place json credentials into the same directory as the python script for auto-detection or enter in file path

The following command specifies the location of the spreadsheet on Google Drive and the spreadsheet's worksheet to edit. Also two students are allowed to work on a project
```
python3 gradeSheet.py --spreadsheet google_file --worksheet 1 --group 2
```

Note: Google spreadsheet must share its content with the 'client_email` in the credentials json

For more help
```
python3 gradeSheet.py -h
```

