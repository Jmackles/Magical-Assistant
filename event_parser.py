import spacy

nlp = spacy.load("en_core_web_sm")

def parse_event_info(user_message):
    event_info = {
        "event_name": "",
        "event_date": "",
        "event_time": "",
        "location": "",
    }

    event_info["event_name"] = parse_event_name(user_message)
    event_info["event_date"], event_info["event_time"] = parse_date_time(user_message)
    event_info["location"] = parse_location(user_message)

    return event_info

def parse_event_name(user_message):
    # Your code for extracting event name here
    pass

def parse_date_time(user_message):
    parsed_date, parsed_time = "", ""
    doc = nlp(user_message)
    for ent in doc.ents:
        if ent.label_ == "DATE":
            parsed_date = ent.text
        elif ent.label_ == "TIME":
            parsed_time = ent.text
    return parsed_date, parsed_time

def parse_location(user_message):
    # Your code for extracting location here