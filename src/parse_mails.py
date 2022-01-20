#!/usr/bin/python3

import pandas as pd
import numpy as np
import re
import os
import dateutil.parser as parser

sent_mail_folder_names = ["sent_items", "_sent_mail", "_sent", "sent"]
date_field_regex = re.compile(r"^Date:")

def _read_maildir(path):
    result_dict = {}
    people = os.listdir(path)
    for person in people:
        current_person_dict = {}
        personal_mailbox_path = os.path.join(path, person)
        folders = os.listdir(personal_mailbox_path)
        merged_folders = [value for value in folders if value in sent_mail_folder_names]
        for folder in merged_folders:
            current_folder_path = os.path.join(personal_mailbox_path, folder)
            current_person_dict.update(_read_folder(current_folder_path, person))
        result_dict.update(current_person_dict)
    return result_dict
        
def _read_folder(path, person):
    result = {}
    children = os.listdir(path)
    for child in children:
        child_path = os.path.join(path, child)
        if os.path.isdir(child_path):
            result.update(_read_folder(child_path, person))
        else:
            with open(child_path, "r", encoding="utf8", errors='ignore') as f:
                lines = f.readlines()
                matched_lines = list(filter(date_field_regex.search, lines))
                if len(matched_lines) != 0:
                    result[child_path] = {"name": person, "date": matched_lines[0]}
    return result
   
def _parse_date(payload):
    return parser.parse(payload.strip()[5:].strip())

def parse_maildir(path):
    df = pd.DataFrame(_read_maildir(path)).transpose()   
    df["parsed_date"] = df["date"].apply(_parse_date)
    df["time"] = df["parsed_date"].apply(lambda x: x.time())
    df["day"] = df["parsed_date"].apply(lambda x: x.date())
    df["tz"] = df["parsed_date"].apply(lambda x: x.tzname())
    return df
