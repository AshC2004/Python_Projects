# 🧠 CNN Models for Car Classification

This directory contains the Jupyter notebooks used to train and evaluate six different Convolutional Neural Network (CNN) architectures for the Car Model Classification project. The goal was to compare the performance of various well-known pre-trained models against a custom-built CNN on a specific dataset.

## 📊 Models Overview

Each notebook is a self-contained experiment for one of the following architectures:

| Notebook File | Model Architecture | Description | Test Accuracy |
|---------------|-------------------|-------------|---------------|
| `My_Model.ipynb` | **🏆 Custom CNN** | A deep CNN built from scratch with 6 convolutional blocks, batch normalization, and progressive dropout. **This was the best-performing model.** | **🥇 91.76%** |
| `AlexNet.ipynb` | **AlexNet** | An implementation of the classic AlexNet architecture, a foundational model in deep learning for image classification. | 🥈 67.47% |
| `DenseNet201.ipynb` | **DenseNet201** | A transfer learning approach using the pre-trained DenseNet201 model, known for its dense connectivity and feature reuse. | 15.38% |
| `InceptionV3.ipynb` | **InceptionV3** | A transfer learning approach using Google's InceptionV3 model, which uses inception modules for efficient, multi-scale feature extraction. | 15.74% |
| `MobileNetV2.ipynb` | **MobileNetV2** | A transfer learning approach using MobileNetV2, a lightweight and efficient architecture designed for mobile and embedded devices. | 15.25% |
| `Xception.ipynb` | **Xception** | A transfer learning approach based on the Xception architecture, which leverages depthwise separable convolutions. | ⚠️ Incomplete |

## 🚀 How to Use

To run these notebooks and replicate the training process, please follow these steps:

### 1. Set up the Environment
It is highly recommended to use a virtual environment.

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install all required libraries
pip install -r requirements.txt
```

### 2. Launch Jupyter Notebook
Once the environment is set up, you can run the notebooks.

```bash
# Navigate to the notebooks directory
cd notebooks/

# Launch Jupyter Lab or Jupyter Notebook
jupyter lab
```

### 3. Run the Notebooks
Open any of the `.ipynb` files and execute the cells sequentially to see the data loading, model building, training, and evaluation process.

## 📁 Code Structure

Each notebook follows a similar structure:

### 1. 🔧 Setup
Installation of dependencies and import of required libraries.

### 2. 📥 Data Loading
Downloading the dataset from Kaggle and setting up `ImageDataGenerator` for training and testing sets.

### 3. 🏗️ Model Definition
- **For transfer learning models:** Loading the pre-trained base model and adding a custom classification head
- **For the custom model:** Defining the CNN architecture layer by layer

### 4. 🏃‍♂️ Training
Compiling the model and running the `.fit()` method with callbacks for early stopping and learning rate reduction.

### 5. 📈 Evaluation
Plotting the training/validation accuracy and loss curves.

### 6. 🔮 Prediction
Running predictions on a sample of test images to visualize the model's performance.

### 7. 💾 Saving
Saving the final trained model to a `.keras` or `.h5` file.

## 📦 Dependencies

The core libraries required to run these notebooks are listed in the `requirements.txt` file. The primary dependencies are:

- `tensorflow` - Deep learning framework
- `pandas` - Data manipulation and analysis
- `matplotlib` - Plotting and visualization
- `numpy` - Numerical computing
- `kagglehub` - Kaggle dataset integration

## 💡 Key Insights

### 🎯 Why the Custom Model Performed Best:

1. **Tailored Architecture:** The custom CNN was specifically designed for this car classification task
2. **Balanced Complexity:** Progressive layer depth and dropout rates prevented overfitting
3. **Dataset Size:** With ~3,300 training images, a custom model was more suitable than large pre-trained networks

### ❌ Transfer Learning Challenges:

The pre-trained models struggled due to:
- **Domain Mismatch:** ImageNet features weren't optimal for car classification
- **Dataset Size:** Insufficient data to effectively fine-tune large networks
- **Overfitting:** Complex models overfitted on the relatively small dataset

## 🔄 Running Individual Experiments

Each notebook can be run independently. Here's what each one focuses on:

- **`My_Model.ipynb`:** 🏆 The winning architecture - start here to see the best results
- **`AlexNet.ipynb`:** 📚 Classic CNN implementation - good for understanding fundamentals
- **`DenseNet201.ipynb`:** 🔗 Dense connectivity exploration
- **`InceptionV3.ipynb`:** 🌐 Multi-scale feature extraction
- **`MobileNetV2.ipynb`:** 📱 Lightweight architecture analysis
- **`Xception.ipynb`:** ⚠️ Incomplete training (convergence issues)

## 📝 Notes

- **Runtime:** Each notebook takes 15-30 minutes to complete on a GPU-enabled environment
- **Memory:** Ensure you have at least 8GB RAM available
- **GPU:** While not required, GPU acceleration significantly speeds up training
- **Data:** The notebooks will automatically download the dataset from Kaggle on first run

---

💡 **Tip:** Start with `My_Model.ipynb` to see the best-performing architecture, then explore the other notebooks to understand why transfer learning didn't work as well for this specific task.
