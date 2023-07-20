import spacy
import re

nlp = spacy.load('en_core_web_sm')

# Regular Expressions
greetings = ['hello', 'hey', 'hi', 'yo']
greeting_regex = re.compile(fr'(?i)\b({"|".join(greetings)})\b')

false = ["false", "no", "nah"]
false_regex = re.compile(fr'(?i)\b({"|".join(false)})\b')

true = ["true", "yes", "yeah", "yh"]
true_regex = re.compile(fr'(?i)\b({"|".join(true)})\b')

# Dicts & Lists
time_type_preposition = ["arriving", "arrive", "getting", "get"]

def get_result(message):
    result = {}

    # Greetings
    if greeting_regex.search(message.lower()):
        result["greeting"] = True

    doc = nlp(message)

    # Location
    for token in doc:
        if token.ent_type_ == "GPE":
            ans_list = [token.text] + [ancestor.text for ancestor in token.ancestors]
            if any(preposition in ans_list for preposition in ["from", "at"]):
                result["start_loc"] = token.text
            elif any(preposition in ans_list for preposition in ["to"]):
                result["end_loc"] = token.text

    # Time
    for ent in doc:
        if ent.ent_type_ == "TIME" and ent.like_num:
            result["time"] = {}
            ans_list = []
            for ancestor in ent.ancestors:
                ans_list.append(ancestor.text)
            if any(time == word for word in ans_list for time in time_type_preposition):
                result["time"]["time_value"] = int(ent.text)
                result["time"]["is_leaving_time"] = False
            else:
                result["time"]["time_value"] = int(ent.text)
                result["time"]["is_leaving_time"] = True

    # Date
    months = ["january", "february", "march", "april", "may", "june",
              "july", "august", "september", "october", "november", "december"]
    result["date"] = {}
    for token in doc:
        if token.text.lower() in months:
            result["date"]["month"] = token.text
        elif re.match(r'\d+th', token.text.lower()):
            day = re.sub(r"th\b", "", token.text)
            result["date"]["day"] = int(day)
        elif re.match(r'\d{1,2}/\d{1,2}', token.text):
            date_parts = token.text.split('/')
            result["date"]["day"] = int(date_parts[0])
            result["date"]["month"] = months[int(date_parts[1]) - 1]

    # Intent
    result["intent"] = {"book": False, "predict": False}

    for token in doc:
        if token.text.lower() in ["travel", "travels", "book", "booking", "bookings", "ticket"]:
            result["intent"]["book"] = True
        if token.text.lower() in ["return", "returning", "back"]:
            result["intent"]["return"] = True

    return result


if __name__ == "__main__":
    text = "Hi, I'd like to book a ticket from London to Liverpool at 9am on 05/01 and return on the 4th of may"
    res = get_result(text)
    print(res)