from fastapi import APIRouter
import akshare as ak
import math
import datetime as dt
import utils
import data

router = APIRouter(
    prefix="/share",
    # 标签
    tags=["share"],
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
    df = ak.stock_zh_a_spot_em()
    df.rename(columns=field_mapping, inplace=True)
    json_data = df.to_dict('records')
    def replace_special_floats(obj):
        if isinstance(obj, dict):
            return {k: replace_special_floats(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_special_floats(i) for i in obj]
        elif isinstance(obj, float):
            if math.isnan(obj) or obj == float('inf') or obj == float('-inf'):
                return None
        return obj
    
    summary = {"量" : format(df['trading_value'].sum(), ","), 
               "上涨" : len(df[df['percent']>=0]), 
               "下跌" : len(df[df['percent']<0]), 
               "涨超9" : len(df[df['percent']>=9]), 
               "跌超9" : len(df[df['percent']<=-9])}
    result = dict(data = json_data, summary = summary)

    return replace_special_floats(result)


@router.get("/tags")
async def tag():
    tags = []
    tags.append({"key":"Take", "names": ['新洁能', '捷佳伟创', ]})
    tags.append({"key":"Favorites", 
                 "names": ['北方华创', '兆易创新', '深南电路', '新易盛', '遥望科技', '新洁能', '中国核电', '中国建筑',
             '中际旭创', '晶方科技', '凯莱英', '金辰股份', '阳光电源', '赣锋锂业', '捷佳伟创',
             '宁德时代', '天齐锂业', '华友钴业', '泸州老窖', '贵州茅台', '中科曙光',
             '隆基绿能', '扬杰科技', '航发动力', '中航重机', '潍柴重机', '吉比特', '赛力斯']})
    tags.append({"key":"有色", "names": ['兖矿能源',]})
    tags.append({"key":"Semi", "names": ['北方华创', '兆易创新', '中芯国际', '新洁能', '寒武纪-U', '晶方科技',
             '长电科技', '扬杰科技', '闻泰科技', '沪硅产业', '华润微', '士兰微']})
    tags.append({"key":"Solar", "names": ['隆基绿能', '阳光电源', '金辰股份', '天合光能', '捷佳伟创',
        '东方日升', '爱旭股份', '晶澳科技', '通威股份', '固德威', '弘元绿能', '东方电缆']})
    tags.append({"key":"Consume", "names": ['泸州老窖', '重庆啤酒', '贵州茅台', '五 粮 液', '山西汾酒', '牧原股份']})
    tags.append({"key":"CPO", "names": ['新易盛', '中际旭创', '剑桥科技', '光库科技', '光迅科技', '天孚通信', '润和软件']})
    tags.append({"key":"医药", "names": ['凯莱英', '药明康德', '泰格医药', '康龙化成', '迈瑞医疗', '以岭药业']})
    tags.append({"key":"军工", "names": ['中航重机', '航发动力', '中航西飞', '航天彩虹', ]})
    tags.append({"key":"PCB", "names": ['沪电股份', '深南电路', '生益电子', '领益智造', '歌尔股份', '欣旺达', '东山精密', '立讯精密']})
    tags.append({"key":"国企蓝筹", "names": ['招商银行', '工商银行', '建设银行', '农业银行', '中国电信', '中国移动', '中国联通', '中国石油', '中国建筑', ]})
    tags.append({"key":"Game", "names": ['三七互娱', '吉比特', '完美世界', '昆仑万维', '世纪华通', '姚记科技', '中青宝', '神州泰岳', '游族网络', '恺英网络', '冰川网络']})
    # tags.append({"key":"金融", "names": []})

    hushen300_df = data.get_hushen300_df()
    names = hushen300_df[1]
    tags.append({"key":"沪深300", "names": names.values.tolist()})

    chuang50_df = data.get_chuang50_df()
    names = chuang50_df[1]
    tags.append({"key":"创50", "names": names.values.tolist()})  

    return tags


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

    print("sma_5", len(sma_5))
    print("sma_20", len(sma_20))
    print("sma_60", len(sma_60))
    print("sma_120", len(sma_120))
    print("sma_250", len(sma_250))

    result = []
    print("records len", len(records))
    for index, r in records.iterrows():
        record = dict(day = r['date'], price = r['close'], volume = r['volume'])
        if len(sma_5) > index - 4 and index > 3:
            record['sma5'] = sma_5[index - 4]
        if len(sma_20) > index - 19 and index > 18:
            record['sma20'] = sma_20[index - 19]
        if len(sma_60) > index - 59 and index > 58:
            record['sma60'] = sma_60[index - 59]
        if len(sma_120) > index - 119 and index > 118:
            record['sma120'] = sma_120[index - 119]
        if len(sma_250) > index - 249 and index > 248:
            record['sma250'] = sma_250[index - 249]
        result.append(record)
        
    result = result[-200:]  
    for r in result:
        print("**" , r)
    return result


@router.get("/today")
async def today(code:str, types:str):
    pass


@router.get("/minate")
async def detail(code:str):
    start = dt.date.today() + dt.timedelta(days=-5)
    period = "5"
    stock_zh_index_daily_em_df = ak.stock_zh_a_hist_min_em(symbol=code, start_date=start.strftime("%Y%m%d"), period=period)
    closes = stock_zh_index_daily_em_df['close']