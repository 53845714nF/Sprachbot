from os import getenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient


endpoint = getenv["AZURE_CONVERSATIONS_ENDPOINT"]
key = getenv["AZURE_CONVERSATIONS_KEY"]
project_name = getenv["AZURE_CONVERSATIONS_PROJECT_NAME"]
deployment_name = getenv["AZURE_CONVERSATIONS_DEPLOYMENT_NAME"]


def analyze_query(query: str):
    client = ConversationAnalysisClient(endpoint, AzureKeyCredential(key))
    with client:
        result = client.analyze_conversation(
        task={
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "participantId": "1",
                    "id": "1",
                    "modality": "text",
                    "language": "en",
                    "text": query
                },
                "isLoggingEnabled": False
            },
            "parameters": {
                "projectName": project_name,
                "deploymentName": deployment_name,
                "verbose": True
            }
        }
    )
    return result
