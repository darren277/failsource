""""""
from settings import SALESFORCE_USERNAME, SALESFORCE_PASSWORD, SALESFORCE_SECURITY_TOKEN

from simple_salesforce import *

session_id, instance = SalesforceLogin(username=SALESFORCE_USERNAME, password=SALESFORCE_PASSWORD, security_token=SALESFORCE_SECURITY_TOKEN, domain='login')
sf = Salesforce(instance=instance, session_id=session_id)




def search_for_profile(profile_name):
    return sf.query_all(f"SELECT Id, Name FROM Profile WHERE Name='{profile_name}'")


def update_field_visibility(profile, field, visible=True):
    """ Update field visibility for a given field for a given profile """
    # TODO: Figure out how to do this programmatically.
    ...



def create_custom_sentiment_rating_field():
    """ Create custom sentiment rating field on Lead object """
    field_api_name = 'SentimentRating'
    field_label = 'SentimentRating'
    field_type = 'Number'
    object_api_name = 'Lead'

    payload = {
        "Metadata": {"type": field_type, "inlineHelpText": "", "precision": 7, "label": field_label, "scale": 6, "required": False, "defaultValue": 0},
        "FullName": f"{object_api_name}.{field_api_name}__c"
    }
    result = sf.restful('tooling/sobjects/CustomField/', method='POST', json=payload)
    print('result:', result)

    # admin_profile = search_for_profile('System Administrator')['records'][0]
    # update_field_visibility(admin_profile, field_api_name)


if __name__ == "__main__":
    create_custom_sentiment_rating_field()

