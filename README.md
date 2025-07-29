# 🧠 Image Captioning Web App

An AI-powered web application that generates human-like captions from uploaded images using deep learning and computer vision.


---

## 🚀 Features

- 📸 Upload any `.jpg`, `.jpeg`, or `.png` image
- 🧠 Deep learning-based caption generation with EfficientNet + LSTM + Attention
- ✨ Beam Search decoding for better results
- 🎨 Modern Streamlit UI with gradients, hover animations, and Lottie animations
- 💬 Clear and interactive output with CTA buttons

---

## 🛠️ Tech Stack

| Layer      | Tools Used                                |
|------------|--------------------------------------------|
| Frontend   | Streamlit, Lottie, HTML/CSS                |
| Backend    | Python, TensorFlow, NumPy, Pillow          |
| Model      | EfficientNetB0 (Encoder), LSTM (Decoder)   |
| Dataset    | MS COCO captions dataset                   |

---

## 🖼️ Demo Preview

<img src="https://github.com/AdityaDharawat/Image-Captioning/assets/demo.gif" width="600"/>

---

## ⚙️ How to Run Locally

```bash
# Clone the repository
git clone https://github.com/AdityaDharawat/Image-Captioning.git
cd Image-Captioning

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

> 🔔 Make sure `image_captioning_model.keras` and `tokenizer.pkl` are present in the root directory.

---

## 🧪 Model Architecture

- **Encoder**: Pretrained EfficientNetB0
- **Decoder**: LSTM + Attention mechanism
- **Trained on**: MS COCO Dataset
- **Evaluation**: BLEU score, manual inspection

---

## 📁 Project Structure
```
ImageCaptioning/
├── app.py
├── generate_caption.py
├── image_captioning_model.keras
├── tokenizer.pkl
├── assets/
│   └── style.css
│   └── animation.json
├── README.md
```

---

## 🙌 Credits
- [COCO Dataset](https://cocodataset.org)
- [Streamlit](https://streamlit.io)
- [LottieFiles](https://lottiefiles.com)

---

## 📢 License
This project is open-source and available under the [MIT License](LICENSE).

---

> 👨‍💻 Made with 💜 by Aditya Dharawat
