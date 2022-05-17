import pandas as pd
import os


if __name__ == '__main__':
    dfs = []
    for f in os.listdir("clean"):
        df = pd.read_csv("clean/" + f, error_bad_lines=False)
        dfs.append(df)

    data = pd.concat(dfs, ignore_index=True)
    print(data)
