# import tensorflow as tf

# Load your TensorFlow model
# model = tf.keras.models.load_model("path/to/your/model")


def generate_embedding(text: str) -> list[float]:
    """
    Generate embeddings for a given text using the TensorFlow model.
    """
    preprocessed_text = preprocess_text(text)
    embedding = model.predict([preprocessed_text])
    return embedding[0].tolist()


def preprocess_text(text: str) -> str:
    """
    Apply preprocessing to the input text as required by the TensorFlow model.
    """
    # Example: Lowercasing, removing special characters, etc.
    return text.lower()
