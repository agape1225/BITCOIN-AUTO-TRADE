import tensorflow as tf

# LSTM 모델 정의
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(64, input_shape=(10, 1)),  # LSTM 레이어, 64개의 유닛, 입력 형태 (10, 1)
    tf.keras.layers.Dense(1)  # 출력 레이어, 1개의 유닛
])

# 모델 컴파일
model.compile(optimizer='adam', loss='mse')  # 최적화 알고리즘: Adam, 손실 함수: 평균 제곱 오차(MSE)

# 데이터 준비
import numpy as np

# 입력 시퀀스 생성 (10개의 시간 단계와 1개의 특성)
X = np.random.rand(100, 10, 1)
# 출력 시퀀스 생성 (각 입력 시퀀스의 다음 값)
y = np.random.rand(100, 1)

# 모델 학습
model.fit(X, y, epochs=10, batch_size=32)  # 10번의 에포크로 배치 크기 32로 학습

# 모델 예측
prediction = model.predict(X[0].reshape(1, 10, 1))  # 첫 번째 입력 시퀀스를 사용하여 예측

print("예측 결과:", prediction)