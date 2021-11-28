import argparse
from manage_google_sheets import *
from build_the_list import *

_DEFAULT_RESULTS_SHEET_NAME = 'results'
_DEFAULT_URLS_SHEET_NAME = 'urls'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="The input of this script is a Google Spreadsheet containing a bunch of urls"
                    "The output is a newly created Spreadsheet containing a number of Worksheets , one "
                    "for each url ."
    )
    parser.add_argument(
        "-i",
        "--input_sheet",
        type=str,
        required=True,
        default=_DEFAULT_URLS_SHEET_NAME,
        help="The title of the Google Spreadsheet that contains the urls of the websites"
    )
    parser.add_argument(
        "-o",
        "--output_sheet",
        type=str,
        required=True,
        default=_DEFAULT_RESULTS_SHEET_NAME,
        help="The title of the Goolge Spreadsheet that will contain the worksheets for each keyword list",
    )
    args = parser.parse_args()
    input_sheet_name = args.input_sheet
    output_sheet_name=args.output_sheet
    try:
        RESULTS_SHEET = client.open(output_sheet_name)
    except  SpreadsheetNotFound:
        print(f'[✘] Could not open The Google sheet with the name {output_sheet_name} , Make sure it exists')
    try:
        URLS_SHEET = client.open(input_sheet_name)
    except SpreadsheetNotFound:
        print(f'[✘] Could not open The Google sheet of name {input_sheet_name} , Make sure it exists', )

    list_of_urls=import_urls_from_sheet(URLS_SHEET)
    #TODO: handle exceptions
    for url in list_of_urls:

        # buile_the_list_of_keywords is going to return nothing if the url given has no keywords
        list_of_keywords=build_the_list_of_keywords(url)
        if(len(list_of_keywords)>0):
            dataframe=convert_list_of_keywords_to_dataframe(list_of_keywords)
            worksheet=create_worksheet_for_url(RESULTS_SHEET,url)
            export_dataframe_to_worksheet(dataframe,worksheet)
        

    print('الحمد لله رب العالمين♥')
    print('Elhamdulillah ♥')




