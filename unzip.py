import sys
import os
import zipfile
from datetime import datetime

import pandas as pd
from os.path import isdir

OUTPUT_DIR = "clean"


def format_dataframe(df):

    df["Open time"] = pd.to_datetime(df['Open time'], unit='ms')
    df = df.set_index("Open time")
    df = df.drop([
        "Close time",
        "Quote asset volume",
        "Number of trades",
        "Taker buy base asset volume",
        "Taker buy quote asset volume",
        "Ignore"
    ], axis=1)

    df = df.sort_index(ascending=True)

    return df


if __name__ == '__main__':
    directory = str(sys.argv[1])

    if isdir(directory):
        files = [file for file in os.listdir(directory) if file[-3:] == "zip"]

        pd_dataframes = []

        for file in files:
            unzipped_folder = zipfile.ZipFile(directory + "/" + file, 'r')
            csv_file_name = unzipped_folder.namelist()[0]
            pd_dataframe = pd.read_csv(
                unzipped_folder.open(csv_file_name), header=None
            )

            pd_dataframe.to_csv("test.csv", index=False)

            pd_dataframe.columns = \
                [
                    "Open time",
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Volume",
                    "Close time",
                    "Quote asset volume",
                    "Number of trades",
                    "Taker buy base asset volume",
                    "Taker buy quote asset volume",
                    "Ignore"
                ]

            pd_dataframes.append(pd_dataframe)

        pd_concat = pd.concat(pd_dataframes, axis=0)

        if not isdir(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)

        pd_formatted = format_dataframe(pd_concat)
        output_name = directory.replace("/", "-")
        pd_formatted.to_csv(f"{OUTPUT_DIR}/{output_name}")

    else:
        raise Exception(
            f"'{directory}' is not a directory. "
            f"Use this command if you follow the tutorial "
            f"'python3 unzip.py data/spot/monthly/klines/BNBBUSD/1w'"
        )
