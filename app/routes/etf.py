from fastapi import APIRouter
import akshare as ak
import pandas as pd
import math
import database
import utils

router = APIRouter(
    prefix="/etf",
    # 标签
    tags=["etf"],
    # # 依赖项
    # dependencies=[Depends(get_token_header)],
    # 响应
    responses={404: {"description": "share Not found"}}
)

# 字段对应关系
field_mapping = {
    '代码':'code',
    '名称':'name',
    '最新价':'price',
    '涨跌幅':'percent',
    '涨跌额':'price_diff',
    '成交量':'trading_volume',
    '成交额':'trading_value',
    '振幅':'amplitude',
    '最高':'high',
    '最低':'low',
    '今开':'t_start',
    '昨收':'y_close',
    '量比':'volume_ratio',
    '换手率':'turnover_ratio',
    '市盈率-动态':'pe_ttm',
    '市净率':'ps',
    '总市值':'total_cap',
    '流通市值':'float_cap',
}


@router.get("/list")
async def curr():

    etf = ak.fund_etf_category_sina(symbol="ETF基金")

    codes = [ 'sz159605', 'sh588200', 'sz159995', 'sh512880', 'sh515790', 'sh512690', 'sz159869', 'sh512400', 
         'sh512660', 'sh512170', 'sh515030', 'sh516160', 'sz159819', 'sz159998']
    filtered_etf = etf.loc[etf['代码'].isin(codes), ]
    sorted_etf = filtered_etf.sort_values(by='涨跌幅', ascending=False)
    sorted_etf['成交额'] = sorted_etf['成交额'].apply(lambda x: "{:,}".format(x))
    sorted_etf.rename(columns=field_mapping, inplace=True)
    json_data = sorted_etf.to_dict('records')
    def replace_special_floats(obj):
        if isinstance(obj, dict):
            return {k: replace_special_floats(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_special_floats(i) for i in obj]
        elif isinstance(obj, float):
            if math.isnan(obj) or obj == float('inf') or obj == float('-inf'):
                return None
        return obj
    result = dict(data = json_data)
    return replace_special_floats(result)


@router.get("/history")
async def history(code:str, types:str):
    # sql = f"select * from share_history where code = '{code}' order by day desc limit 1000"
    # records = database.find_list(sql)
    # records = list(filter(lambda x : x['close'], records))

    if(code.startswith('0') or code.startswith('3')):
        code = "sz" + code
    elif(code.startswith('6')):
        code = "sh" + code
    daily_start = "20190101"
    records = ak.stock_zh_index_daily_em(symbol=code, start_date=daily_start)
    # print(records)
    closes = records['close']
    sma_5 = utils.calculate_sma(closes, 5) if len(closes) > 5 else []
    sma_20 = utils.calculate_sma(closes, 20) if len(closes) > 20 else []
    sma_60 = utils.calculate_sma(closes, 60) if len(closes) > 60 else []
    sma_120 = utils.calculate_sma(closes, 120) if len(closes) > 120 else []
    sma_250 = utils.calculate_sma(closes, 250) if len(closes) > 250 else []

    result = []
    print("records len", len(records))
    for index, r in records.iterrows():
        record = dict(day = r['date'], price = r['close'], volume = r['volume'])
        print(record)
        if len(sma_5) > index:
            record['sma5'] = sma_5[index]
        if len(sma_20) > index:
            record['sma20'] = sma_20[index]
        if len(sma_60) > index:
            record['sma60'] = sma_60[index]
        if len(sma_120) > index:
            record['sma120'] = sma_120[index]
        if len(sma_250) > index:
            record['sma250'] = sma_250[index]
        result.append(record)
      
    result = result[-200:]  
    return result


@router.get("/today")
async def today(code:str, types:str):
    pass