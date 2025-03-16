# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionProvideDiseaseInfo(Action):

    def name(self) -> Text:
        return "action_provide_disease_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent = tracker.latest_message['intent'].get('name')

        url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "prop": "extracts",
            "exintro": True,
            "titles": last_intent,
            "format": "json"
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            page = list(data["query"]["pages"].values())[0]
            extract = page.get("extract", "No extract available.")
            message = ""
            dispatcher.utter_message(extract)
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            dispatcher.utter_message("Wait, loading")

        return []
