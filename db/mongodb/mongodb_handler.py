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
            self._client = MongoClient(host='localhost', port=27017)

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

    def insert_item(self, data, db_name=None, collection_name=None):
        """

        :param data:
        :param db_name: 데이터베이스에 해당하는 이름
        :param collection_name: 데이터베이스에 속하는 콜렉션
        :return: 입력 완료된 문서의 ObjectId를 반환한다.
        """

        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

        return self._collection.insert_one(data).inserted_id

    def insert_items(self, datas, db_name=None, collection_name=None):
        """
        MongoDB에 다수의 문서를 입력하기 위한 메소드이다.
        :param datas:
        :param db_name: MongoDB에서 데이터베이스에 해당하는 이름을 받는다.
        :param collection_name: 데이터베이스에 속하는 콜렉션 이름을 받는다.
        :return: 입력 완료된 문서의 ObjectId리스트를 반환한다.
        """

        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection_name = self._db[collection_name]
        return self._collection.insert_many(datas).inserted_ids

    def find_items(self, condition=None, db_name=None, collection_name=None):
        """
        MongoDB에서 다수의 문서를 검색하기 위한 메소드이다.
        :param condition: 검색 조건을 딕셔너리 형태로 받는다
        :param db_name: MongoDB에서 데이터베이스에 해당하는 이름을 받는다.
        :param collection_name: 데이터베이스에 속하는 콜렉션 이름을 받는다.
        :return: 커서를 반환한다.
        """
        if condition is None:
            condition = {}
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

        return self._collection.find(condition, cursor_type=CursorType.EXHAUST)

    def find_item(self, condition=None, db_name=None, collection_name=None):
        """
        MongdDB에서 하나의 문서를 검색하기 의한 메소드입니다.
        :param condition: 검색 조건을 딕셔너리 형태로 받는다
        :param db_name: MongoDB에서 데이터베이스에 해당하는 이름을 받는다
        :param collection_name: 데이터베이스에 속하는 콜렉션 이름을 받는다
        :return: 만약 검색된 문서가 있다면 문서의 내용을 반환한다
        """

        if condition is None:
            condition = {}
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.find_one(condition)

    def delete_items(self, condition=None, db=None, collection=None):
        """
        Mongodb에서 다수의 collection을 삭제한다.
        :param condition: 삭제 조건을 딕셔너리 형태로 받는다.
        :param db: Mongodb에서 데이터베이스에 해당하는 이름을 받는다.
        :param collection: 데이터베이스에 속하는 collection이름을 받는다.
        :return: PyMondo의 문서의 삭제 결과 객체인 DeleteResult가 반환된다.
        """

        if condition is None:
            raise Exception("Need to condition")
        if db is not None:
            self._db = self._client[db]
        if collection is not None:
            self._collection = self._db[collection]
        return self._collection.delete_many(condition)

    def update_items(self, condition=None, update_value=None, db_name=None, collection_name=None):
        """
        MongoDB에서 다수의 문서를 갱신하기 위한 메소드이다.
        :param condition: 업데이트 조건을 딕셔너리 형태로 받는다.
        :param update_value: 업데이트하고자 하는 값을 딕셔너리 형태로 받는다.
        :param db_name: MongoDB에서 데이터베이스에 해당하는 이름을 받는다.
        :param collection_name: 데이터베이스에 속하는 콜렉션 이름을 받는다.
        :return: PyMongo의 문서의 업데이트 결과 객체인 UpdateResult가 반환된다.
        """
        if condition is None:
            raise Exception("Need to condition")
        if update_value is None:
            raise Exception("Need to update value")
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.update_many(filter=condition, update=update_value)

    def aggregate(self, pipeline=None, db_name=None, collection_name=None):
        """
        MongoDB의 집계 작업을 위한 메소드이다.
        :param pipeline: 갱신 조건을 딕셔너리 형태로 받는다.
        :param db_name: MongoDB에서 데이터베이스에 해당하는 이름을 받는다.
        :param collection_name:  데이터배이스에 속하는 콜렉션 이름을 받는다.
        :return: PyMongo의 CommandCursor를 반환한다.
        """

        if pipeline is None:
            raise Exception("Need to pipeline")
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.aggregate(pipeline)
