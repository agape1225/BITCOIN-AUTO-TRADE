from machine.bithumb_machine import BithumbMachine
from db.mongodb.mongodb_handler import MongoDBHandler
from AI.lstm_machine import LstmMachine

bithumbMachine = BithumbMachine()
lstmMachine = LstmMachine()
mongodbMachine = MongoDBHandler(db_name="AI", collection_name="actual_data")
#data = bithumbMachine.get_last_data()
#mongodbMachine.insert_items(datas=data,db_name="AI", collection_name="actual_data")

#data = bithumbMachine.get_last_data()
#mongodbMachine.insert_item(data=data, db_name="AI", collection_name="actual_data")
#print(data)

#database에서 15개의 데이터를 가지고옴
actual_data = mongodbMachine.find_items_for_db(db_name="AI", collection_name="actual_data")
for document in actual_data:
    print(document)
    
#역순으로
#종가만 뽑이먹기
#그걸로 학습 ㄱㄱ
#이걸로 학습 조지기
#lstmMachine.data_processing(actual_data)
