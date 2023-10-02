from machine.bithumb_machine import BithumbMachine
from db.mongodb.mongodb_handler import MongoDBHandler

bithumbMachine = BithumbMachine()
mongodbMachine = MongoDBHandler(db_name="AI", collection_name="actual_data")

datas = bithumbMachine.get_all_data()

mongodbMachine.insert_items(datas=datas,db_name="AI", collection_name="actual_data")