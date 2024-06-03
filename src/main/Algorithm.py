import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Embedding, Flatten, Concatenate, Dense, Dropout
from sklearn.preprocessing import LabelEncoder
import os


def preprocess_data(user_interests, user_clicks, all_articles):
    user_interests_text = " ".join(user_interests[:3])
    user_clicks_text = " ".join([click['title'] + " " + click['description'] for click in user_clicks])
    user_profiles = [user_interests_text + " " + user_clicks_text]

    articles_texts = [(article['title'] + " " + (article['summary'] if article['summary'] else "")) for article in
                      all_articles]

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(user_profiles + articles_texts + user_interests)

    user_sequences = tokenizer.texts_to_sequences(user_profiles)
    article_sequences = tokenizer.texts_to_sequences(articles_texts)
    interest_sequences = tokenizer.texts_to_sequences(user_interests)

    max_len = max(max(len(seq) for seq in user_sequences),
                  max(max(len(seq) for seq in article_sequences), max(len(seq) for seq in interest_sequences)))
    user_padded_sequences = pad_sequences(user_sequences, maxlen=max_len)
    article_padded_sequences = pad_sequences(article_sequences, maxlen=max_len)
    interest_padded_sequences = pad_sequences(interest_sequences, maxlen=max_len)

    return user_padded_sequences, article_padded_sequences, interest_padded_sequences, tokenizer


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

    concatenated = Concatenate()([user_flat, article_flat, interest_flat])
    dense = Dense(128, activation='relu')(concatenated)
    dense = Dropout(0.5)(dense)
    output = Dense(1, activation='sigmoid')(dense)

    model = Model(inputs=[user_input, article_input, interest_input], outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model


def train_model(interests, clicks, all_articles, model_path='model.h5'):
    user_padded_sequences, article_padded_sequences, interest_padded_sequences, tokenizer = preprocess_data(interests,
                                                                                                            clicks,
                                                                                                            all_articles)

    vocab_size = len(tokenizer.word_index) + 1
    embedding_dim = 50
    max_len = user_padded_sequences.shape[1]

    if os.path.exists(model_path):
        model = load_model(model_path)
    else:
        model = build_model(vocab_size, embedding_dim, max_len)

    X_user = np.tile(user_padded_sequences, (len(article_padded_sequences), 1))
    X_article = article_padded_sequences
    X_interest = np.tile(interest_padded_sequences, (len(article_padded_sequences), 1))
    y = np.ones(len(article_padded_sequences))

    model.fit([X_user, X_article, X_interest], y, epochs=10, verbose=1)

    model.save(model_path)
    return model, tokenizer, max_len


def recommend_articles(user_data, access_token, server_url, model_path='model.h5'):
    interests = user_data['interests']
    clicks = user_data['clicks']
    all_articles = user_data['all_articles']

    if not interests or not clicks or not all_articles:
        return []

    model, tokenizer, max_len = train_model(interests, clicks, all_articles, model_path)

    user_profiles = [" ".join(interests[:3] + [click['title'] + " " + click['description'] for click in clicks])]
    user_sequences = tokenizer.texts_to_sequences(user_profiles)
    user_padded_sequences = pad_sequences(user_sequences, maxlen=max_len)

    articles_texts = [(article['title'] + " " + (article['summary'] if article['summary'] else "")) for article in
                      all_articles]
    article_sequences = tokenizer.texts_to_sequences(articles_texts)
    article_padded_sequences = pad_sequences(article_sequences, maxlen=max_len)

    interest_sequences = tokenizer.texts_to_sequences(interests[:3])
    interest_padded_sequences = pad_sequences(interest_sequences, maxlen=max_len)

    X_user = np.tile(user_padded_sequences, (len(article_padded_sequences), 1))
    X_article = article_padded_sequences
    X_interest = np.tile(interest_padded_sequences, (len(article_padded_sequences), 1))

    predictions = model.predict([X_user, X_article, X_interest])

    article_scores = [(score, article) for score, article in zip(predictions, all_articles)]
    article_scores.sort(reverse=True, key=lambda x: x[0])

    recommended_articles = article_scores[:5]

    return recommended_articles
