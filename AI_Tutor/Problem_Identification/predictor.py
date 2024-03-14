import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences
import pickle

loaded_model = tf.keras.models.load_model('model1.keras')

with open('tokenizer_and_parameters.pkl', 'rb') as file:
    saved_data = pickle.load(file)
    tokenizer = saved_data['tokenizer']
    max_sequence_length = saved_data['max_sequence_length']
    label_dict = saved_data['label_dict']
    inverse_label_dict = saved_data['inverse_label_dict']

def predict_math_type(user_input, tokenizer, max_sequence_length, model):
    sequence = tokenizer.texts_to_sequences([user_input])
    padded_sequence = pad_sequences(sequence, maxlen=max_sequence_length)
    predictions = model.predict(padded_sequence)
    predicted_label = tf.argmax(predictions, axis=1).numpy()[0]
    return predicted_label

user_question = input("Enter a math-related question: ")

predicted_label = predict_math_type(user_question, tokenizer, max_sequence_length, loaded_model)

predicted_math_type = inverse_label_dict[predicted_label]

print(f"The predicted math type for the question is: {predicted_math_type}")
