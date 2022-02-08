import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-BTC", count = 14)
print(df)

# 변동폭(고가 - 저가) * k 값
df['range'] = (df['high'] - df['low']) * 0.5

# target = 매수가, range컬럼은 한칸씩 밑으로 내림(shift(1))
df['target'] = df['open'] + df['range'].shift(1)

## fee = 0.0032
# ror = 수익률, 
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'], ## - fee
                     1)
# cumprod = 누적 곱 계산
df['hpr'] = df['ror'].cumprod()

# dd = Draw Down = 누적 최대값과 현재 hpr 차이 / 누적최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx")