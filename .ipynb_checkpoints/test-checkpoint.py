import sys

from google.ads.googleads.errors import GoogleAdsException

from build_the_service import GOOGLE_ADS_CLIENT, CUSTOMER_ID, location_ids, page_url, language_id
from generate_keyword_ideas import generate_keyword_ideas

try:
    list_keywords = generate_keyword_ideas(
        client=GOOGLE_ADS_CLIENT,
        customer_id=CUSTOMER_ID,
        location_ids=location_ids,
        language_id=language_id,
        page_url=page_url,
        keyword_texts=[],
    )
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
print(list_keywords)
