import sys
import pandas as pd
from google.ads.googleads.errors import GoogleAdsException
from build_the_service import GOOGLE_ADS_CLIENT, CUSTOMER_ID, location_ids, language_id
from generate_keyword_ideas import generate_keyword_ideas


def build_the_list_of_keywords(page_url: str) -> list:
    """
    Generates a list of keywords from a given url

    :param page_url: url of a website to extract keywords from
    :returns: list of keywords
    """
    try:
        list_of_keywords = generate_keyword_ideas(
            client=GOOGLE_ADS_CLIENT,
            customer_id=CUSTOMER_ID,
            location_ids=location_ids,
            language_id=language_id,
            page_url=page_url,
            keyword_texts=[],
        )
        if(len(list_of_keywords)!=0):
            print("[✔]  The list Built Successfully")
        else:
            print('[✖] No keywords found for this website')
        return list_of_keywords
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
