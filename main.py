import argparse
_DEFAULT_INPUT_SHEET_TITLE='urls'
from manage_google_sheets import *
from build_the_list import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="The input of this script is a Google Spreadsheet containing a bunch of urls"
                    "The output is a newly created Spreadsheet containing a number of Worksheets , one "
                    "for each url ."
    )
    parser.add_argument(
        "-s",
        "--spreadsheet",
        type=str,
        required=True,
        default=_DEFAULT_INPUT_SHEET_TITLE,
        help="The title of the Goolge Spreadsheet that contains the urls of the websites",
    )
    args=parser.parse_args()
    input_sheet_name=args.spreadsheet
    list_of_urls=import_urls_from_sheet()




