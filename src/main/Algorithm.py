import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Embedding, Flatten, Concatenate, Dense, Dropout, Multiply, Lambda
import os

def preprocess_data(user_interests, user_clicks, all_articles, max_vocab_size=35000):
    user_interests_text = " ".join(user_interests[:3])
    user_clicks_text = " ".join([click['title'] for click in user_clicks])
    user_profiles = [user_interests_text + " " + user_clicks_text]

    articles_texts = [article['title'] for article in all_articles]

    tokenizer = Tokenizer(num_words=max_vocab_size)
    tokenizer.fit_on_texts(user_profiles + articles_texts + user_interests)

    user_sequences = tokenizer.texts_to_sequences(user_profiles)
    article_sequences = tokenizer.texts_to_sequences(articles_texts)
    interest_sequences = tokenizer.texts_to_sequences(user_interests)

    vocab_size = min(max_vocab_size, len(tokenizer.word_index) + 1)

    def correct_indices(sequences, vocab_size):
        corrected_sequences = []
        for seq in sequences:
            corrected_seq = []
            for index in seq:
                if index >= vocab_size:
                    corrected_seq.append(vocab_size - 1)
                else:
                    corrected_seq.append(index)
            corrected_sequences.append(corrected_seq)
        return corrected_sequences

    user_sequences = correct_indices(user_sequences, vocab_size)
    article_sequences = correct_indices(article_sequences, vocab_size)
    interest_sequences = correct_indices(interest_sequences, vocab_size)

    max_len = max(max(len(seq) for seq in user_sequences),
                  max(max(len(seq) for seq in article_sequences), max(len(seq) for seq in interest_sequences)))
    user_padded_sequences = pad_sequences(user_sequences, maxlen=max_len)
    article_padded_sequences = pad_sequences(article_sequences, maxlen=max_len)
    interest_padded_sequences = pad_sequences(interest_sequences, maxlen=max_len)

    return user_padded_sequences, article_padded_sequences, interest_padded_sequences, tokenizer, max_len

def build_model(vocab_size, embedding_dim, max_len):
    user_input = Input(shape=(max_len,), name='user_input')
    user_embedding = Embedding(input_dim=vocab_size, output_dim=embedding_dim)(user_input)
    user_flat = Flatten()(user_embedding)

    article_input = Input(shape=(max_len,), name='article_input')
    article_embedding = Embedding(input_dim=vocab_size, output_dim=embedding_dim)(article_input)
    article_flat = Flatten()(article_embedding)

    interest_input = Input(shape=(max_len,), name='interest_input')
    interest_embedding = Embedding(input_dim=vocab_size, output_dim=embedding_dim)(interest_input)
    interest_flat = Flatten()(interest_embedding)

    # 관심사의 가중치를 증가시키기 위해 요소별 곱셈
    interest_weighted = Lambda(lambda x: x * 2)(interest_flat)  # 가중치를 2배로 설정

    concatenated = Concatenate()([user_flat, article_flat, interest_weighted])
    dense = Dense(128, activation='relu')(concatenated)
    dense = Dropout(0.5)(dense)
    output = Dense(1, activation='sigmoid')(dense)

    model = Model(inputs=[user_input, article_input, interest_input], outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model

def train_model(interests, clicks, all_articles, model_path='model.h5'):
    user_padded_sequences, article_padded_sequences, interest_padded_sequences, tokenizer, max_len = preprocess_data(interests, clicks, all_articles)

    vocab_size = min(35000, len(tokenizer.word_index) + 1)
    embedding_dim = 50

    if os.path.exists(model_path):
        os.remove(model_path)
        print(f"Deleted existing model file: {model_path}")

    model = build_model(vocab_size, embedding_dim, max_len)

    if clicks:
        clicked_titles = [click['title'] for click in clicks]
        clicked_articles = [article for article in all_articles if article['title'] in clicked_titles]
        non_clicked_articles = [article for article in all_articles if article['title'] not in clicked_titles]

        article_padded_sequences_pos = pad_sequences(tokenizer.texts_to_sequences([article['title'] for article in clicked_articles]), maxlen=max_len)
        article_padded_sequences_neg = pad_sequences(tokenizer.texts_to_sequences([article['title'] for article in non_clicked_articles]), maxlen=max_len)

        X_user_pos = np.tile(user_padded_sequences, (len(article_padded_sequences_pos), 1))
        X_article_pos = article_padded_sequences_pos
        X_interest_pos = np.tile(interest_padded_sequences, (len(article_padded_sequences_pos), 1))
        y_pos = np.ones(len(article_padded_sequences_pos))

        X_user_neg = np.tile(user_padded_sequences, (len(article_padded_sequences_neg), 1))
        X_article_neg = article_padded_sequences_neg
        X_interest_neg = np.tile(interest_padded_sequences, (len(article_padded_sequences_neg), 1))
        y_neg = np.zeros(len(article_padded_sequences_neg))

        X_user = np.concatenate([X_user_pos, X_user_neg])
        X_article = np.concatenate([X_article_pos, X_article_neg])
        X_interest = np.concatenate([X_interest_pos, X_interest_neg])
        y = np.concatenate([y_pos, y_neg])
    else:
        X_user = np.tile(user_padded_sequences, (len(article_padded_sequences), 1))
        X_article = article_padded_sequences
        X_interest = np.tile(interest_padded_sequences, (len(article_padded_sequences), 1))
        y = np.ones(len(article_padded_sequences))

    # X_interest의 크기를 X_user와 X_article의 크기에 맞춥니다.
    X_interest = X_interest[:len(X_user)]

    # 입력 데이터의 크기를 출력하여 확인합니다.
    print(f"X_user: {X_user.shape}, X_article: {X_article.shape}, X_interest: {X_interest.shape}, y: {y.shape}")

    model.fit([X_user, X_article, X_interest], y, epochs=10, batch_size=64, verbose=1)

    model.save(model_path)
    return model, tokenizer, max_len

def recommend_articles(user_data, access_token, server_url, model_path='model.h5'):
    interests = user_data['interests']
    clicks = user_data['clicks']
    all_articles = user_data['all_articles']

    # 사용자 데이터를 출력하여 문제를 진단합니다.
    print(f"Interests: {interests}, Clicks: {clicks}, All Articles: {len(all_articles)}")

    if not interests or not clicks or not all_articles:
        return []

    model, tokenizer, max_len = train_model(interests, clicks, all_articles, model_path)

    user_profiles = [" ".join(interests[:3] + [click['title'] + " " + click['description'] for click in clicks])]
    user_sequences = tokenizer.texts_to_sequences(user_profiles)
    user_padded_sequences = pad_sequences(user_sequences, maxlen=max_len)

    articles_texts = [(article['title'] + " " + (article['summary'] if article['summary'] else "")) for article in all_articles]
    article_sequences = tokenizer.texts_to_sequences(articles_texts)
    article_padded_sequences = pad_sequences(article_sequences, maxlen=max_len)

    interest_sequences = tokenizer.texts_to_sequences(interests[:3])
    interest_padded_sequences = pad_sequences(interest_sequences, maxlen=max_len)

    X_user = np.tile(user_padded_sequences, (len(article_padded_sequences), 1))
    X_article = article_padded_sequences
    X_interest = np.tile(interest_padded_sequences, (len(article_padded_sequences), 1))

    # X_interest의 크기를 X_user와 X_article의 크기에 맞춥니다.
    X_interest = X_interest[:len(X_user)]

    predictions = model.predict([X_user, X_article, X_interest])

    article_scores = [(score, article) for score, article in zip(predictions, all_articles)]
    article_scores.sort(reverse=True, key=lambda x: x[0])

    recommended_articles = article_scores[:5]

    return recommended_articles
