import spacy
from spacy.matcher import PhraseMatcher
from experta import *

# load a language model
nlp = spacy.load("en_core_web_sm")

"""Classes"""
class Ticket(Fact):
    start_location = Field(str)
    end_location = Field(str)

class Memory(Fact):
    start = Field(str)
    end = Field(str)
    pass

class Action(Fact):
    pass

class Statement(Fact):
    pass

class CityMatcher(Fact):
    # Create a City matcher object
    city_matcher = spacy.matcher.Matcher(nlp.vocab)


"""Knowledge Base"""
class Pathfinder(KnowledgeEngine):
    @DefFacts()
    def set_up(self):
        self.city_matcher = spacy.matcher.Matcher(nlp.vocab)
        # Create a matcher for the cities
        self.city_matcher.add("CITIES", cities_rules)

        # Create the ticket for the booking
        yield Ticket()

    @Rule()
    def start_up(self):
        print("Hi! how can I help you today? : ")
        self.declare(Action("get-users-text"))

    @Rule(AS.get_text << Action("get-users-text"))
    def get_users_text(self, get_text):
        # forget the Action
        self.retract(get_text)
        text = input(f"enter: ")
        # Turn the text into lower case
        text = text.lower()
        # Turn the text into NLP objects
        doc = nlp(text)
        # Add to Pathfinder's memory
        self.declare(Statement(doc))

    @Rule(Statement(MATCH.info))
    def get_locations(self, info):
        # Create a City matcher object
        res = self.find_city(info)
        self.declare(Ticket(start_location=res["start"], end_location=res["end"]))
        self.declare(Action("validate-ticket"))

    @Rule(AND(AS.validate << Action("validate-ticket"), Ticket(start_location=MATCH.start, end_location=MATCH.end)))
    def validate_ticket(self, validate, start, end):
        self.retract(validate)
        if start == "" and end == "":
            self.declare(Action("no-destination"))
        elif start != "" and end == "":
            self.declare(Action("no-end-destination"))
            self.declare(Memory(start=start))
        elif start == "" and end != "":
            self.declare(Action("no-start-destination"))
        else:
            self.declare(Action("got-all-destinations"))

    @Rule(AS.no_end_dest << Action("no-end-destination"), AS.mem << Memory(MATCH.start))
    def no_end_destination(self, no_end_dest, start):
        self.retract(no_end_dest)
        self.retract(start)
        print("Got starting dest but Not End dest")
        self.declare(Action("get-users-text"))
        self.declare()

    @Rule(AS.no_start_dest << Action("no-start-destination"))
    def no_start_destination(self, no_start_dest):
        self.retract(no_start_dest)
        print("Got Ending dest but Not Start dest")
        self.declare(Action("get-users-text"))


    @Rule(AS.no_dest << Action("no-destination"))
    def no_destination(self, no_dest):
        self.retract(no_dest)
        print("No Destinations")
        self.declare(Action("get-users-text"))


    @Rule(AS.all_dest << Action("got-all-destinations"))
    def all_destination(self, all_dest):
        self.retract(all_dest)
        print("Got Both destinations")

    def find_city(self, doc):
        cities = {"start": "", "end": ""}
        # Check to see if a city is found in the text
        city_matches = self.city_matcher(doc)

        if len(city_matches) > 0:
            # Find all the cities in the sentence, and append their prev word to the city name
            for match_id, start, end in city_matches:
                if str(doc[start - 1]) in departure_prepositions:
                    cities["start"] = str(doc[start:end])
                elif str(doc[start - 1]) in arrival_prepositions:
                    cities["end"] = str(doc[start:end])
        return cities


"""INFORMATION"""
# Initialize a list of all possible cities the Bot should be able to handle
cities_rules = [
    [{"LOWER": "new york"}], [{"LOWER": "san francisco"}], [{"LOWER": "norwich"}], [{"LOWER": "london"}],
    [{"LOWER": "manchester"}], [{"LOWER": "birmingham"}], [{"LOWER": "bristol"}], [{"LOWER": "york"}],
    [{"LOWER": "cambridge"}], [{"LOWER": "liverpool"}], [{"LOWER": "oxford"}], [{"LOWER": "newcastle"}],
    [{"LOWER": "brighton"}], [{"LOWER": "nottingham"}], [{"LOWER": "plymouth"}], [{"LOWER": "leeds"}],
    [{"LOWER": "southampton"}], [{"LOWER": "sheffield"}], [{"LOWER": "exeter"}], [{"LOWER": "coventry"}],
    [{"LOWER": "hull"}], [{"LOWER": "portsmouth"}]
]

# Initialize possible prepositions for the sentences
departure_prepositions = ["from"]
arrival_prepositions = ["to", "in", "at"]
time_prepositions = ["at", "by", "of"]


if __name__ == "__main__":
    chatbot = Pathfinder()
    chatbot.reset()
    chatbot.run()
