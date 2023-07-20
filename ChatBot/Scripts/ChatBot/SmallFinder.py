from experta import *
import spacy
import random

from spacy.matcher import phrasematcher

# load a language model
nlp = spacy.load("en_core_web_sm")


class Ticket(Fact):
    start = Field(str)
    end = Field(str)
    time = Field(int)


class Action(Fact):
    action = Field(str)


class Statement(Fact):
    info = Field(str)


string = "I'd Like to book a ticket from london to liverpool at 5pm today"

greetings = ["Hi! how can I help you today? : ", "Hello, How can I be of assistance? :"]


def find_city(doc):
    start_loc = None
    end_loc = None

    for ent in doc:
        if ent.ent_type_ == "GPE":
            ans_list = []
            for ancestor in ent.ancestors:
                ans_list.append(ancestor.text)
            if any("from" in word for word in ans_list):
                start_loc = ent.text
            elif any("to" in word for word in ans_list):
                end_loc = ent.text
    print(f"From {start_loc} to {end_loc}")

    return start_loc, end_loc

def get_time(doc):
    time_type_preposition = ["arriving", "arrive", "getting", "get"]

    dep_type = None
    time = None

    for ent in doc:
        if ent.ent_type_ == "TIME":
            ans_list = []
            for ancestor in ent.ancestors:
                ans_list.append(ancestor.text)
            if any(time == word for word in ans_list for time in time_type_preposition):
                time = int(ent.text)
                dep_type = False
            else:
                time = int(ent.text)
                dep_type = True
    return dep_type, time


class KnowledgeBase(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.test = {}

    @DefFacts()
    def start_up(self):
        # Select a random greeting from the list
        greet = random.choice(greetings)
        print(greet)
        print(self.test["Text"])
        yield Action(action="get-users-text")

    @Rule(AS.res << Action(action="get-users-text"))
    def get_users_text(self, res):
        # forget the Action
        self.retract(res)
        text = input()
        # Turn the text into lower case
        text = text.lower()
        # Turn the text into NLP objects
        doc = nlp(text)
        # Add to Pathfinder's memory
        self.declare(Statement(doc))

    @Rule(AS.res << Statement(MATCH.info))
    def get_information(self, res, info):
        # forget
        self.retract(res)
        # Return - Split the sentence into 2

        """INTENT RECOGNITION CODE -- HERE--"""
        """
        -- find the intent of the sentence--
        
        if intent == destination{
        
        }
        elif intent == time{
        
        }
        elif intent == Greet{
        
        }
        elif intent== date{
        
        }
        """
        # Destinations
        loc = find_city(info)

        # Time
        time = get_time(info)

        # Date


        self.declare(Ticket(start=loc[0], end=loc[1], time=time[1], depType=time[0]))





if __name__ == "__main__":
    engine = KnowledgeBase()
    engine.test = {"Text": "Hello"}
    engine.reset()
    engine.run()
