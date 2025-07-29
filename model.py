# model.py

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, add

def define_captioning_model(vocab_size, max_length):
    """
    WHAT'S THIS?
    Builds an image captioning model:
    - Image features (2048D from CNN) are processed through a Dense layer
    - Caption input (text sequence) is passed through Embedding + LSTM
    - Both branches are merged and passed to output Dense layer (softmax)
    
    Args:
        vocab_size (int): total number of unique words (tokens) in the captions
        max_length (int): max caption length (used for padding)

    Returns:
        Keras Model: compiled captioning model
    """

    # 1. Image Feature Extractor Input
    inputs1 = Input(shape=(2048,), name="image_input")  # from InceptionV3
    fe1 = Dropout(0.5)(inputs1)
    fe2 = Dense(256, activation='relu')(fe1)

    # 2. Caption Sequence Input
    inputs2 = Input(shape=(max_length,), name="text_input")
    se1 = Embedding(input_dim=vocab_size, output_dim=256, mask_zero=True)(inputs2)
    se2 = Dropout(0.5)(se1)
    se3 = LSTM(256)(se2)

    # 3. Merge Image + Text
    decoder1 = add([fe2, se3])
    decoder2 = Dense(256, activation='relu')(decoder1)
    outputs = Dense(vocab_size, activation='softmax')(decoder2)

    # 4. Final Model
    model = Model(inputs=[inputs1, inputs2], outputs=outputs)

    # 5. Compile Model
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model
