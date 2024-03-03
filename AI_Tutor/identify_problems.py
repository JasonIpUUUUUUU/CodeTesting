import tensorflow as tf
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

with open('questions.txt', 'r') as file:
    lines = file.readlines()

questions = []
math_types = []

for line in lines:
    parts = line.strip().split('#')
    questions.append(parts[0])
    math_types.append(parts[1])

unique_math_types = set(math_types)

label_dict = {math_type: i for i, math_type in enumerate(unique_math_types)}

labels = [label_dict[math_type] for math_type in math_types]

tokenizer = Tokenizer(oov_token="<OOV>", num_words=5000)
tokenizer.fit_on_texts(questions)
word_index = tokenizer.word_index

max_sequence_length = 100

sequences = tokenizer.texts_to_sequences(questions)

padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)

labels = np.array(labels)

X_train, X_test, y_train, y_test = train_test_split(
    padded_sequences, labels, test_size=0.2, random_state=42
)

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=len(word_index) + 1, output_dim=16),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(label_dict), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

model.save('model1.keras')