from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from bs4 import BeautifulSoup

class ActionProvideDiseaseInfo(Action):

    def name(self) -> Text:
        return "action_provide_disease_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent = tracker.latest_message['intent'].get('name')

        entities = tracker.latest_message.get('entities', [])
        symptoms = [e['value'] for e in entities if e['entity'] == 'symptom']
        disease = next((e['value'] for e in entities if e['entity'] == 'disease'), None)

        search_term = disease if disease else last_intent

        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "prop": "extracts",
            "exintro": True,
            "titles": search_term,
            "format": "json"
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            page = list(data["query"]["pages"].values())[0]
            extract = page.get("extract", "No information found.")
            clean_text = BeautifulSoup(extract, "html.parser").get_text()
            dispatcher.utter_message(clean_text)
        else:
            dispatcher.utter_message("Sorry, I couldn't fetch the information.")

        return []
