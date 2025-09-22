import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
from dotenv import load_dotenv
load_dotenv()

key = os.environ['CONTENT_SAFETY_KEY']
endpoint = os.environ['CONTENT_SAFETY_ENDPOINT']


def moderate_comment(comment_text):
    print("--- 1. Starting moderation service ---")
    analysis_data = get_azure_analysis(comment_text)
    final_status = classify_comment(analysis_data)
    analysis_data_dict = None
    if analysis_data:
        analysis_data_dict = {
            'categories_analysis': [
                {'category': cat.category, "severity": cat.severity}
                for cat in analysis_data.categories_analysis
            ]
        }

    return final_status, analysis_data_dict


def get_azure_analysis(comment_text):

    try:
        client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
        request = AnalyzeTextOptions(text=comment_text)
        response = client.analyze_text(request)
        print("--- 2. Azure API call successful ---")

        return response
    except HttpResponseError as e:
        print(f'Error while analizing text: {e.error_message}')

        return None


def classify_comment(analysis_data):
    if not analysis_data:
        print("--- 3. Classification failed: No analysis data received ---")
        return 'pending'

    max_severity = 0
    for category in analysis_data.categories_analysis:

        if category.severity > max_severity:
            max_severity = category.severity
    print(f"--- 3. Max severity calculated: {max_severity} ---")

    if max_severity >= 4:
        return 'not_approved'

    elif max_severity >= 2:
        return 'pending'
    else:
        return 'approved'
