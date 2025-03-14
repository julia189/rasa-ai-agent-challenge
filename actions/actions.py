from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from doctolib import get_available_doctors

class ActionGetDoctorAppointment(Action):
    def name(self) -> Text:
        return "action_get_available_doctors"
    
    def run(self, dispatcher, tracker, domain):

        doctor_location = tracker.get_slot("location")
        availability = tracker.get_slot("availability")
        top_3_doctors_df = get_available_doctors(location=doctor_location, availabilities=availability)
        dispatcher.utter_message(text=f"Here are three doctors that are available: {top_3_doctors_df}")
#rasa run actions

class ActionCheckAvailableNannys(Action):
    def name(self) -> Text:
        return "action_check_nannys_available"
    
    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date_ = tracker.get_slot("nanny_date")
        nanny_time = tracker.get_lot("nanny_time")
        nanny_hours = tracker.get_slot("nanny_hours")

        return super().run(dispatcher, tracker, domain)

class ActionCheckSufficientFunds(Action):
    def name(self) -> Text:
        return "action_check_sufficient_funds"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # hard-coded balance for tutorial purposes. in production this
        # would be retrieved from a database or an API
        balance = 1000
        transfer_amount = tracker.get_slot("amount")
        has_sufficient_funds = transfer_amount <= balance
        return [SlotSet("has_sufficient_funds", has_sufficient_funds)]
