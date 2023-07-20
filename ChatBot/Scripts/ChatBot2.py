import spacy

# load a language model
nlp = spacy.load("en_core_web_sm")

string = "I'd Like to book a ticket from london to liverpool at 5:05 today"

text = string
# Turn the text into lower case
text = text.lower()
# Turn the text into NLP objects
doc = nlp(text)

time_type_preposition = ["arriving", "arrive", "getting", "get"]

for ent in doc:
    if ent.ent_type_ == "TIME":
        ans_list = []
        for ancestor in ent.ancestors:
            ans_list.append(ancestor.text)
        if any(time == word for word in ans_list for time in time_type_preposition):
            print(f"arrival: {ent.text}")
        else:
            print(f"dep: {ent.text}")
