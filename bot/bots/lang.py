from os import getenv

from requests import post


def analyze_query(query: str, entity_type: str):
    
    endpoint = getenv("AZURE_CONVERSATIONS_ENDPOINT")
    key = getenv("AZURE_CONVERSATIONS_KEY")
    
    url = f"{endpoint}:analyze-conversations?api-version=2024-11-15-preview"
    
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    
    data = {
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "id": "1",
                "text": query,
                "modality": "text",
                "language": "de",
                "participantId": "1"
            }
        },
        "parameters": {
            "projectName": "chatbot",
            "verbose": True,
            "deploymentName": "chatbot-deployment-0.0.6",
            "stringIndexType": "TextElement_V8"
        }
    }
    
    response = post(url, headers=headers, json=data)
    entities = response.json().get('result', {}).get('prediction', {}).get('entities', [])

    for entity in entities:
        if entity.get('category') == entity_type:
            result = entity.get('text')
            print(result)
            return result

    return None

