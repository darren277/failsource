# Fail Source: Find the source of your failures on Salesforce

## Description

Right now this project allows you to scan your recent e-mails (Gmail only at the moment) and assigns sentiment ratings.

If the sender of the e-mail is in your Salesforce leads, then it will assign them an aggregate sentiment rating.


## How to Use

1. Clone the repo.
2. Have AWS credentials and know the pricing for Comprehend sentiment analysis.
3. Enable Gmail API and create and download an OAuth credentials file.
4. Have a Salesforce account with third party API access enabled and place credentials, including security token, into `.env` file.
5. Run `pip install -r requirements.txt` to install dependencies.
6. Run `python main.py` to run the program.
7. ???
8. Profit.


## Future Plans

Still deciding... 🤔...



