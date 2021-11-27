from google.ads.googleads.client import GoogleAdsClient
from generate_keyword_ideas import _DEFAULT_LANGUAGE_ID, _DEFAULT_LOCATION_IDS

# Prepare the arguments required for generate_keyword_ideas
# 1)
# client
# a client for the API
GOOGLE_ADS_CLIENT = GoogleAdsClient.load_from_storage(
    version="v9",
    path='./google-ads.yaml'
)
# 2)
# The id of a test Google Ads Test Account
# This should be the id of Google ads account of your client your are working with
CUSTOMER_ID = '4315122109'

# 3)
location_ids = _DEFAULT_LOCATION_IDS

# 4)
language_id = _DEFAULT_LANGUAGE_ID

# 5)
# The page url you want to extract keywords from
# The should be loaded from a csc file or a Goolge Sheet