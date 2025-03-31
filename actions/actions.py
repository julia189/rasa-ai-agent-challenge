from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from apis.doctolib import get_available_doctors, get_city_from_postcode
from apis.product_search import get_products
from apis.symptoms_search import get_search_results
from apis.youtube_client import get_youtube_recommendations, get_text_from_video
import re

class ActionGetDoctorAppointment(Action):
    def name(self) -> Text:
        return "action_get_available_doctors"
    
    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:

        doctor_location = tracker.get_slot("doctor_location")
        availability = 1
        top_3_doctors_df = get_available_doctors(location=doctor_location, availabilities=availability)

        if top_3_doctors_df is not None:
            results_readable = "\n".join(["Name: " + doctor_['name'] + "Address: " + doctor_['address'] for _, doctor_ in top_3_doctors_df.iterrows()])
            dispatcher.utter_message(text=f"Here are three doctors that are available \n: {results_readable}")
        else:
            results_readable = None
            dispatcher.utter_message(text=f"I'm sorry something did not work out, please try again.")
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

        if not isinstance(n_search_results, int):
            print("Convert n_search_results to integer")
            n_search_results = int(n_search_results)
    
        products_df = get_products(search_word=searched_product_string, retailer=retailer,  n_search_results=n_search_results, sorting_attribute=sorting_attribute)
        product_search_results_readable = "\n".join() #TODO: fix 
        return [SlotSet("product_search_results_readable", str(products_df.head(n_search_results)))]
        
#class ActionGetProductReview(Action):
 #  pass 

class ActionCheckIfPostcode(Action):
    def name(self) -> Text:
        return "action_check_if_postcode"
    
    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        doctor_location = tracker.get_slot("doctor_location")
        if _is_valid_postcode(doctor_location):
            dispatcher.utter_message(text=f"I am checking if I find a city for this postcode.")
            city = get_city_from_postcode(doctor_location).split(',')[1]
            location_postcode_string = '-'.join(doctor_location, city)
            dispatcher.utter_message(text=f"Did you mean {location_postcode_string}?")
            return[SlotSet("is_postcode", True), SlotSet("doctor_location", location_postcode_string)]


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
        result = get_youtube_recommendations(query=search_string)

        if response:
            results_readable = "\n".join(["Title: " + item_['snippet']['title'] + "\n Description: " + item_['description'] 
            + f"\n [View video] (https://www.youtube.com/watch?v={item_['id']['videoId']})" for item_ in result])
            dispatcher.utter_message(text=f"Here are the top 3 videos \n: {results_readable}")
        else:
            results_readable = None
            dispatcher.utter_message(text=f"I'm sorry something did not work out, please try again.")
        return [SlotSet("video_ids", str(','.join([item_['id']['videoId'] for item_ in result])))]


class ActionSummarizeYoutubeVideo(Action):
    def name(self) -> Text:
        return "action_summarize_youtube_video"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        video_position = tracker.get_slot("video_number")
        video_ids = tracker.get_slot("video_ids")
        video_id = video_ids.split(",")[video_position-1]
        transcript_text = get_text_from_video(video_id=video_id)
        chunks = create_chunks(transcript_text)
        return chunks



class ActionGetBabyDataResponse(Action):
    def name(self) -> Text:
        return "action_get_baby_data_response"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            baby_data_request = tracker.get_slot("baby_data_request")
            


def _is_valid_postcode(postcode):
    pattern = r'^\d{5}?$'  
    return bool(re.match(pattern, postcode))


class ActionRunInternetSearch(Action):
    def name(self) -> Text:
        return "action_run_internet_search"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        symptoms = tracker.get_slot("symptoms")
        duration = tracker.get_slot("duration")
        search_results = get_search_results(symptoms, duration)
        
        if search_results:
            results_readable = "\n".join([f"Title: {result['snippet']}\n Link: {result['link']}" for result in search_results])
            dispatcher.utter_message(text=f"Here are some articles that might help:\n{results_readable}")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find any relevant articles.")
        
        return []