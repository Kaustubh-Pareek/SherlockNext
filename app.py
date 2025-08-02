import streamlit as st
import numpy as np
import pickle
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

# Load model and tokenizer
model = load_model('next_word_lstm.h5', compile=False)
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Get max sequence length
max_sequence_len = model.input_shape[1]

st.title("Next Word Predictor")
st.write("Enter a seed sentence and select how many words to predict.")

# Input fields
seed_text = st.text_input("Seed text", "I will leave if they")
next_words = st.number_input("Number of words to predict", min_value=1, max_value=20, value=4)

# Button to trigger prediction
if st.button("Predict"):
    original_seed = seed_text
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        predicted = np.argmax(model.predict(token_list), axis=-1)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word

    st.write("**Input:**", original_seed)
    st.write("**Predicted Sentence:**", seed_text)
