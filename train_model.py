# train_model.py

import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from model import define_captioning_model

# ========== 🔹 Load Tokenizer ==========
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

vocab_size = len(tokenizer.word_index) + 1
print(f"✅ Loaded tokenizer | Vocabulary Size: {vocab_size}")

# ========== 🔹 Load Image Features ==========
with open('image_features.pkl', 'rb') as f:
    image_features = pickle.load(f)

print(f"✅ Loaded image features | Total images: {len(image_features)}")

# ========== 🔹 Load and Clean Captions ==========
def load_captions(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    captions = {}
    for line in lines:
        image_id, caption = line.strip().split('\t')
        image_id = image_id.split('#')[0]
        if image_id not in captions:
            captions[image_id] = []
        captions[image_id].append(caption)
    return captions

def clean_caption(caption):
    import string
    caption = caption.lower()
    caption = caption.translate(str.maketrans('', '', string.punctuation))
    caption = caption.split()
    caption = [word for word in caption if len(word) > 1]
    return ' '.join(caption)

captions_file = './dataset/Flickr8k_text/Flickr8k.token.txt'
captions_dict = load_captions(captions_file)

cleaned_captions = {}
for img_id, cap_list in captions_dict.items():
    cleaned_captions[img_id] = [f"startseq {clean_caption(c)} endseq" for c in cap_list]

# ========== 🔹 Get Max Caption Length ==========
all_captions = [cap for caps in cleaned_captions.values() for cap in caps]
max_length = max(len(c.split()) for c in all_captions)
print(f"📏 Max caption length: {max_length}")

# ========== 🔹 Data Generator ==========
def data_generator(captions_dict, image_features, tokenizer, max_length, vocab_size, batch_size=64):
    X1, X2, y = [], [], []
    n = 0
    while True:
        for key, captions in captions_dict.items():
            photo = image_features.get(key, None)
            if photo is None:
                continue
            for caption in captions:
                seq = tokenizer.texts_to_sequences([caption])[0]
                for i in range(1, len(seq)):
                    in_seq, out_seq = seq[:i], seq[i]
                    in_seq = pad_sequences([in_seq], maxlen=max_length)[0]
                    out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]
                    X1.append(photo)
                    X2.append(in_seq)
                    y.append(out_seq)
                    n += 1
                    if n == batch_size:
                        yield ((np.array(X1, dtype='float32'), 
                                np.array(X2, dtype='int32')), 
                               np.array(y, dtype='float32'))
                        X1, X2, y = [], [], []
                        n = 0

# ========== 🔹 Build the Model ==========
model = define_captioning_model(vocab_size, max_length)
model.summary()

# ========== 🔹 Wrap the Generator with tf.data.Dataset ==========
steps = sum(len(c) for c in cleaned_captions.values()) // 64
print(f"🚀 Training started | Steps per epoch: {steps}")

train_dataset = tf.data.Dataset.from_generator(
    lambda: data_generator(cleaned_captions, image_features, tokenizer, max_length, vocab_size),
    output_signature=(
        (
            tf.TensorSpec(shape=(None, 2048), dtype=tf.float32),     # X1 - image features
            tf.TensorSpec(shape=(None, max_length), dtype=tf.int32)  # X2 - padded sequence
        ),
        tf.TensorSpec(shape=(None, vocab_size), dtype=tf.float32)     # y - one-hot encoded
    )
)

# ========== 🔹 Train the Model ==========
print(f"🚀 Training started | Steps per epoch: {steps}")

generator = data_generator(cleaned_captions, image_features, tokenizer, max_length, vocab_size)
model.fit(generator, epochs=10, steps_per_epoch=steps, verbose=1)


# ========== 🔹 Save the Trained Model ==========
model.save('image_captioning_model.keras')
print("✅ Model trained and saved as image_captioning_model.h5")
