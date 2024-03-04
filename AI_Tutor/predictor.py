import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences
import pickle

# Load the saved model
loaded_model = tf.keras.models.load_model('model1.keras')

# Load the tokenizer and other necessary parameters
with open('tokenizer_and_parameters.pkl', 'rb') as file:
    saved_data = pickle.load(file)
    tokenizer = saved_data['tokenizer']
    max_sequence_length = saved_data['max_sequence_length']
    label_dict = saved_data['label_dict']
    inverse_label_dict = saved_data['inverse_label_dict']

# Function to preprocess user input and make predictions
def predict_math_type(user_input, tokenizer, max_sequence_length, model):
    # Tokenize and pad the user input
    sequence = tokenizer.texts_to_sequences([user_input])
    padded_sequence = pad_sequences(sequence, maxlen=max_sequence_length)

    # Make predictions
    predictions = model.predict(padded_sequence)

    # Get the predicted label
    predicted_label = tf.argmax(predictions, axis=1).numpy()[0]

    return predicted_label

# Example of testing user input
user_question = input("Enter a math-related question: ")

# Use the function to predict the math type
predicted_label = predict_math_type(user_question, tokenizer, max_sequence_length, loaded_model)

# Map the predicted label back to the original math type
predicted_math_type = inverse_label_dict[predicted_label]

print(f"The predicted math type for the question is: {predicted_math_type}")
