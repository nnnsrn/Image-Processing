# 🎨 Smart Image Editing Application (Mini Adobe AI)

Final Project Image Processing and Recognition Course Group 2 AI Class 1 Batch 2024

A powerful image editing application built with Python, OpenCV, and Streamlit, featuring both basic editing tools and AI-powered features.

## 📋 Features

### Core Functionality
- **File Operations**: Open, display, edit, and save images
- **Format Support**: PNG, JPEG, and BMP formats
- **Undo/Redo System**: Stack-based history management with up to 20 states
- **User-Friendly Interface**: Built with Streamlit for an intuitive GUI

### Editing Tools

#### 📐 Transform
- **Resize**: Adjust image dimensions with custom width and height
- **Rotate**: Rotate images by any angle (-180° to 180°)
- **Flip**: Flip images horizontally or vertically

#### 🎨 Adjustments
- **Brightness**: Control image brightness (0.0 to 3.0x)
- **Contrast**: Adjust image contrast (0.0 to 3.0x)

#### 🔍 Filters
- **Blur**: Apply Gaussian blur with adjustable intensity
- **Sharpen**: Enhance image details
- **Grayscale**: Convert to grayscale
- **Edge Detection**: Detect edges using Canny algorithm

#### ✂️ Crop
- **Precise Cropping**: Crop images with coordinate-based controls

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/nnnsrn/Image-Processing.git
cd Image-Processing
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

Run the application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### How to Use

1. **Upload an Image**: Click "Browse files" in the sidebar and select an image (PNG, JPEG, or BMP)
2. **Edit Your Image**: Use the tabs to access different editing tools
3. **Undo/Redo**: Use the history buttons to manage your changes
4. **Save Your Work**: Download the edited image in your preferred format

## 🏗️ Architecture

### Core Components

#### ImageHistory Class
Implements undo/redo functionality using a stack-based approach:
- Maintains up to 20 states in history
- Supports undo and redo operations
- Automatically manages history when new edits are made

#### ImageEditor Class
Contains static methods for all image editing operations:
- File I/O operations
- Transform operations (resize, rotate, flip)
- Adjustment operations (brightness, contrast)
- Filter operations (blur, sharpen, grayscale, edge detection)
- Crop operations

#### Streamlit Session State
Manages application state:
- `history`: ImageHistory instance
- `current_image`: Currently displayed image
- `original_image`: Original uploaded image
- `filename`: Current file name

## 📦 Dependencies

- **streamlit**: Web application framework
- **opencv-python**: Image processing operations
- **Pillow**: Additional image manipulation
- **numpy**: Array operations

## 🔧 Technical Details

### Image Processing Pipeline
1. Images are loaded using PIL and converted to numpy arrays
2. OpenCV processes images in BGR format
3. Display uses RGB format for correct color representation
4. Each edit creates a new state in the history stack

### Memory Management
- History limited to 20 states to prevent excessive memory usage
- Images are copied when stored in history to prevent reference issues

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is part of an academic course assignment.

## 👥 Authors

Group 2 AI Class 1 Batch 2024

## 🙏 Acknowledgments

- Image Processing and Recognition Course
- OpenCV community
- Streamlit team
