import sqlite3

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGiveRecipe(Action):
    def name(self):
        return "utter_give_recipe"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, **kwargs):
        user_id = tracker.sender_id
        meal = tracker.get_slot("meal")

        with sqlite3.connect('recipes.db') as conn:
            curs = conn.cursor()
            curs.execute(
                "SELECT id, url FROM recipes WHERE meal_name = ?",
                (meal, )
            )
            (meal_id, url) = curs.fetchone()
            curs.execute("INSERT INTO USER (user_id, meal_id) VALUES (?, ?)", (user_id, meal_id))
            if url:
                dispatcher.utter_message(url)
            else:
                dispatcher.utter_message("Извините, я не знаю этот рецепт")


class ActionShowHistory(Action):
    def name(self):
        return "utter_show_history"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, **kwargs):
        user_id = tracker.sender_id
        with sqlite3.connect('recipes.db') as conn:
            curs = conn.cursor()
            curs.execute(
                "SELECT MEAL FROM USER INNER JOIN recipe BY user.meal_id = meal.meal_id WHERE user.user_id = ?",
                (user_id, )
            )






