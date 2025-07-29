import numpy as np
import pickle
import heapq
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# ========== 🔹 Load Saved Components ==========
print("🔁 Loading model and tokenizer...")
model = load_model('image_captioning_model.keras')

with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

vocab_size = len(tokenizer.word_index) + 1
max_length = 34  # update if different
print(f"✅ Model and tokenizer loaded | Vocab Size: {vocab_size}")

# ========== 🔹 Word Index Mappings ==========
index_word = {v: k for k, v in tokenizer.word_index.items()}

# ========== 🔹 Image Encoder (InceptionV3) ==========
inception_model = InceptionV3(weights='imagenet')
cnn_encoder = Model(inputs=inception_model.input, outputs=inception_model.layers[-2].output)

def preprocess_image(img_path):
    img = load_img(img_path, target_size=(299, 299))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

def encode_image(image_path):
    img = preprocess_image(image_path)
    feature_vector = cnn_encoder.predict(img)
    return np.reshape(feature_vector, (1, 2048))

# ========== 🔹 Caption Generation (Greedy Search) ==========
def generate_caption_greedy(image_path):
    photo = encode_image(image_path)
    caption = 'startseq'

    for _ in range(max_length):
        sequence = tokenizer.texts_to_sequences([caption])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo, sequence], verbose=0)
        word_id = np.argmax(yhat)

        word = index_word.get(word_id)
        if word is None:
            break
        caption += ' ' + word
        if word == 'endseq':
            break

    final_caption = caption.replace('startseq', '').replace('endseq', '').strip()
    return final_caption

# ========== 🔹 Caption Generation (Beam Search) ==========
def generate_caption(image_path, beam_index=5):
    """
    Generate a caption for an image using beam search.
    
    Args:
        image_path (str): Path to the image
        beam_index (int): Beam width for beam search
        
    Returns:
        str: Generated caption
    """
    # If beam_index is 1 or less, use greedy search
    if beam_index <= 1:
        return generate_caption_greedy(image_path)
    
    # Encode the image
    photo = encode_image(image_path)
    
    # Start with 'startseq'
    start_word = [tokenizer.word_index['startseq']]
    
    # Initialize beam search
    beam_size = beam_index
    sequences = [[start_word, 0.0]]
    
    # Expand each sequence one word at a time
    for _ in range(max_length):
        all_candidates = []
        
        # Expand each current candidate
        for seq, score in sequences:
            if seq[-1] == tokenizer.word_index.get('endseq', 1):
                # If the sequence ends with 'endseq', keep it as is
                all_candidates.append([seq, score])
                continue
                
            # Prepare the sequence
            sequence = pad_sequences([seq], maxlen=max_length)[0]
            sequence = np.reshape(sequence, (1, max_length))
            
            # Predict the next word probabilities
            yhat = model.predict([photo, sequence], verbose=0)
            
            # Get top k predictions
            yhat = yhat[0]
            top_indices = np.argsort(yhat)[-beam_size:]
            
            # Create a new candidate for each top prediction
            for i in top_indices:
                word = index_word.get(i)
                if word is not None:  # Skip if word is None
                    candidate_seq = seq.copy()
                    candidate_seq.append(i)
                    candidate_score = score + np.log(yhat[i])
                    all_candidates.append([candidate_seq, candidate_score])
        
        # Order all candidates by score
        ordered = sorted(all_candidates, key=lambda x: x[1], reverse=True)
        
        # Select k best
        sequences = ordered[:beam_size]
        
        # Check if all sequences end with 'endseq'
        if all(seq[-1] == tokenizer.word_index.get('endseq', 1) for seq, _ in sequences):
            break
    
    # Get the best sequence
    best_sequence = sequences[0][0]
    
    # Convert sequence to words
    caption = ' '.join([index_word.get(i, '') for i in best_sequence])
    
    # Clean up the caption
    final_caption = caption.replace('startseq', '').replace('endseq', '').strip()
    return final_caption

# ========== 🔹 Run Captioning ==========
if __name__ == "__main__":
    img_path = 'test.jpg'
    caption = generate_caption(img_path, beam_index=5)
    print(f"🖼️ Generated Caption for {img_path}: {caption}")
