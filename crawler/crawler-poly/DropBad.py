import pandas as pd
import os


def parse(file_name):
    data = pd.read_csv("output/" + file_name, error_bad_lines=False)
    raw_size = data.shape[0]

    # print(data.columns)

    data.drop_duplicates("crossTxHash", keep='first', inplace=True)
    data = data.dropna(axis=0, how='any')
    data = data[data["fromChainName"] != data["toChainName"]]
    data.sort_values(by="timeStr", inplace=True, ascending=False)

    cur_size = data.shape[0]
    data.to_csv("clean/" + file_name, index=0)

    print("{}, Raw size {}, current size {}".format(
        file_name, raw_size, cur_size))


if __name__ == "__main__":
    for file_name in os.listdir("output"):
        parse(file_name)
