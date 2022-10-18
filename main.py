""""""
from settings import SALESFORCE_USERNAME, SALESFORCE_PASSWORD, SALESFORCE_SECURITY_TOKEN
from src.mail import GMail

from simple_salesforce import *



def main():
    gmail = GMail()

    last_10 = gmail.scan_messages(10)

    session_id, instance = SalesforceLogin(username=SALESFORCE_USERNAME, password=SALESFORCE_PASSWORD, security_token=SALESFORCE_SECURITY_TOKEN, domain='login')
    sf = Salesforce(instance=instance, session_id=session_id)

    all_leads = sf.query_all("SELECT Id, Email, SentimentRating__c FROM Lead")

    def update_lead_field(lead, field, value): sf.Lead.update(lead['Id'], {field: value})

    for lead in all_leads['records']:
        for sender, sentiment_rating in last_10.items():
            if lead['Email'] == sender:
                update_lead_field(lead, 'SentimentRating__c', sentiment_rating)




if __name__ == "__main__":
    main()

