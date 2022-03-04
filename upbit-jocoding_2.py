import time
import pyupbit
import datetime

access = "aaa"
secret = "bbb"
interval = "minute240"

def get_target_price(ticker, interval, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval = interval, count=14)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker, interval):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC", interval)
        end_time = start_time + datetime.timedelta(days=1) - datetime.timedelta(seconds=5)

        # 9:00 < 현재 < 8:59:50
        if start_time < now < end_time:
            target_price = get_target_price("KRW-BTC", interval, 0.15)
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
        elif now > end_time:
            btc = get_balance("BTC")
            upbit.sell_market_order("KRW-BTC", btc)
            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
