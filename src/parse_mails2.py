#!/usr/bin/python3

import email.parser as parser
import pandas as pd
import numpy as np
import re
import os

def _read_folder2(path):
    result = {}
    children = os.listdir(path)
    for child in children:
        child_path = os.path.join(path, child)
        if os.path.isdir(child_path):
            result.update(_read_folder2(child_path))
        else:
            with open(child_path, "rb") as f:
                message = parser.BytesParser().parse(f, headersonly=True)
                result[child_path] = {
                    "from": message["from"], 
                    "to": message["to"], 
                    "subject": message["subject"], 
                    "date": message["date"]}
    return result   
    
def parse_maildir2(path, strip_migration_duplicates=True):
    '''
    Parses the given path as the "maildir" of the Enron mail corpus.
    Returns a pandas.DataFrame. 
    All folders are read, mails from @enron-addresses are stored in 
    the resulting dataframe. Mails with the same sender, subject and 
    date are considered duplocates, only the first encounter of this 
    mail is kept. If "strip_migration_duplicates" is set to True, 
    e-mails that differ only in hour, date or month are considered a
    migration duplicate and are also removed.
    '''
    df = pd.DataFrame(_read_folder2(path)).transpose()
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
   