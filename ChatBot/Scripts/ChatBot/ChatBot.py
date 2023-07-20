from experta import *
from nlu import get_result

class Greeting(Fact):
    pass

class BookingIntent(Fact):
    pass

class StartLocation(Fact):
    pass

class EndLocation(Fact):
    pass

class Date(Fact):
    pass

class Time(Fact):
    pass

class UserInput(Fact):
    pass

class ChatBot(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Greeting()

    @Rule(Greeting())
    def greet(self):
        print("Bot: Hi, I'm your travel assistant. How can I help you today?")
        self.declare(BookingIntent())

    @Rule(BookingIntent() & AS._intent << L('book'))
    def book_intent(self, _intent):
        self.declare(BookingIntent(intent='book'))

    @Rule(BookingIntent() & AS._intent << L('predict'))
    def predict_intent(self, _intent):
        self.declare(BookingIntent(intent='predict'))

    @Rule(BookingIntent(intent='book') & NOT(StartLocation()))
    def ask_start_location(self):
        self.declare(StartLocation())

    @Rule(BookingIntent(intent='book') & NOT(EndLocation()))
    def ask_end_location(self):
        self.declare(EndLocation())

    @Rule(BookingIntent(intent='book') & NOT(Date()))
    def ask_date(self):
        self.declare(Date())

    @Rule(BookingIntent(intent='book') & NOT(Time()))
    def ask_time(self):
        self.declare(Time())

    @Rule(BookingIntent(intent='book'),
          OR(StartLocation(MATCH.start_loc),
             EndLocation(MATCH.end_loc),
             Date(MATCH.date),
             Time(MATCH.time)))
    def process_booking_details(self, start_loc=None, end_loc=None, date=None, time=None):
        if not start_loc:
            print("Bot: Did you have a start location in mind?")
        elif not end_loc:
            print("Bot: Where would you like to go?")
        elif not date:
            print("Bot: When would you like to travel?")
        elif not time:
            print("Bot: What time would you like to depart/arrive?")
        else:
            print(f"Bot: Great! I can book a ticket for you to travel from {start_loc} to {end_loc} on {date}.")
            if time["is_leaving_time"]:
                print(f"Bot: You'll depart at {time['time_value']} o'clock.")
            else:
                print(f"Bot: You'll arrive at {time['time_value']} o'clock.")
            print("Bot: Is there anything else you would like from me?")

    @Rule(BookingIntent(intent='predict'))
    def process_prediction_intent(self):
        print("Bot: I'm sorry, but the prediction feature is currently unavailable.")
        print("Bot: Is there anything else I can assist you with?")

    @Rule(BookingIntent(intent='book') & AS._input << UserInput("no"))
    def exit_bot(self, _input):
        print("Bot: Okay, thank you. Have a great day!")

    def process_user_input(self, message):
        result = get_result(message)

        if intent == "greet":
            self.declare(Greeting())
        elif intent == "book":
            self.declare(BookingIntent(intent='book'))
        elif intent == "predict":
            self.declare(BookingIntent(intent='predict'))
        else:
            self.declare(UserInput(message=message))

        for entity in entities:
            if entity['entity'] == "start_location":
                self.declare(StartLocation(entity['value']))
            elif entity['entity'] == "end_location":
                self.declare(EndLocation(entity['value']))
            elif entity['entity'] == "date":
                self.declare(Date(entity['value']))
            elif entity['entity'] == "time":
                is_leaving_time = True if entity['value'] == "departure" else False
                self.declare(Time(entity['value'], is_leaving_time))

    def generate_response(self):
        self.run()


if __name__ == "__main__":
    bot = ChatBot()
    while True:
        user_input = input("User: ")
        bot.process_user_input(user_input)
        bot.generate_response()
