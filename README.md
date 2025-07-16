# Social Post Sentiment Classification (LSTM)

This project predicts positive/negative reactions to social media posts using deep learning (LSTM neural networks).  
Based on Reddit “Am I The Asshole” posts.

---

## 🧐 Project Overview

- **Goal:** Classify social media posts by sentiment (positive/negative = guilty user).
- **Approach:** Data preprocessing → Embedding → LSTM model → Evaluation.
- **Result:** Improved accuracy from 50% (baseline) to 67% (LSTM).

---

## 🛠️ Main Tools

- Python (pandas, numpy, scikit-learn)
- TensorFlow / Keras
- NLTK (for text cleaning)
- Jupyter Notebook

---

## Usage

1. Download the data and GloVe embeddings from:  
[Google Drive Link](https://drive.google.com/drive/folders/1VmTGtCu21Gg8aPz-Uxff9Fqu2lvxIZ8p?usp=sharing)
2. Place `aita_verdicts_unique_6000.csv` and `glove.6B.50d.txt` inside the `data/` folder.
3. Open the notebook: notebooks/text_classification_final.ipynb
4. Run all cells to train and evaluate the model.

---

## 📝 Results

- **Baseline (by random):** ~50%
- **LSTM:** ~67% accuracy

---
> *Feedback and suggestions welcome!*

