""""""
import boto3

client = boto3.client('comprehend', region_name='us-east-1')

def get_sentiment(s: str):
    if len(s) > 5000: return 0
    response = client.detect_sentiment(Text=s, LanguageCode='en')
    return response['SentimentScore']['Negative']

