import json
import os
import pandas as pd


def get_hushen300_json():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "data", "hushen300.json")
    with open(file_path) as f:
        content = f.readlines()
        json_data = json.loads("\n".join(content))
        return json_data


def get_hushen300_df():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "data", "hushen300.json")
    df = pd.read_json(file_path)
    return df


def get_chuang50_df():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "data", "chuang50.json")
    df = pd.read_json(file_path)
    return df


def refresh_hushen300():
    dict = {
        "399673": "chuang50",
        "000300": "hushen300",
    }
    import akshare as ak
    
    symbol = "000300"
    filename = dict[symbol]
    
    index_stock_cons_df = ak.index_stock_cons(symbol=symbol)
    with open(f"./share/data/{filename}.json", 'w') as f:
        f.write(index_stock_cons_df.to_json(orient='values'))


if __name__ == '__main__':
    # refresh_hushen300()
    
    df = get_hushen300_df()
    print(df[1])
    print(df.iloc[:, 1])
    print(df.loc[1])


