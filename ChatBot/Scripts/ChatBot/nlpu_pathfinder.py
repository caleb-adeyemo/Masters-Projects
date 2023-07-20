import spacy
import re

nlp = spacy.load('en_core_web_sm')  # lg

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
    message = nlp(message)

    result = {}

    # Greetings
    if greeting_regex.search(str(message)):
        result["greeting"] = True


    # Location
    for ent in message:
        if ent.ent_type_ == "GPE":
            ans_list = []
            for ancestor in ent.ancestors:
                ans_list.append(ancestor.text)
            if any("from" in word for word in ans_list):    # Change hard coding of "from" to more departure prepositions
                result["start_loc"] = ent.text
            elif any("to" in word for word in ans_list):    # Change hard coding of "to" to more arrival prepositions
                result["end_loc"] = ent.text

    # Time
    for ent in message:
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
    for ent in message:
        # get the month
        if ent.text in months:
            result["date"]["month"] = ent.text
        # get the day
        elif re.match(r'\d+th', str(ent.text)):  # Look for the "th" in the sentence
            day = re.sub(r"th\b", "", str(ent.text))
            result["date"]["day"] = int(day)
        elif re.match(r'\d{1,2}/\d{1,2}', ent.text):  # Look for 12/06 pattern
            date_parts = ent.text.split('/')
            result["date"]["day"] = int(date_parts[0])
            result["date"]["month"] = months[int(date_parts[1]) - 1]

    # Intent
    result["intent"] = {"book": False, "return": False}

    for ent in message:
        if ent.text in ["travel", "travels", "book", "booking", "bookings", "ticket"]:
            result["intent"]["book"] = True
        if ent.text in ["return", "returning", "back"]:
            result["intent"]["return"] = True

    return result


if __name__ == "__main__":
    text = "Hi, I'd like to book a ticket from London to Liverpool at 9am on 05/01 and return on the 4th of may"
    res = get_result(text)
    print(res)













