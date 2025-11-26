# Chinese Word Segmentation (Max Match Algorithm)

This project implements a **Maximum Matching algorithm** to segment Chinese text (sentences without spaces) into individual words using a dictionary-based approach. It also includes an evaluation script to measure the accuracy against a Gold Standard.

## 📂 Project Structure

* `chinese_segmentation.py` - The main script implementing the segmentation algorithm.
* `eval_chinese_segmentation.py` - Script to evaluate accuracy (Precision/Recall equivalent).
* `chinesetrad_wordlist.utf8` - Dictionary of known Chinese words (Traditional).
* `chinesetext.utf8` - Raw input text to be segmented.
* `chinesetext_goldstandard.utf8` - Manually segmented text (ground truth) for evaluation.
* `chinese_segmentation.ipynb` - Jupyter notebook with comment clean code and evaluation all together.
## 🚀 How to Run

### 1. Segmentation
Run the main script to segment the raw text. It takes the wordlist and input text as arguments and saves the result to `MYRESULTS.utf8`.

```bash
python chinese_segmentation.py chinesetrad_wordlist.utf8 chinesetext.utf8 MYRESULTS.utf8
