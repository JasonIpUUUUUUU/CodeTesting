import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import pickle

prefix = "Summarise: "

with open('Articles.txt', 'r') as file:
    lines = file.readlines()

articles = []
summaries = []

for line in lines:
    parts = line.strip().split('@')
    articles.append(prefix + parts[0])
    summaries.append(parts[1])

combined_data = [(article, summary) for article, summary in zip(articles, summaries)]

train_data, test_data = train_test_split(combined_data, test_size=0.5, random_state=42)

train_articles, train_summaries = zip(*train_data)
test_articles, test_summaries = zip(*test_data)

max_words = 10000
max_len = 100

tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
tokenizer.fit_on_texts(train_articles + train_summaries)

train_article_sequences = pad_sequences(tokenizer.texts_to_sequences(train_articles), maxlen=max_len, padding='post', truncating='post')
train_summary_sequences = pad_sequences(tokenizer.texts_to_sequences(train_summaries), maxlen=max_len, padding='post', truncating='post')

test_article_sequences = pad_sequences(tokenizer.texts_to_sequences(test_articles), maxlen=max_len, padding='post', truncating='post')
test_summary_sequences = pad_sequences(tokenizer.texts_to_sequences(test_summaries), maxlen=max_len, padding='post', truncating='post')

train_summary_sequences_onehot = to_categorical(train_summary_sequences, num_classes=max_words)
test_summary_sequences_onehot = to_categorical(test_summary_sequences, num_classes=max_words)

embedding_dim = 100
model = Sequential([
    Embedding(input_dim=max_words, output_dim=embedding_dim),
    LSTM(100, return_sequences=True),
    Dense(max_words, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

early_stopping_callback = EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True)
epochs = 10

model.fit(
    train_article_sequences,
    train_summary_sequences_onehot,  
    epochs=epochs,
    validation_data=(test_article_sequences, test_summary_sequences_onehot),  
    callbacks=[early_stopping_callback]
)

model.save('summariser.keras')

saved_data = {
    'tokenizer': tokenizer,
    'max_sequence_length': max_len
}

with open('tokenizer_and_parameters.pkl', 'wb') as file:
    pickle.dump(saved_data, file)

