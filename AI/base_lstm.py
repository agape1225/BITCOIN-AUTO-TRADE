from machine.bithumb_machine import BithumbMachine
from db.mongodb.mongodb_handler import MongoDBHandler
from AI.lstm_machine import LstmMachine
import datetime

def extract_close_prices(data):
    close_prices = [float(entry['close_price']) for entry in data]
    return close_prices

bithumbMachine = BithumbMachine()
lstmMachine = LstmMachine()
mongodbMachine = MongoDBHandler(db_name="AI", collection_name="actual_data")

data = mongodbMachine.find_items(db_name="AI", collection_name="actual_data")
data = list(data)
#data = extract_close_prices(data)
result = []
for i in range(0, len(data) - 15):
    chunk = data[i:i+15]
    result.insert(0, chunk)
result.reverse()
for i in result:
    print(i)

tmp = []
for i in result:
    print(i)
    data = extract_close_prices(i)
    data = lstmMachine.data_processing(data)
    result = lstmMachine.get_predict_value(data)
    one_day_data = {}
    date_string = i[-1]["timestamp"]  # 예시로 사용할 날짜 문자열
    date_format = "%Y-%m-%d"  # 날짜 형식을 지정합니다. 여기서는 "년-월-일" 형식입니다.
    one_day_data["timestamp"] = ( datetime.datetime.strptime(date_string, date_format) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    one_day_data["predicted_price"] = result + 0.0
    #print(one_day_data)
    mongodbMachine.insert_item(data=one_day_data, db_name="AI", collection_name="predicted_data")

# for i in tmp:
#     print(i)

# #하루치 데이터 저장
# data = bithumbMachine.get_last_data()
# recv = mongodbMachine.insert_item(data=data, db_name="AI", collection_name="actual_data")



#model 예측 과정
# past_data = mongodbMachine.find_items_for_db(db_name="AI", collection_name="actual_data")
# data = extract_close_prices(past_data)
# data.reverse()
# data = lstmMachine.data_processing(data)
# result = lstmMachine.get_predict_value(data)

# #예측된 값 저장
# one_day_data = {}
# one_day_data["timestamp"] = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
# one_day_data["predicted_price"] = result + 0.0
# mongodbMachine.insert_item(data=one_day_data, db_name="AI", collection_name="predicted_data")