import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from src.DB import db_connection

def preprocess_data(user_interests, user_clicks, all_articles):
    # 사용자 관심사와 클릭한 기사를 하나의 텍스트로 결합
    user_profiles = [" ".join(interests + [click[0] + " " + click[1] for click in user_clicks]) for interests, user_clicks in zip(user_interests, user_clicks)]

    # 모든 기사 제목과 설명을 결합
    articles_texts = [title + " " + description for _, title, description, _ in all_articles]

    # 텍스트 데이터 토큰화
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(user_profiles + articles_texts)

    # 사용자 프로필과 기사 텍스트를 시퀀스로 변환
    user_sequences = tokenizer.texts_to_sequences(user_profiles)
    article_sequences = tokenizer.texts_to_sequences(articles_texts)

    # 패딩
    max_len = max(max(len(seq) for seq in user_sequences), max(len(seq) for seq in article_sequences))
    user_padded_sequences = pad_sequences(user_sequences, maxlen=max_len)
    article_padded_sequences = pad_sequences(article_sequences, maxlen=max_len)

    return user_padded_sequences, article_padded_sequences, tokenizer

def build_model(vocab_size, embedding_dim, max_len):
    user_input = tf.keras.layers.Input(shape=(max_len,), name='user_input')
    user_embedding = tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len)(user_input)
    user_flat = tf.keras.layers.Flatten()(user_embedding)

    article_input = tf.keras.layers.Input(shape=(max_len,), name='article_input')
    article_embedding = tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len)(article_input)
    article_flat = tf.keras.layers.Flatten()(article_embedding)

    concatenated = tf.keras.layers.concatenate([user_flat, article_flat])
    dense = tf.keras.layers.Dense(128, activation='relu')(concatenated)
    output = tf.keras.layers.Dense(1, activation='sigmoid')(dense)

    model = tf.keras.models.Model(inputs=[user_input, article_input], outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model():
    user_interests, user_clicks, all_articles = db_connection.get_all_user_data()
    if not user_interests or not user_clicks or not all_articles:
        print("Not enough data to train the model")
        return

    user_sequences, article_sequences, tokenizer = preprocess_data(user_interests, user_clicks, all_articles)

    # 학습 데이터와 레이블 생성
    num_users = len(user_sequences)
    num_articles = len(article_sequences)
    labels = np.zeros((num_users, num_articles))

    for i, clicks in enumerate(user_clicks):
        for click in clicks:
            for j, article in enumerate(all_articles):
                if click[2] == article[3]:  # URL이 같은 경우
                    labels[i, j] = 1

    # 학습 데이터 분할
    X_user_train, X_article_train, y_train = user_sequences, article_sequences, labels

    # 모델 파라미터
    vocab_size = len(tokenizer.word_index) + 1
    embedding_dim = 50
    max_len = X_user_train.shape[1]

    model = build_model(vocab_size, embedding_dim, max_len)
    model.summary()

    # 모델 학습
    model.fit([X_user_train, X_article_train], y_train, epochs=10, batch_size=32, validation_split=0.2)

    # 모델 저장
    model.save('news_recommendation_model.h5')

def recommend_articles(username, top_n=5):
    model = tf.keras.models.load_model('news_recommendation_model.h5')
    user_id = db_connection.get_user_id_by_name(username)
    if user_id is None:
        print("User not found")
        return []

    user_interests, user_clicks, all_articles = db_connection.get_user_interests_and_clicks_and_all_articles(username)
    if not user_interests or not user_clicks or not all_articles:
        print("Not enough data to recommend articles")
        return []

    user_profiles = [" ".join(user_interests + [click[0] + " " + click[1] for click in user_clicks])]
    articles_texts = [title + " " + description for _, title, description, _ in all_articles]

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(user_profiles + articles_texts)

    user_sequence = tokenizer.texts_to_sequences(user_profiles)
    user_padded_sequence = pad_sequences(user_sequence, maxlen=model.input_shape[1])

    article_sequences = tokenizer.texts_to_sequences(articles_texts)
    article_padded_sequences = pad_sequences(article_sequences, maxlen=model.input_shape[1])

    predictions = model.predict([np.repeat(user_padded_sequence, len(article_padded_sequences), axis=0), article_padded_sequences])
    top_indices = predictions.flatten().argsort()[-top_n:][::-1]

    recommended_articles = [all_articles[i] for i in top_indices]
    return recommended_articles

if __name__ == "__main__":
    train_model()
