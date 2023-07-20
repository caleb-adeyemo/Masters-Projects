import spacy
from spacy.matcher import PhraseMatcher

# load a language model
nlp = spacy.load("en_core_web_sm")

# define rules for handling user input
greeting_rules = [
    [{"LOWER": "hi"}],
    [{"LOWER": "hi"}, {"IS_PUNCT": True}],
    [{"LOWER": "hello"}, {"IS_PUNCT": True}],
]

# Initialize a list of all possible cities the Bot should be able to handle
cities_rules = [
    [{"LOWER": "new york"}], [{"LOWER": "san francisco"}], [{"LOWER": "norwich"}], [{"LOWER": "london"}],
    [{"LOWER": "manchester"}], [{"LOWER": "birmingham"}], [{"LOWER": "bristol"}], [{"LOWER": "york"}],
    [{"LOWER": "cambridge"}], [{"LOWER": "liverpool"}], [{"LOWER": "oxford"}], [{"LOWER": "newcastle"}],
    [{"LOWER": "brighton"}], [{"LOWER": "nottingham"}], [{"LOWER": "plymouth"}], [{"LOWER": "leeds"}],
    [{"LOWER": "southampton"}], [{"LOWER": "sheffield"}], [{"LOWER": "exeter"}], [{"LOWER": "coventry"}],
    [{"LOWER": "hull"}], [{"LOWER": "portsmouth"}]
]
ticket_booking_rules = [
    {"LOWER": "book"},
    {"LOWER": "a"},
    {"LOWER": "ticket"},
    {"LOWER": "from"},
    {"ENT_TYPE": "GPE", "OP": "+"},
    {"LOWER": "to"},
    {"ENT_TYPE": "GPE", "OP": "+"},
]

greeting_response_dict = {
    0: "",
    1: "Hello! How can I help you today?",
    2: "Hello!"
}

# Initialize possible prepositions for the sentences
departure_prepositions = ["from"]
arrival_prepositions = ["to", "in", "at"]
time_prepositions = ["at", "by", "of"]


# define a function to handle user input
def handle_input(input_text):
    # Turn the text into lower case
    input_text = input_text.lower()
    # Turn the text into NLP objects
    doc = nlp(input_text)
    """GREETING"""
    greeting_response = handle_greeting(doc)

    """TICKETS"""
    start_dest, end_dest = handle_tickets(doc)

    # check if input greeting_matches a ticket booking rule
    if start_dest and end_dest:
        print(f"Great! I'll book a ticket from {start_dest} to {end_dest}. When would you like to travel?")
    elif start_dest and not end_dest:
        print(f"Sorry, you want to leave from {start_dest} but I didn't catch the End destination. Please provide an "
              f"Ending location.")
    elif end_dest and not start_dest:
        print("Sorry, I didn't catch the Start destination. Please provide a Start location.")
    # handle other scenarios or intents here
    # ...

    return "Sorry, I'm not sure how to help with that. Can you please provide more information?"


def handle_greeting(doc):
    """GREETING"""
    # Create a Greeting matcher object
    greeting_matcher = spacy.matcher.Matcher(nlp.vocab)
    # Create a matcher for the greetings
    greeting_matcher.add("GREETING", greeting_rules)
    # check if input matches a greeting rule
    greeting_matches = greeting_matcher(doc)

    if len(greeting_matches) > 0:
        """
        NOTE-
        Variable: greeting_response_dict
        Type: Dictionary
        
        1 return value is for the case of where no Location is provided so the bot prompts the user for enquiry
        2 return value is for when the user provides at least on info.
        0 return value is for when no greeting is found
        """
        return 1, 2
    return 0


def handle_tickets(doc):
    """TICKET"""
    # Create a City matcher object
    city_matcher = spacy.matcher.Matcher(nlp.vocab)
    # Create a matcher for the cities
    city_matcher.add("CITIES", cities_rules)
    # Check to see if a city is found in the text
    city_matches = city_matcher(doc)

    # initialize variables for departure and arrival locations and time
    start_dest = None
    end_dest = None

    if len(city_matches) > 0:
        # Find all the cities in the sentence, and append their prev word to the city name
        for match_id, start, end in city_matches:
            if str(doc[start - 1]) in departure_prepositions:
                start_dest = doc[start:end]
            elif str(doc[start - 1]) in arrival_prepositions:
                end_dest = doc[start:end]
    return start_dest, end_dest


# example usage
user_input = "Hello! Can you book a ticket from London to Liverpool for me?"
# user_input = "Hello! Can you book a ticket from London for me?"
# user_input = "Hello! Can you book a ticket to Liverpool for me?"
# user_input = "Can you book a ticket from London to Liverpool for me?"


response = handle_input(user_input)
# print(response)
