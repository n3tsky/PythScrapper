# coding=utf-8
from tabulate import tabulate
from time import sleep

import settings
from functions.http import *
from functions.generic import *

OFFSET_VALUE=100

### API calls
def hunterIO_call_account(HTTP_REQ):
    HTTP_REQ["url"] = "%s?api_key=%s" % (HUNTERIO_ACCOUNT_URL, HUNTERIO_API_KEY)
    http_code, response = http_get_json(HTTP_REQ)
    return response

def hunterIO_call_domain_search(HTTP_REQ, domain, offset=0, limit=100):
    HTTP_REQ["url"] = "%s?api_key=%s&domain=%s&offset=%d&limit=%d" % (HUNTERIO_DOMAIN_URL, HUNTERIO_API_KEY, domain, offset, limit)
    http_code, response = http_get_json(HTTP_REQ)
    return response

### /API calls

# Parsing
def hunterIO_parse_info(data):
    print("ok")
    # Get emails
    #emails = dict_check_and_get(data, "emails")
    #print(emails)
    #if emails != None:
    #    for e in emails:
    #        display_value_from_dict(e, "value", " - Email: ")
    #        display_value_from_dict(e, "type", " - Email type: ")
    #        display_value_from_dict(e, "confidence", " - Confidence: ")
    #        display_value_from_dict(e, "first_name", " - First name: ")
    #        display_value_from_dict(e, "last_name", " - Last name: ")
    #        display_value_from_dict(e, "phone_number", " - Phone: ")
    #        print()
    #print(json_data)

def hunterIO_fetch_domain_info(HTTP_REQ, domain):
    # Get data
    current_offset = OFFSET_VALUE
    json_data = hunterIO_call_domain_search(HTTP_REQ, domain) # Default offset = 0

    # Get data
    data = dict_check_and_get(json_data, "data")
    if data != None:
        display_value_from_dict(data, "webmail", " - Webmail: ")
        display_value_from_dict(data, "pattern", " - Mail pattern: ")
        display_value_from_dict(data, "organization", " - Organization: ")
        # Parse info
        #hunterIO_parse_info(data)

    # Get meta
    meta = dict_check_and_get(json_data, "meta")
    if meta != None:
        total_people = dict_check_and_get(meta, "results")
        display_value_from_dict(meta, "results", " - results: ")
        display_value_from_dict(meta, "limit", " - limit: ")
        # Loop and fetch people
        while total_people > current_offset:
            print("[*] People: %d - %d" % (current_offset, total_people))
            # Query and parse
            #json_data = hunterIO_call_domain_search(HTTP_REQ, domain, offset=current_offset)
            # Parse info
            #hunterIO_parse_info(data)
            current_offset += OFFSET_VALUE


# Display info about account related to API key
def hunterIO_display_account_info(data_info):
    print("[*] HunterIO account info:")
    display_value_from_dict(data_info, "email", " - Email: ")
    display_value_from_dict(data_info, "plan_name", " - Account type: ")
    display_value_from_dict(data_info, "reset_date", " - Reset date: ")
    display_value_from_dict(data_info, "calls", " - Calls: ")

# Check accounts (calls /account)
def hunterIO_check_account(HTTP_REQ):
    result = hunterIO_call_account(HTTP_REQ)
    if result != None:
        errors = dict_check_and_get(result, "errors")
        if errors != None: # Not good
            details =  dict_check_and_get(errors[0], "details")
            print("[!] Error: %s " % details)
        else:
            data = dict_check_and_get(result, "data")
            hunterIO_display_account_info(data)
            return 1
    return 0

# Check if an API key has been set by user
def hunterIO_check_basic():
    if HUNTERIO_API_KEY != "":
        return 1
    else:
        return 0

# Perform checks
def hunterIO_checks(HTTP_REQ):
    print("[*] HunterIO: Checking API key\n")
    if not (hunterIO_check_basic() and hunterIO_check_account(HTTP_REQ)):
        exiting("Error while checking HunterIO API key (please provide a valid API key)")