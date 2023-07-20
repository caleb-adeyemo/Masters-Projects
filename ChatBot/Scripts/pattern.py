import spacy
from spacy.matcher import PhraseMatcher
nlp = spacy.load("en_core_web_sm")

'''
NOTE FOR MEETING:
1.  Learn how to search for statements i.e no.4 in the text_list is wrong as the "to" in "get to" is mistook for arrival
2.  Incorporate "out of" into the "departure_prep" list


'''

# Users Texts
text_list = {
    1: "I want to book a ticket from New York City to San Francisco tomorrow at 10 AM",
    2: "Can I book a ticket to London from Norwich City by 12 pm",
    3: "Can you help me find a train ticket departing from London and arriving in Manchester city leaving at 2 PM?",
    4: "I need to get to Birmingham from Bristol by train. What are my options for a departure time of 8 AM?",
    5: "What train schedules do you have available for a trip from York City to Cambridge leaving at 10 AM?",
    6: "Is it possible to book a train ticket from Liverpool to oxford leaving at 7:30 AM?",
    # 7: "I would like to travel from Newcastle to Brighton by train. Can you check if there are any departures around "
    #    "noon?",
    # 8: "Can I book a train ticket from Nottingham to Plymouth leaving in the morning?",
    # 9: "Could you find me a train ticket from Leeds to Southampton departing in the evening?",
    # 10: "What are the train options available for a trip from Sheffield to Exeter leaving around 3 PM?",
    # 11: "Is there a train that goes from Coventry to Bristol leaving at 5 PM?",
    # 12: "I need a train ticket from Hull to Portsmouth departing early morning. Can you help me book it?",
    # 13: "I want to travel from New York to San Francisco on the 10th of May."
}

# Create a PhaseMater object
city_finder = PhraseMatcher(nlp.vocab, None)

# Initialize a list of all possible cities the Bot should be able to handle
cities = ["new york", "san francisco", "norwich", "london", "manchester", "birmingham", "bristol", "york", "cambridge",
          "liverpool", "oxford", "newcastle", "brighton", "nottingham", "plymouth", "leeds", "southampton", "sheffield",
          "exeter", "coventry", "hull", "portsmouth"]

# Initialize a list of all possible prepositions the Bot should be able to handle
departure_prep = ["leaving from", "departing from", "out of", "out from", "starting from", "from"]
arrival_prep = ["arriving at", "arrive at", "into", "to"]
time_prep = ["leaving at", "departing at", "scheduled for", "for", "at", "on"]


# Create NLP objects of these cities
city_obj_list = [nlp(city.lower()) for city in cities]

# Add the NLP objects to the PhaseMatcher Object created earlier
city_finder.add("CITY_NAME", None, *city_obj_list)

# Loop through the list of user texts
for index, text in text_list.items():
    # initialize variables for departure & arrival locations and time
    start_dest = None
    end_dest = None
    dep_time = None

    # Change the texts to lower case
    text = text.lower()

    # Change the text to an NLP object
    doc = nlp(text)

    # Find all the cities in the sentence, and append their name and starting positions
    city_index_dic = {}
    city_matches = city_finder(doc)
    for match_id, start, end in city_matches:
        city_index_dic[doc[start:end]] = start

    # Loop through every word in the preposition list, looking for it in the sentence
    for word in departure_prep:
        # Initialize the min distance and city to the closest preposition
        min_distance = float("inf")
        min_city = None

        # If we have found a value for start_dest then leave this loop
        if end_dest is not None:
            break

        # Look to see if the word is part of the sentence
        if word in text:
            print(index)

            for name, start_idx in city_index_dic.items():
                idx = text.find(word)
                idx_city = text.find(name.text)
                print(f"Word: {word} \t index: {idx} \t city: {name} \t city index: {idx_city}")
                distance = idx_city - idx
                if min_distance > distance >= 0:
                    min_distance = distance
                    min_city = name
            start_dest = min_city
            print(f"Start dest: {start_dest}")

    # Loop through every word in the preposition list, looking for it in the sentence
    for word in arrival_prep:
        # Initialize the min distance and city to the closest preposition
        min_distance = float("inf")
        min_city = None

        # If we have found a value for start_dest then leave this loop
        if end_dest is not None:
            break

        # Look to see if the word is part of the sentence
        if word in text:

            for name, start_idx in city_index_dic.items():
                idx = text.find(word)
                idx_city = text.find(name.text)
                print(f"Word: {word} \t index: {idx} \t city: {name} \t city index: {idx_city}")
                distance = idx_city - idx
                if min_distance > distance >= 0:
                    min_distance = distance
                    min_city = name
            end_dest = min_city
            print(f"End dest: {end_dest}")

        # elif word.text in arrival_prep:
        #     for name, start_idx in city_index_dic.items():
        #         distance = start_idx - word.i
        #         if min_distance > distance >= 0:
        #             min_distance = distance
        #             min_city = name
        #     end_dest = min_city
        #
        # elif word.text in time_prep:
        #     # Create empty array to store the Information
        #     gpe_list = []
        #     for sub_text in word.subtree:
        #         if sub_text.ent_type_ == "TIME":
        #             gpe_list.append(sub_text.text)
        #     gpe_phrase = " ".join(gpe_list)
        #     dep_time = gpe_phrase

    # print(index)
    # print("Start Destination:", start_dest)
    # print("End Destination:", end_dest)
    # print("Departure Time:", dep_time)
    # print("\n")
