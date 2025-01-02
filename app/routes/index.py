from fastapi import APIRouter
import akshare as ak
import pandas as pd
import math


router = APIRouter(
    prefix="/index",
    # 标签
    tags=["index"],
    # # 依赖项
    # dependencies=[Depends(get_token_header)],
    # 响应
    responses={404: {"description": "share Not found"}}
)


@router.get("/ka")
async def curr():
    return {"message": "Hello World"}


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
async def get_index():
    sh_index_spot_em_df = ak.stock_zh_index_spot_em(symbol="上证系列指数")
    sz_index_spot_em_df = ak.stock_zh_index_spot_em(symbol="深证系列指数")

    combined_df = pd.concat([sh_index_spot_em_df, sz_index_spot_em_df], axis=0)
    combined_df['成交额'] = combined_df['成交额'].apply(lambda x: "{:,}".format(x))

    codes = [ '000001', '000300', '399673', "399006", '399001', '000126', '000852', '899050']
    columns = ['代码', '名称', '最新价', '涨跌幅', '成交量', '成交额', '振幅', '量比']
    sorted_etf = combined_df.loc[combined_df['代码'].isin(codes), columns]
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