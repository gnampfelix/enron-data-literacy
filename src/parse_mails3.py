#!/usr/bin/python3

import email.parser as parser
import pandas as pd
import numpy as np
import os

sent_mail_folder_names = ["sent_items", "_sent_mail", "_sent", "sent"]

def _read_maildir3(path):
    result_dict = {}
    people = os.listdir(path)
    for person in people:
        current_person_dict = {}
        personal_mailbox_path = os.path.join(path, person)
        folders = os.listdir(personal_mailbox_path)
        merged_folders = [value for value in folders if value in sent_mail_folder_names]
        for folder in merged_folders:
            current_folder_path = os.path.join(personal_mailbox_path, folder)
            result_dict.update(_read_folder3(current_folder_path))
    return result_dict

def _read_folder3(path):
    result = {}
    children = os.listdir(path)
    for child in children:
        child_path = os.path.join(path, child)
        if os.path.isdir(child_path):
            result.update(_read_folder3(child_path))
        else:
            with open(child_path, "rb") as f:
                message = parser.BytesParser().parse(f, headersonly=True)
                result[child_path] = {
                    "from": message["from"], 
                    "to": message["to"], 
                    "subject": message["subject"], 
                    "date": message["date"]}
    return result   
    
def parse_maildir3(path, strip_migration_duplicates=True):
    '''
    Parses the given path as the "maildir" of the Enron mail corpus.
    Returns a pandas.DataFrame. 
    Only the folders "sent_items", "_sent_mail", "_sent", "sent" of each maiblox
    are read, mails from @enron-addresses are stored in 
    the resulting dataframe. Mails with the same sender, subject and 
    date are considered duplocates, only the first encounter of this 
    mail is kept. If "strip_migration_duplicates" is set to True, 
    e-mails that differ only in hour, date or month are considered a
    migration duplicate and are also removed.
    '''
    df = pd.DataFrame(_read_maildir3(path)).transpose()
    df = df[df["from"].str.contains("enron.com", case=False)].drop_duplicates(subset=["from", "subject", "date"])
    df["date"] = pd.to_datetime(df["date"], utc=True)
    df = df[df["date"] > "1999-01-01"]
    df["week"] = df["date"].apply(lambda x: x.isocalendar()[1])
    df["year"] = df["date"].apply(lambda x: x.year)
    df["month"] = df["date"].apply(lambda x: x.month)
    df["seconds_since_midnight"] = df["date"].apply(lambda x: x.time().hour * 60 * 60 + x.time().minute * 60 + x.time().second)
    df["hour"] = df["date"].apply(lambda x: x.time().hour)
    df["minute"] = df["date"].apply(lambda x: x.time().minute)
    df["second"] = df["date"].apply(lambda x: x.time().second)
    if strip_migration_duplicates:
        df = df.sort_values(by="date").drop_duplicates(subset=["subject", "from", "minute", "second"],keep="first")
    return df
   