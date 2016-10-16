from __future__ import print_function
import urllib2

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    # Setting the default website and category
    session_attributes['website'] = "seattletimes"
    session_attributes['category'] = "nation"
    card_title = "Welcome"
    speech_output = "Welcome to Light Bringer! " \
                    "What do you want to do? " \
                    "Get News about a topic or Get description of the Image ?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "What do you want to do?" \
                    "Get News about a topic or Get description of the Image ?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Light Bringer " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_selected_website_attributes(setWebSiteTo):
    return {"website": setWebSiteTo}

def create_selected_category_attributes(setCategoryTo):
    return {"category": setCategoryTo}

def set_website_from_session(intent, session):
    """ Sets the website in the session and prepares the speech to reply to the
        user.
    """
    card_title = intent['name']
    session_attributes = session.get('attributes', {})
    should_end_session = False

    if 'website' in intent['slots']:
        setWebSiteTo = intent['slots']['website']['value']
        session_attributes = create_selected_website_attributes(setWebSiteTo)
        speech_output = "You have successfully set your interested website to " + \
                        setWebSiteTo + \
                        ". Now you can ask to get news "
        reprompt_text = "You can now ask to get news "
    else:
        speech_output = "I'm not sure what the website you mentioned " \
                        "Please try again."
        reprompt_text = "I'm not sure what the website you mentioned " \
                        "You can set the website by mentioning, " \
                        "set website to Seattle times" 
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_website_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    reprompt_text = None

    if session.get('attributes', {}) and "website" in session.get('attributes', {}):
        website = session['attributes']['website']
        speech_output = "Your website is set to " + website + "."
        should_end_session = False
    else:
        speech_output = "I'm not sure what your website is set to!" \
                        "You can say, set website to your favorite website."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def get_category_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    reprompt_text = None

    if session.get('attributes', {}) and "category" in session.get('attributes', {}):
        category = session['attributes']['category']
        speech_output = "Your category is set to " + category + "."
        should_end_session = False
    else:
        speech_output = "I'm not sure what your category is set to!" \
                        "You can say, get news about something and the category is automatically updated." 
        reprompt_text = "I'm not sure what your category is set to!" \
                        "You can say, get news about something and the category is automatically updated."          
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))




def get_image_response(intent, session):
    session_attributes = {}
    reprompt_text = None
    speech_output = "The image is related to " + urllib2.urlopen("http://995b8d08.ngrok.io/info").read()

    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def get_news_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    # print(session_attributes);
    reprompt_text = None
    # website = session['attributes']['website']
    # speech_output = "Your website is set to " + website + "."

    if session.get('attributes', {}) and "website" in session.get('attributes', {}):
        website = session['attributes']['website']
        speech_output = "Your website is set to " + website + "."
        should_end_session = False
        # session_attributes['website'] = website
        if 'category' in intent['slots']:
            category = intent['slots']['category']['value']
            # speech_output = "Your website is set to " + website + " and category is set to" + category
            print("http://995b8d08.ngrok.io/" + website.lower() + "/" + category.lower() + "/")
            speech_output = "The headlines in " + website + " about " + category + " are " + urllib2.urlopen("http://995b8d08.ngrok.io/" + website.lower() + "/" + category.lower() + "/").read()
            should_end_session = False
            # session_attributes['category'] = category
        else:
            speech_output = "Your website category is set to something I dont know"
            should_end_session = False
    else:
        speech_output = "Your website is set to something I dont know"
        should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetNews":
        return get_news_from_session(intent,session)
    elif intent_name == "SetNews":
        return set_news_from_session(intent,session)
    elif intent_name == "SetNewsWebsite":
        return set_website_from_session(intent, session)
    elif intent_name == "GetNewsWebsite":
        return get_website_from_session(intent, session)
    elif intent_name == "GetCategory":
        return get_category_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "GetImageInformation":
        return get_image_response(intent,session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
