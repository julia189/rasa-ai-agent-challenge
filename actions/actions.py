from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from doctolib import get_available_doctors
from unwrangle_api import get_products

class ActionGetDoctorAppointment(Action):
    def name(self) -> Text:
        return "action_get_available_doctors"
    
    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:

        doctor_location = tracker.get_slot("doctor_location")
        availability = 1
        top_3_doctors_df = get_available_doctors(location=doctor_location, availabilities=availability)
          
        results_readable = "\n".join(["Name: " + doctor_['name'] + "Address: " + doctor_['address'] for _, doctor_ in top_3_doctors_df.iterrows()])
        dispatcher.utter_message(text=f"Here are three doctors that are available \n: {results_readable}")
        return [SlotSet("doctors_search_results_readable", str(results_readable))]
#rasa run actions


class ActionGetProductResponse(Action):
    def name(self) -> Text:
        return "action_get_product_response"
    
    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        
        searched_product_string = tracker.get_slot("searched_product")
        retailer = tracker.get_slot("retailer")
        n_search_results = tracker.get_slot('n_search_result')
        sorting_attribute = tracker.get_slot('sorting_attribute')
    
        products_df = get_products(search_word=searched_product_string, retailer=retailer,  n_search_results=n_search_results, sorting_attribute=sorting_attribute)
        buttons = []
        products_df['url'].apply(lambda value_ : buttons.append({"title" : "Buy product", "payload": value_}))

        dispatcher.utter_message(buttons=buttons)
        
class ActionGetProductReview(Action):
    pass 



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


class ActionGetYoutubeVideos(Action):
    def name(self) -> Text:
        return "action_find_youtube_videos"

    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        search_string = tracker.get_slot("youtube_search_string")
        

class ActionGetBabyDataResponse(Action):
    def name(self) -> Text:
        return "action_get_baby_data_response"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            baby_data_request = tracker.get_slot("baby_data_request")
            


