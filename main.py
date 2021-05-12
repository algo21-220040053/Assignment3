import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pandas.plotting import register_matplotlib_converters
import statsmodels.api as sm
import tushare as ts


token = 'f6b511d8d4529f19319e1861edadda749e64a5b8573102deec80cfd8'
pro = ts.pro_api()


def cal_smb_hml(df):
    # 划分大小市值公司
    df['SB'] = df['circ_mv'].map(lambda x: 'B' if x >= df['circ_mv'].median() else 'S')
    # 求账面市值比：PB的倒数
    df['BM'] = 1 / df['pb']
    # 划分高、中、低账面市值比公司
    border_down, border_up = df['BM'].quantile([0.3, 0.7])
    border_down, border_up
    df['HML'] = df['BM'].map(lambda x: 'H' if x >= border_up else 'M')
    df['HML'] = df.apply(lambda row: 'L' if row['BM'] <= border_down else row['HML'], axis=1)
    # 组合划分为6组
    df_SL = df.query('(SB=="S") & (HML=="L")')
    df_SM = df.query('(SB=="S") & (HML=="M")')
    df_SH = df.query('(SB=="S") & (HML=="H")')
    df_BL = df.query('(SB=="B") & (HML=="L")')
    df_BM = df.query('(SB=="B") & (HML=="M")')
    df_BH = df.query('(SB=="B") & (HML=="H")')
    # 计算各组收益率
    R_SL = (df_SL['pct_chg'] * df_SL['circ_mv'] / 100).sum() / df_SL['circ_mv'].sum()
    R_SM = (df_SM['pct_chg'] * df_SM['circ_mv'] / 100).sum() / df_SM['circ_mv'].sum()
    R_SH = (df_SH['pct_chg'] * df_SH['circ_mv'] / 100).sum() / df_SH['circ_mv'].sum()
    R_BL = (df_BL['pct_chg'] * df_BL['circ_mv'] / 100).sum() / df_BL['circ_mv'].sum()
    R_BM = (df_BM['pct_chg'] * df_BM['circ_mv'] / 100).sum() / df_BM['circ_mv'].sum()
    R_BH = (df_BH['pct_chg'] * df_BH['circ_mv'] / 100).sum() / df_BH['circ_mv'].sum()
    # 计算SMB, HML并返回
    smb = (R_SL + R_SM + R_SH - R_BL - R_BM - R_BH) / 3
    hml = (R_SH + R_BH - R_SL - R_BL) / 2
    return smb, hml

def df_smb_hml():
    data = []
    df_cal = pro.trade_cal(start_date='20180101', end_date='20210331')
    df_cal = df_cal.query('(exchange=="SSE") & (is_open==1)')
    for date in df_cal.cal_date:
        df_daily = pro.daily(trade_date=date)
        df_basic = pro.daily_basic(trade_date=date)
        df = pd.merge(df_daily, df_basic, on='ts_code', how='inner')
        smb, hml = cal_smb_hml(df)
        data.append([date, smb, hml])
        print(date, smb, hml)

    df_tfm = pd.DataFrame(data, columns=['trade_date', 'SMB', 'HML'])
    df_tfm['trade_date'] = pd.to_datetime(df_tfm.trade_date)
    df_tfm = df_tfm.set_index('trade_date')
    df_tfm.to_csv('df_three_factor_model.csv')
    return df_tfm

def get_local_data():
    df = pd.read_csv('df_three_factor_model.csv')
    df = df.set_index('trade_date')
    return df

def get_stock():
    wanke = pro.daily(ts_code='000002.SZ', start_date='20180101', end_date='20210331')
    pingan = pro.daily(ts_code='601318.SH', start_date='20180101', end_date='20210331')
    maotai = pro.daily(ts_code='600519.SH', start_date='20180101', end_date='20210331')
    wanhua = pro.daily(ts_code='002415.SZ', start_date='20180101', end_date='20210331')
    keda = pro.daily(ts_code='002230.SZ', start_date='20180101', end_date='20210331')
    gzA = pro.index_daily(ts_code='399317.SZ', start_date='20180101', end_date='20210331')
    stock_list = [wanke, pingan, maotai, wanhua, keda, gzA]
    for stock in stock_list:
        stock.index = pd.to_datetime(stock.trade_date)
    df_stock = pd.concat([stock.pct_chg / 100 for stock in stock_list], axis=1)
    df_stock.columns = ['wanke', 'pingan', 'maotai', 'wanhua', 'keda', 'gzA']
    df_stock = df_stock.sort_index(ascending=True)
    return df_stock


def merge_df(stock,tfm):
    df = pd.merge(stock, tfm, left_index=True, right_index=True, how='inner')
    df = df.fillna(0)
    rf = 1.032 ** (1 / 360) - 1
    df = df - rf
    df = df['20180101':]
    return df


def visual_ana(df):
    sns.set()
    plt.figure(figsize=(8, 6))
    plt.title('相关系数统计图', fontsize=20)
    sns.heatmap(df.corr(), cmap='bwr')

    register_matplotlib_converters()
    plt.figure(figsize=(10, 5))
    for col in df.columns:
        plt.plot(df[col], label=col)
    plt.title('日收益率时序图', fontsize=20)
    plt.legend()

    plt.figure(figsize=(10, 5))
    for col in df.columns:
        plt.plot((df[col] + 1).cumprod() - 1, label=col)
    plt.title('累计收益率时序图', fontsize=20)
    plt.legend()

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()


def fama_model(df):
    stock_names = {
        'wanke': '万科A',
        'pingan': '中国平安',
        'maotai': '贵州茅台',
        'wanhua': '万华化学',
        'keda': '科大讯飞'
    }
    params = pd.DataFrame()
    for stock in ['wanke', 'pingan', 'maotai', 'wanhua', 'keda']:
        model = sm.OLS(df[stock], sm.add_constant(
            df[['gzA', 'SMB', 'HML']].values))
        result = model.fit()
        params[stock_names[stock]] = result.params
        print(stock_names[stock] + '\n')
        print(result.summary())
        print('\n\n')
    params.index = ['Alpha', '市场因子', '规模因子', '价值因子']
    params.loc['Alpha'] = params.loc['Alpha'] * 100
    return params


def fama_ana(params):
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(params.index.tolist())
            .add_yaxis("中国平安", params['中国平安'].round(3).tolist())
            .add_yaxis("贵州茅台", params['贵州茅台'].round(3).tolist())
            .add_yaxis("万华化学", params['万华化学'].round(3).tolist())
            .add_yaxis("科大讯飞", params['科大讯飞'].round(3).tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title="个股收益归因分析"))
    )
    bar.render()


if __name__ == '__main__':
    # df_tfm = df_smb_hml()
    df_tfm = get_local_data()
    df_stock = get_stock()
    df = merge_df(df_stock, df_tfm)
    visual_ana(df)
    params = fama_model(df)
    fama_ana(params)