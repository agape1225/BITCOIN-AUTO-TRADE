from pymongo import MongoClient
from pymongo.cursor import CursorType
import configparser
from db.base_handler import DBHandler

class MongoDBHandler(DBHandler):

    """
    PyMongo를 래핑해서 사용하는 클래스이다. DBHandler 추상 클래스를 상속한다.
    리모트 DB와 로컬 DB를 모두 사용할 수 있도록 __init__에서 mode로 구분한다.
    """

    def __init__(self, mode="local", db_name=None, collection_name=None):
        """
        MongoDBHandler __init__ 구현부
        :param mode: 로컬 DB인지 리모트 DB인지를 구분한다.
        :param db_name: MongoDB에서 데이터베이스에 해당하는 이름을 받는다.
        :param collection_name: 데이터베이스에 속하는 콜렉션 이름을 받는다.
        """

        if mode == "remote":
            self._client = MongoClient("mongodb://{user}:{password}@{remote_host}:{port}".format(**self.db_config))
        elif mode == "local":
            self._client = MongoClient("mongodb://{user}:{password}@{local_ip}:{port}".format(**self.db_config))

        self._db = self._client[db_name]
        self._collection = self._db[collection_name]

    def set_db_collection(self, db_name=None, collection_name=None):
        """

        MongoDB에서 작업하려는 데이터베이스와 콜렉션을 변경할 때 사용

        :param db_name: 데이터베이스에 해당하는 이름을 입력받는다
        :param collection_name: 데이터베이스에 속하는 컬랙션을 입력받는다
        :return: None
        """

        if db_name is None:
            raise Exception("Need to dbname name")

        self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

    def get_current_db_name(self):
        """

        현재 MongoDB에서 작업 중인 데이터베이스의 이름을 반환한다.

        :return: self._db.name
        """
        return self._db.name

    def get_current_collection_name(self):
        """

        현재 MongoDB에서 작업 중인 콜렉션의 이름을 반환한다.

        :return: self._collection.name: 현재 사용중인 콜렉션의 이름을 반환
        """
        return self._collection.name

    def insert_items(self):
        pass

    def find_items(self):
        pass

    def find_item(self):
        pass

    def delete_items(self):
        pass

    def update_items(self):
        pass

    def aggregate(self):
        pass