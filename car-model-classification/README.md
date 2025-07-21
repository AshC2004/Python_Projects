# 🚗 Car Model Classification Project

This project uses Convolutional Neural Networks (CNNs) to classify car models from images. It compares several pre-trained architectures against a custom-built CNN, with the custom model achieving a superior test accuracy of **91.76%**.

**Dataset:** [Cars Image Dataset on Kaggle](https://www.kaggle.com/datasets/car-image-dataset)

<!-- ![Sample Predictions](images/sample_predictions.png) -->
<!-- *A sample of the best model's high-confidence predictions.* -->
> **Note:** Sample prediction images will be added once the model training is complete.

## Table of Contents

- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Models Used](#models-used)
- [Installation](#installation)
- [Usage](#usage)
- [Results and Analysis](#results-and-analysis)
- [Future Improvements](#future-improvements)
- [License](#license)

## Project Overview

The goal of this project is to develop a robust image classification model capable of distinguishing between seven different classes of cars. The core task is to explore the effectiveness of transfer learning with established architectures versus a custom-built CNN tailored specifically to this dataset.

### The project pipeline includes:

- **Data Preprocessing:** Loading and augmenting the "Cars Image Dataset" from Kaggle, which contains 3,352 training images and 813 test images.
- **Model Experimentation:** Training and evaluating six different CNN architectures.
- **Performance Analysis:** Comparing the models based on test accuracy and loss to identify the most effective approach.
- **App Demonstration:** A simple Streamlit app is included to showcase the prediction functionality.

## Technology Stack

- **Language:** Python
- **Core Libraries:** TensorFlow, Keras
- **Data Manipulation:** NumPy, Pandas
- **Web Framework:** Streamlit
- **Plotting:** Matplotlib
- **Development Environment:** Jupyter Notebook, Google Colab

## Models Used

A total of six different CNN architectures were trained and evaluated:

### 🏆 My_Model (Best Performing)
A custom-built sequential CNN designed to balance depth and regularization. Its architecture consists of 6 main blocks with:
- Progressively deeper convolutional layers (from 32 to 512 filters)
- Increasing dropout rates (from 0.10 to 0.35)
- Each block pattern: `Conv2D -> BatchNormalization -> Conv2D -> BatchNormalization -> MaxPooling -> Dropout`

This structure proved highly effective at learning the specific features of the car dataset without significant overfitting.

### Transfer Learning Models:
- **AlexNet:** An implementation of the classic AlexNet architecture
- **DenseNet201:** Utilizes the pre-trained DenseNet201, known for its dense connectivity
- **InceptionV3:** Employs Google's InceptionV3 for multi-scale feature extraction
- **MobileNetV2:** A lightweight architecture optimized for performance
- **Xception:** Based on depthwise separable convolutions *(Note: Training for this model was inconclusive and did not converge effectively)*

## Installation

Follow these steps to set up the project environment locally:

```bash
# 1. Clone the repository
git clone https://github.com/your-username/car-model-classification.git
cd car-model-classification

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# 3. Install the required dependencies
pip install -r requirements.txt
```

## Usage

### 1. To run the training notebooks:
Navigate to the `notebooks/` directory and open the Jupyter notebooks (`.ipynb` files). You can re-run the training and evaluation process for each model.

### 2. To run the Streamlit web app:
The provided `app.py` uses an external API for predictions and serves as a demonstration of the user interface.

```bash
streamlit run app.py
```

After running the command, open your web browser to `http://localhost:8501`.

## Results and Analysis

The custom-built model significantly outperformed all the pre-trained models. This outcome strongly suggests that for this particular dataset's size and specificity, a tailored architecture was more effective than fine-tuning a general-purpose one.

### Key Observations:

**✅ Custom Model Success:** The custom model's architecture, with its gradual increase in complexity and regularization at each stage, was able to learn the hierarchical features of the cars effectively, leading to a high test accuracy of **91.76%**.

**❌ Transfer Learning Challenges:** The pre-trained models struggled, with the best of them (AlexNet) only reaching 67.47% accuracy. This poor performance is likely due to:
- **Dataset Mismatch:** Features learned from ImageNet may not have been fully suitable for this specific car classification task
- **Overfitting Risk:** Large, complex models like DenseNet201 can easily overfit on smaller datasets if not fine-tuned carefully
- **Small Dataset:** With only ~3,300 training images, there may not have been enough data to effectively fine-tune the deeper layers of the pre-trained networks

### Final Test Results:

| Model | Test Accuracy | Test Loss |
|-------|---------------|-----------|
| **My_Model** | **91.76%** | **0.2651** |
| AlexNet | 67.47% | 0.9125 |
| InceptionV3 | 15.74% | 2.0179 |
| DenseNet201 | 15.38% | 4.3540 |
| MobileNetV2 | 15.25% | 2.1370 |
| Xception | Incomplete | Incomplete |

<!-- ![Training Curves](images/training_curves.png) -->
<!-- *Training and validation accuracy/loss curves for the best-performing custom model.* -->

## Future Improvements

- **Hyperparameter Tuning:** Use automated tools like KerasTuner or Optuna to systematically find optimal hyperparameters (learning rate, batch size, dropout rates) for the custom model
- **Advanced Data Augmentation:** Implement more sophisticated augmentation techniques like CutMix, Mixup, or GridMask to create more robust training samples
- **Integrate Best Model into App:** Modify the `app.py` to load and use the trained `my_model.keras` file directly for predictions, making the project fully self-contained
- **Deploy to Cloud:** Deploy the final Streamlit application to a service like Streamlit Community Cloud or Hugging Face Spaces for public access

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

⭐ If you found this project helpful, please consider giving it a star!

📧 For questions or suggestions, feel free to open an issue or contact me directly.
