import spacy

nlp = spacy.load("en_core_web_sm")

'''
NOTE FOR MEETING:

1.) In index 2 in the text_list, spaCy doesn't recognise Norwich as a GPE unless it's enter as "Norwich City"
    This should not be a problem as the data set would have station in the name.

'''


# preprocess user input
text_list = {
    1: "I want to book a ticket from New York City to San Francisco tomorrow at 10 AM",
    2: "Can I book a ticket to London from Norwich City by 12 pm",
    3: "Can you help me find a train ticket departing from London and arriving in Manchester city leaving at 2 PM?",
    4: "I need to get to Birmingham from Bristol by train. What are my options for a departure time of 8 AM?",
    5: "What train schedules do you have available for a trip from York City to Cambridge leaving at 10 AM?",
    6: "Is it possible to book a train ticket from Liverpool to London leaving at 7:30 AM?",
    7: "I would like to travel from Newcastle to Bristol by train. Can you check if there are any departures around "
       "noon?",
    8: "Can I book a train ticket from Nottingham City to Plymouth City leaving in the morning?",
    9: "Could you find me a train ticket from Leeds to Southampton departing in the evening?",
    10: "What are the train options available for a trip from Sheffield to Exeter leaving around 3 PM?",
    11: "Is there a train that goes from Coventry to Bristol leaving at 5 PM?",
    12: "I need a train ticket from Hull to Portsmouth departing early morning. Can you help me book it?",
    13: "I want to travel from New York to San Francisco on the 10th of May."
}


for index, text in text_list.items():
    text = text.lower()

    doc = nlp(text)

    # initialize variables for departure and arrival locations and time
    start_dest = None
    end_dest = None
    dep_time = None

    # Initialize possible prepositions for the sentences
    departure_prepositions = ["from"]
    arrival_prepositions = ["to", "in", "at"]
    time_prepositions = ["at", "by", "of"]

    '''
    # Initialize a list of all possible cities the Bot should be able to handle
    cities = ["new york", "san francisco", "norwich", "london", "manchester", "birmingham", "bristol", "york",
              "cambridge",
              "liverpool", "oxford", "newcastle", "brighton", "nottingham", "plymouth", "leeds", "southampton",
              "sheffield",
              "exeter", "coventry", "hull", "portsmouth"]
    '''
    # find the departure and arrival locations
    for token in doc:  # Loop through every object in the sentence
        # print(f"{token} : {token.ent_type_}")
        # print(f"{token} : {token.pos_}")

        # Look to see if this word is a preposition;
        if token.dep_ == "prep":
            '''
            NOTE:
            This is because prepositions tend to link nouns in a sentence
            and in our case, Destinations. i.e the preposition "from" would give us our starting destination
            '''
            # found a prepositional phrase
            '''
                DEBUG - DELETE print statement
            '''
            # print(f"Sub Tree for \"{token}\":", [sub.text for sub in token.subtree])

            # Create empty array to store the Information
            gpe_list = []

            # Loop through the subtree for this word and get the GPE and TIME information
            for sub_token in token.subtree:
                if sub_token.ent_type_ == "GPE" or sub_token.ent_type_ == "TIME":
                    # found a location entity
                    gpe_list.append(sub_token.text)
            gpe_phrase = " ".join(gpe_list)
            # print(gpe_phrase)

            '''
                NOTE:
                We will need to redo this part to add to the list of possible prepositions
            '''
            # print(token.text)
            if token.text in departure_prepositions and sub_token.ent_type_ == "GPE":
                start_dest = gpe_phrase
            elif token.text in arrival_prepositions and sub_token.ent_type_ == "GPE":
                end_dest = gpe_phrase
            elif token.text in time_prepositions and sub_token.ent_type_ == "TIME":
                dep_time = gpe_phrase

    # print the results
    print(index)
    print("Start Destination:", start_dest)
    print("End Destination:", end_dest)
    print("Departure Time:", dep_time)
    print("\n")

