import pandas as pd
import pygsheets
import pygsheets.spreadsheet
from googleapiclient.errors import HttpError
from authorize_google_sheet import client
from urllib.parse import urlparse
from helpers import is_url
from pygsheets.exceptions import WorksheetNotFound, SpreadsheetNotFound
from pygsheets.spreadsheet import Spreadsheet
from pygsheets.worksheet import  Worksheet



RESULTS_SHEET_NAME = 'results'
URLS_SHEET_NAME = 'urls'
try:
    RESULTS_SHEET = client.open(RESULTS_SHEET_NAME)
except  SpreadsheetNotFound as ex:
    print(f'[X] Could not open The Google sheet of name {RESULTS_SHEET} , Make sure it exists')
    print('Exception {0}', ex)
try:
    URLS_SHEET = client.open(URLS_SHEET_NAME)
except SpreadsheetNotFound as ex:
    print(f'[X] Could not open The Google sheet of name {0} , Make sure it exists', )
    print('Exception {0}', ex)


def import_urls_from_sheet(sheet: Spreadsheet) -> list:
    """
    Imports the urls in the given sheet , put them in a pandas DataFrame then converts the DataFrame to a list
    :param sheet: Spreadsheet object ,containing the urls
    :returns: List of urls extracted from the Spreadsheet
    """
    try:
        worksheet = sheet.sheet1
    except WorksheetNotFound  as ex:
        print(ex)
    df = worksheet.get_as_df()
    list_of_urls = df['urls'].values.tolist()
    return list_of_urls


def convert_list_of_keywords_to_dataframe(list_of_keywords: list) -> pd.DataFrame:
    """

    Converts a list of keywords to a pandas DataFrame

    :param list_of_keywords: Native python list
    :returns: pandas DataFrame of the given list
    """
    list_to_excel = []
    if (len(list_of_keywords) != 0):
        for x in range(len(list_of_keywords)):
            list_months = []
            list_searches = []
            list_annotations = []
            for y in list_of_keywords[x].keyword_idea_metrics.monthly_search_volumes:
                list_months.append(str(y.month)[12::] + " - " + str(y.year))
                list_searches.append(y.monthly_searches)

            for y in list_of_keywords[x].keyword_annotations.concepts:
                list_annotations.append(y.concept_group.name)

            list_to_excel.append(
                [list_of_keywords[x].text,
                 list_of_keywords[x].keyword_idea_metrics.avg_monthly_searches,
                 str(list_of_keywords[x].keyword_idea_metrics.competition)[28::],
                 list_of_keywords[x].keyword_idea_metrics.competition_index,
                 list_searches, list_months,
                 list_annotations]
            )

        df = pd.DataFrame(list_to_excel,
                          columns=[
                              "Keyword", "Average Searches", "Competition Level", "Competition Index",
                              "Searches Past Months", "Past Months", "List Annotations"
                          ]
                          )
    else:
        # Create an empty dataframe
        df = pd.DataFrame()
    return df


def get_worksheet(sheet: Spreadsheet, worksheet_title: str) -> Worksheet:
    """
    Get a worksheet in the given sheet with the given title.

    :param sheet: Google Spreeadsheet
    :param worksheet_title: The title of the worksheet you want to return
    :returns: worksheet with the given name
    """
    try:
        list_of_worksheets = sheet.worksheets(sheet_property='title', value=worksheet_title)
        return list_of_worksheets[0]
    except WorksheetNotFound as ex:
        print(f'The worksheet with the name {worksheet_title} does not exist')


def create_worksheet_for_url(sheet: Spreadsheet, url_name: str) -> Worksheet:
    """
    Creats a worksheet by the name 'worksheet_name' in the given google sheet 'sheet'

    :param sheet: Google Spreadsheet
    :param url_name: the name of the worksheet that is going to be created
    :returns: The worksheet
    """
    if is_url(url_name):
        domain_name = urlparse(url_name).netloc
        worksheet_title = f'Keywords For {domain_name}'

    try:
        worksheet = sheet.add_worksheet(title=worksheet_title)

    except HttpError:
        print(f'A sheet with the name {worksheet_title} already exists')
        print(f'A sheet with the name {worksheet_title} is going to be deleted')
        worksheet = get_worksheet(sheet=sheet, worksheet_title=worksheet_title)
        sheet.del_worksheet(worksheet=worksheet)
        worksheet = sheet.add_worksheet(title=worksheet_title)
        print(f'A sheet with the name {worksheet_title} created successfully')
    return worksheet


def export_dataframe_to_worksheet(df: pd.DataFrame, worksheet: Worksheet):
    """
    Exports DataFrame to google Worksheet

    :param df: pandas DataFrame
    :param worksheet:
    """
    try:
        worksheet.set_dataframe(df=df, start=(1, 1), fit=True)
    except Exception as ex:
        print(ex)
