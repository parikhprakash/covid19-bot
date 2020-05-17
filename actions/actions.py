# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
from actions import process_data
from typing import Any, Text, Dict, List
from datetime import datetime
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
import pickle

from dateutil import relativedelta, parser
try:
    with open('daily_data.pkl','rb') as fp:
        df = pickle.load(fp)
except:
    print("Something went wrong while reading pickle")

def format_time_by_grain(time, grain=None):
    grain_format = {
        "second": "%I:%M:%S%p, %A %b %d, %Y",
        "day": "%A %b %d, %Y",
        "week": "%A %b %d, %Y",
        "month": "%b %Y",
        "year": "%Y",
    }
    timeformat = grain_format.get(grain, "%I:%M%p, %A %b %d, %Y")
    return time.strftime(timeformat)





class QueryNumber(FormAction):
    def name(self):
        return "form_reply_number"
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["metric"]
    
    def submit(self,
                    dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any],
                ) -> List[Dict]:
        #read pickle file
        if tracker.get_slot('time') is None:
            date_query = datetime.today().date()
            print(date_query)
            out_data = df[df['date'].dt.date == date_query]
            # print('DATAFRAME')
            # print(out_data.head())
            if len(out_data)>0:
                if tracker.get_slot('metric') == 'confirmed':
                    dispatcher.utter_message("Total confirmed cases are {} out of which {} are added today".format(list(out_data['totalconfirmed'])[0],list(out_data['dailyconfirmed'])[0]))
                elif tracker.get_slot('metric') == 'recovered':
                    dispatcher.utter_message("Total recovered cases are {} out of which {} are added today".format(list(out_data['totalrecovered'])[0],list(out_data['dailyrecovered'])[0]))
                elif tracker.get_slot("metric") == "deceased":
                    dispatcher.utter_message("Total deceased cases are {} out of which {} are added today".format(list(out_data['totaldeceased'])[0],list(out_data['dailydeceased'])[0]))
                else:
                    dispatcher.utter_message("Total active cases are {} out of which {} are added today".format(list(out_data['totalactive'])[0],list(out_data['dailyactive'])[0]))
            else:
                dispatcher.utter_message("I am having trouble getting you the data. I am still in learning phase.")
            return [AllSlotsReset()]
        else:
            all_entities = tracker.latest_message.get("entities", [])
            time_entity = [e for e in all_entities if e.get("entity") == "time"]
            # print(time_entity)
            additional_info = time_entity[0]['additional_info']
            print(additional_info)
            # dispatcher.utter_message("Additional Info")
            if additional_info['type'] == 'interval':
                from_time = parser.isoparse(additional_info['from']['value'])
                to_time =  parser.isoparse(additional_info['to']['value'])
                grain = additional_info['from']['grain']
                if grain == "day":
                    out_data = df[(df['date'].dt.date > from_time.date()) &
                                    (df['date'].dt.date <= to_time.date())]['daily'+tracker.get_slot('metric')].sum()
                elif grain == 'month':
                    out_data = df[(df['date'].dt.month > from_time.month) &
                                    (df['date'].dt.month <= to_time.month)]['daily'+tracker.get_slot('metric')].sum()
                elif grain == 'week':
                    out_data = df[(df['date'].dt.week > int(from_time.strftime('%V'))) &
                                    (df['date'].dt.week <= int(to_time.strftime('%V')))]['daily'+tracker.get_slot('metric')].sum()
                elif grain == 'year':
                    out_data = df[(df['date'].dt.year > from_time.year) &
                                    (df['date'].dt.year <= to_time.year)]['daily'+tracker.get_slot('metric')].sum()
                else:
                    dispatcher.utter_message("I have date wise data only. I wish I could have second wise feed :(")
                    return [AllSlotsReset()]
                if tracker.get_slot('metric') == 'confirmed':

                    dispatcher.utter_message("In {} total confirmed cases are {}".format(tracker.get_slot("time"),out_data))
                elif tracker.get_slot('metric') == 'recovered':
                    dispatcher.utter_message("In {} total recovered cases are {}".format(tracker.get_slot("time"),out_data))
                elif tracker.get_slot("metric") == "deceased":
                    dispatcher.utter_message("In {} total deceased cases are {}".format(tracker.get_slot("time"),out_data))
                else:
                    dispatcher.utter_message("In {} total active cases are {}".format(tracker.get_slot("time"),out_data))
            else:
                from_time = parser.isoparse(additional_info['value'])
                # from_time = parser.isoparse(additional_info['value'])
                # to_time =  parser.isoparse(additional_info['to']['value'])
                if additional_info['grain'] == 'day':
                    out_data = df[df['date'].dt.date == from_time.date()]['daily'+tracker.get_slot('metric')].sum()
                elif additional_info['grain'] == 'month':
                    out_data = df[df['date'].dt.month == from_time.month]['daily'+tracker.get_slot('metric')].sum()
                elif additional_info['grain'] == 'week':
                    out_data = df[df['date'].dt.week == int(from_time.strftime('%V'))]['daily'+tracker.get_slot('metric')].sum()
                elif additional_info['grain'] == 'year':
                    out_data = df[df['date'].dt.year == from_time.year]['daily'+tracker.get_slot('metric')].sum()
                else:
                    dispatcher.utter_message("I wish I could have that granular data :(")
                    return [AllSlotsReset()]
                time_print = format_time_by_grain(from_time,additional_info['grain'])
                if tracker.get_slot('metric') == 'confirmed':

                    dispatcher.utter_message("{}: total confirmed cases are {}".format(time_print,out_data))
                elif tracker.get_slot('metric') == 'recovered':
                    dispatcher.utter_message("{}:total recovered cases are {}".format(time_print,out_data))
                elif tracker.get_slot("metric") == "deceased":
                    dispatcher.utter_message("{}: total deceased cases are {}".format(time_print,out_data))
                else:
                    dispatcher.utter_message("{}: total active cases are {}".format(time_print,out_data))
            return [AllSlotsReset()]
        # print(tracker.slots)
        # print(tracker.latest_message)
        # dispatcher.utter_message("Here is your number")
        return []

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
