from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np


class LstmMachine:
    def __init__(self):
        """
        가장 먼저 호출되는 메서드
        config.ini에서 정보를 읽어옴
        """
        # self.model_path = "static/BITCOIN_MODEL_VER1.h5"
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = load_model("./BITCOIN_MODEL_VER1.h5", compile=False)

    """def get_model(self, current_data):

        loaded_model = load_model(self.model_path, compile=False)
        predicted = loaded_model.predict(current_data)
        #ret = load_model.predict(current_data)

        return predicted"""

    def get_predict_value(self, current_data):
        """
        모델을 불러와서 학습을 진행하고 결과값을 return
        """
        # model = self.get_model(current_data)

        predicted_value = self.model.predict(current_data)
        predicted_value = self.scaler.inverse_transform(predicted_value)
        # predicted_value = model.predict(current_data)
        return predicted_value[0][0]

    def data_processing(self, raw_data):
        """
        학습을 위한 전처리 진행
        """

        final_data = []

        for i in raw_data:
            tmp = []
            tmp.append(i)
            final_data.append(tmp)

        final_data = self.scaler.fit_transform(
            np.array(final_data).reshape(-1, 1)
        )

        final_data = np.array([final_data])

        return final_data