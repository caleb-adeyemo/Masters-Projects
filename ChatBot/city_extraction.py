import spacy
from spacy.matcher import PhraseMatcher
nlp = spacy.load("en_core_web_sm")

'''
NOTE FOR MEETING:

1.) In index 2 in the text_list, spaCy doesn't recognise Norwich as a GPE unless it's enter as "Norwich City"
    This should not be a problem as the data set would have station in the name.

'''


# preprocess user input
text_list = {
    1: "I want to book a ticket from New York City to San Francisco tomorrow at 10 AM",
    2: "Can I book a ticket to London from Norwich by 12 pm",
    3: "Can you help me find a train ticket departing from London and arriving in Manchester city leaving at 2 PM?",
    4: "I need to get to Birmingham from Bristol by train. What are my options for a departure time of 8 AM?",
    5: "What train schedules do you have available for a trip from York City to Cambridge leaving at 10 AM?",
    6: "Is it possible to book a train ticket from Liverpool to Oxford City leaving at 7:30 AM?",
    7: "I would like to travel from Newcastle to Brighton by train. Can you check if there are any departures around "
       "noon?",
    8: "Can I book a train ticket from Nottingham to Plymouth leaving in the morning?",
    9: "Could you find me a train ticket from Leeds to Southampton departing in the evening?",
    10: "What are the train options available for a trip from Sheffield to Exeter leaving around 3 PM?",
    11: "Is there a train that goes from Coventry to Bristol leaving at 5 PM?",
    12: "I need a train ticket from Hull to Portsmouth departing early morning. Can you help me book it?",
    13: "I want to travel from New York to San Francisco on the 10th of May."
}

# Initialize possible prepositions for the sentences
departure_prepositions = ["from"]
arrival_prepositions = ["to", "in", "at"]
time_prepositions = ["at", "by", "of"]

# Initialize a list of all possible cities the Bot should be able to handle
cities = ["new york", "san francisco", "norwich", "london", "manchester", "birmingham", "bristol", "york",
          "cambridge",
          "liverpool", "oxford", "newcastle", "brighton", "nottingham", "plymouth", "leeds", "southampton",
          "sheffield",
          "exeter", "coventry", "hull", "portsmouth"]

# Create NLP objects of these cities
city_obj_list = [nlp(city.lower()) for city in cities]
# Create a PhaseMater object
city_finder = PhraseMatcher(nlp.vocab)
# Add the NLP objects to the PhaseMatcher Object
city_finder.add("CITY_NAME", None, *city_obj_list)

# Loop through each sentence in the list of sentences
for index, text in text_list.items():
    # Turn it into lower case
    text = text.lower()

    # Make the sentence an NLP sentence
    doc = nlp(text)

    # initialize variables for departure and arrival locations and time
    start_dest = None
    end_dest = None
    dep_time = None

    # Find all the cities in the sentence, and append their prev word to the city name
    city_index_dic = {"From": None,
                      "To": None,
                      "Time": None}
    city_matches = city_finder(doc)
    for match_id, start, end in city_matches:
        if str(doc[start - 1]) in departure_prepositions:
            city_index_dic["From"] = doc[start:end]
        elif str(doc[start - 1]) in arrival_prepositions:
            city_index_dic["TO"] = doc[start:end]

    # Loop through every object in the sentence
    for token in doc:
        # Look to see if this word is a preposition;
        if token.ent_type_ == "TIME":
            # Create empty array to store the Information
            gpe_list = []

            # Loop through the subtree for this word and get the TIME information
            for sub_token in token.subtree:
                gpe_list.append(sub_token.text)
            gpe_phrase = " ".join(gpe_list)
            city_index_dic["Time"] = gpe_phrase

    start_dest = city_index_dic["From"]
    end_dest = city_index_dic["TO"]
    dep_time = city_index_dic["Time"]

    # print the results
    print(index)
    print("Start Destination:", start_dest)
    print("End Destination:", end_dest)
    print("Departure Time:", dep_time)
    print("\n")
