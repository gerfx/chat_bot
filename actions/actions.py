import sqlite3

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionNewRequest(Action):
    def name(self):
        return "utter_new_request"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, **kwargs):
        user_id = tracker.sender_id
        meal = tracker.get_slot("meal")

        with sqlite3.connect('recipes.db') as conn:
            curs = conn.cursor()
            curs.execute(
                "select id, url from recipes where meal_name = ?",
                (meal, )
            )
            (meal_id, url) = curs.fetchone()
            if url:
                dispatcher.utter_message(url)
                curs.execute(
                    "insert into user values(?, ?)",
                    (user_id, meal_id)
                )
            else:
                dispatcher.utter_message("Извините, я не знаю этот рецепт")


class ActionShowHistory(Action):
    def name(self):
        return "action_show_history"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, **kwargs):
        user_id = tracker.sender_id
        with sqlite3.connect('recipes.db') as conn:
            curs = conn.cursor()
            curs.execute(
                "select meal from user inner join recipe by user.meal_id = meal.meal_id"
                "where user.user_id = ?",
                (user_id, )
            )






