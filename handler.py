import os
import requests
import json

from oauth2client.service_account import ServiceAccountCredentials

GA_AUTH_SCOPE    = 'https://www.googleapis.com/auth/analytics.readonly'
GA_AUTH_KEY_PATH = 'key.json'
GA_API_BASE_URL  = 'https://www.googleapis.com/analytics/v3/data/ga'

SHIFTER_PUB_URL    = os.environ.get('SHIFTER_PUB_URL')
GA_IDS             = os.environ.get('GA_IDS')
GA_START_DATE      = os.environ.get('GA_START_DATE')
GA_END_DATE        = os.environ.get('GA_END_DATE')
GA_DIMENSION_NAME  = os.environ.get('GA_DIMENSION_NAME')
GA_DIMENSION_VALIE = os.environ.get('GA_DIMENSION_VALIE')
GA_MAX_RESULTS     = os.environ.get('GA_MAX_RESULTS')

def main(event, context):

    token = ServiceAccountCredentials.from_json_keyfile_name(GA_AUTH_KEY_PATH, GA_AUTH_SCOPE).get_access_token().access_token
    url = build_GApi_url(token)
    res = requests.get(url)

    if (res.status_code == 200):
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': SHIFTER_PUB_URL
            },
            'body': json.dumps(res.json())
        }
    else:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': SHIFTER_PUB_URL
            },
            'body': 'error'
        }

def build_GApi_url(token):
    url  = GA_API_BASE_URL + '?ids=' + GA_IDS
    url += '&start-date=' + GA_START_DATE
    url += '&end-date=' + GA_END_DATE
    url += '&metrics=ga%3Apageviews'
    url += '&dimensions=ga%3ApagePath%2Cga%3ApageTitle'
    url += '&filters=' + GA_DIMENSION_NAME + '%3D%3D' + GA_DIMENSION_VALIE
    url += '&sort=-ga%3Apageviews'
    url += '&start-index=1'
    url += '&max-results=' + GA_MAX_RESULTS
    url += '&access_token=' + token
    return url
