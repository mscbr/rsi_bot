import websocket, json, pprint, talib
import numpy as np 

SOCKET = 'wss://stream.binance.com/ws/ethusdt@kline_1m'

RSI_PERIOD = 14
RSI_OVB = 70
RSI_OVS = 30
SYMBOL = 'ETHUSD'
QUANTITY = 0.05


closes = []
in_position = False

def on_open(ws):
  print('openned connection')

def on_close(ws):
  print('closed connection')

def on_message(ws, message):
  global closes
  json_message = json.loads(message)
  
  candle = json_message['k']
  pprint.pprint(candle['c'])

  if (candle['x']):
    print('candle closed at {}'.format(candle['c']))
    closes.append(float(candle['c']))
    print(closes)

    if len(closes) > RSI_PERIOD:
      np_closes = np.array(closes)
      rsi = talib.RSI(np_closes, RSI_PERIOD)
      last_rsi = rsi[-1]
      print("the current RSI {}".format(last_rsi))

      if last_rsi > RSI_OVB:
        if in_position:
          print("SELL!!!", candle['c'])
          in_position=False
          # put sell logic here
        else:
          print("Already in position...zzZZzz...")
      
      if last_rsi < RSI_OVS:
        if in_position:
          print("Already in position...zzZZzz...")
        else:
          print("BUY!!!", candle['c'])
          in_position=True;
          # put order logic here  
    

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

ws.run_forever()