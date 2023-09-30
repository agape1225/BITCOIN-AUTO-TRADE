from machine.bithumb_machine import BithumbMachine
from db.mongodb.mongodb_handler import MongoDBHandler

bithumbMachine = BithumbMachine()
mongodbMachine = MongoDBHandler(db_name="AI", collection_name="actual_data")
data = bithumbMachine.get_last_data()
mongodbMachine.insert_item(data=data, db_name="AI", collection_name="actual_data")
print(data)