# Trained Models

This directory contains the final trained model weights saved after running the experiments in the `notebooks` directory.

## Model Files

Below is a list of the available models, their corresponding architectures, and their final performance on the test set. The `My_Model.keras` file represents the **best-performing model** and is recommended for any inference tasks.

| Model File | Architecture | Test Accuracy | Notes |
|------------|-------------|---------------|-------|
| `My_Model.keras` | Custom CNN | **91.76%** | **Best performing model** |
| `AlexNet.h5` | AlexNet | 67.47% | - |
| `DenseNet201.h5` | DenseNet201 | 15.38% | Poor performance |
| `InceptionV3.h5` | InceptionV3 | 15.74% | Poor performance |
| `MobileNetV2.h5` | MobileNetV2 | 15.25% | Poor performance |
| `Xception.h5` | Xception | Incomplete | Training did not converge |

## ⚠️ Important Note on Usage and Compatibility

These model files were generated in a specific environment and **may not work "out-of-the-box"** in a different setup. If you encounter errors when trying to load or use these models (`.h5` or `.keras` files), please consider the following factors:

### 1. Library Versions
The models are highly dependent on the versions of `TensorFlow` and `Keras` they were trained with. A **version mismatch is the most common cause of errors** when loading a model. Please ensure you are using the versions specified in the `requirements` section.

### 2. Python Version
While less common, subtle differences between Python versions can sometimes affect the unpickling process used to load model components.

### 3. Data Preprocessing
A trained model expects input data to be preprocessed in *exactly* the same way as the data it was trained on. This includes:

- **Image Size:** All models were trained on images resized to `(128, 128)`
- **Scaling:** 
  - The custom model expects pixel values scaled to `` (by dividing by 255)
  - The transfer learning models (like MobileNetV2, InceptionV3, etc.) require their own specific `preprocess_input` function, which often scales pixel values to `[-1, 1]`
- **Color Channels:** The models expect 3-channel (RGB) images

### Recommendations
To ensure successful use of these models, it is **strongly recommended** to:
- Use the exact data preprocessing pipeline found in the corresponding training notebook
