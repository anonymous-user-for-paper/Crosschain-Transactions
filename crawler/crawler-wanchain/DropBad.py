import pandas as pd
import os


def parse(file_name):
    data = pd.read_csv("output/" + file_name, error_bad_lines=False)
    # print(data.columns)
    raw_size = data.shape[0]

    data.drop_duplicates("lockHash", keep='first', inplace=True)
    data.dropna()

    cur_size = data.shape[0]
    data.to_csv("clean/" + file_name, index=0)

    print("{}, Raw size {}, current size {}".format(
        file_name, raw_size, cur_size))


if __name__ == "__main__":
    for file in os.listdir("output"):
        parse(file)
