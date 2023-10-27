import sqlite3

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from add_url import write


write()


class ActionGiveRecipe(Action):
    def name(self):
        return "action_give_recipe"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        user_id = tracker.sender_id
        meal = tracker.get_slot("meal")

        with sqlite3.connect('recipes.db') as conn:
            curs = conn.cursor()
            curs.execute(
                "SELECT id, meal_url FROM Meals WHERE meal_name = ?",
                (meal, )
            )
            (meal_id, meal_url) = curs.fetchone()
            curs.execute("INSERT INTO User (user_id, meal_id) VALUES (?, ?)", (user_id, meal_id))
            if meal_url:
                dispatcher.utter_message(meal_url)
            else:
                dispatcher.utter_message("Извините, я не знаю этот рецепт")
        return meal_url


class ActionShowHistory(Action):
    def name(self):
        return "utter_show_history"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, **kwargs):
        user_id = tracker.sender_id
        history = []

        with sqlite3.connect('recipes.db') as conn:
            curs = conn.cursor()
            curs.execute(
                "SELECT MEAL FROM USER INNER JOIN recipe BY user.meal_id = meal.meal_id WHERE user.user_id = ?",
                (user_id, )
            )
            history = curs.fetchall()
            if history:
                dispatcher.utter_message("\n".join(history))
            else:
                dispatcher.utter_message("История пуста")
        return history

