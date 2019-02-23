#! /usr/bin/env python

import argparse
import pandas as pd
import json
import os


def dictify_df(df:pd.DataFrame)->dict:
    df = json.loads(df.set_index('id').to_json(orient='index'))
    df = {key: value["value"] for key, value in df.items()}
    return df


def filter_df_on_key(df:pd.DataFrame, key:str)-> pd.DataFrame:
    return df[df.id.str.startswith(key)]


def parse_authors(df_input:pd.DataFrame) -> pd.DataFrame:
    df_authors = filter_df_on_key(df_input, "globalAuthor")

    def json_string_to_series(text): return pd.Series(json.loads(text))

    df_authors = pd.concat([df_authors.id, df_authors.value.apply(json_string_to_series)], axis=1)
    df_authors.name = df_authors.name.fillna("")
    df_authors.padIDs = df_authors.padIDs.fillna("{}")
    df_authors.id = df_authors.id.apply(lambda id: id.replace("globalAuthor:a.", ""))

    return df_authors


def parse_comments(df_input:pd.DataFrame) -> dict:
    df_comments = filter_df_on_key(df_input, "comments")

    def jsonify_text(text): return json.loads(text)

    df_comments = pd.concat([df_comments.id, df_comments.value.apply(jsonify_text)], axis=1)
    df_comments.id = df_comments.id.apply(lambda id: id.replace("comments:", ""))

    comments_info = dictify_df(df_comments)
    return comments_info


def parse_pads(df_input:pd.DataFrame)-> dict:
    df_pads = filter_df_on_key(df_input, "pad")

    def extract_content(text):
        pad_json = json.loads(text)
        return pd.Series(pad_json["atext"]["text"])

    df_pads = pd.concat([df_pads.id, df_pads.value.apply(extract_content)], axis=1)
    df_pads.columns = ["id", "value"]
    df_pads.id = df_pads.id.apply(lambda id: id.replace("pad:", ""))

    pads_info = dictify_df(df_pads)
    return pads_info


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_dump_file", help="the path leading to the dump of etherpad database")
    parser.add_argument("out_dir", help="the directory to use to save data")
    args = parser.parse_args()

    csv_file = args.csv_dump_file
    out_dir = args.out_dir
    pads_dir = os.path.join(out_dir, "pads")
    comments_dir = os.path.join(out_dir, "comments")

    # Getting the whole file like this
    with open(file=csv_file, mode="r", encoding="ISO-8859-1") as fh:
        lines = fh.read().splitlines()

    # Removing header if present
    if "key," in lines[0]:
        del lines[0]

    # Splitting on first comma
    tuples = list(map(lambda record: record.split(",", maxsplit=1), lines))

    # Getting the data-frame
    df_input = pd.DataFrame(tuples, columns=["id", "value"])

    # Parsing it
    df_authors = parse_authors(df_input)
    comments_info = parse_comments(df_input)
    pads_info = parse_pads(df_input)

    # Dumping stuff
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(pads_dir, exist_ok=True)
    os.makedirs(comments_dir, exist_ok=True)

    df_authors.to_csv(os.path.join(out_dir, "authors.csv"), index=False)

    for pad_name, comments in comments_info.items():
        with open(os.path.join(comments_dir, f"{pad_name}.json"),"w") as fh:
            json.dump(comments, fh)

    for pad_name, content in pads_info.items():
        with open(os.path.join(pads_dir, f"{pad_name}.txt"),"w") as fh:
            fh.write(content)
