# Usage Guide - Smart Image Editing Application

## Quick Start

1. **Installation**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

3. **Access the Application**:
   - Open your browser at `http://localhost:8501`

## Features Overview

### File Operations
- **Upload**: Click "Browse files" in the sidebar and select an image (PNG, JPEG, or BMP)
- **Download**: Choose your preferred format (PNG, JPEG, BMP) and click "Download"

### Editing Toolbar

#### Transform Tab
- **Resize**: Adjust width and height, then click "Apply Resize"
- **Rotate**: Use the slider to select angle (-180° to 180°), then click "Apply Rotation"
- **Flip**: Choose Horizontal or Vertical, then click "Apply Flip"

#### Adjustments Tab
- **Brightness**: Adjust brightness factor (0.0 to 3.0, default 1.0)
- **Contrast**: Adjust contrast factor (0.0 to 3.0, default 1.0)

#### Filters Tab
- **Blur**: Apply Gaussian blur with adjustable intensity
- **Sharpen**: Enhance image details
- **Grayscale**: Convert image to grayscale
- **Edge Detection**: Detect edges using Canny algorithm

#### Crop Tab
- **Crop**: Specify X, Y coordinates and width, height for precise cropping

### History Management
- **Undo**: Go back to previous state (up to 20 states)
- **Redo**: Go forward after undo
- **Reset**: Return to original uploaded image

## Tips

1. **Multiple Edits**: Apply multiple edits in sequence. Each edit is saved in history.
2. **Undo/Redo**: Use these buttons to experiment with different edits without losing your work.
3. **Download**: You can download at any point in your editing process.
4. **Reset**: If you want to start over, use the "Reset to Original" button.

## Technical Details

### Supported Formats
- **Input**: PNG, JPEG, BMP
- **Output**: PNG, JPEG, BMP

### Image Processing
- All images are processed in BGR format (OpenCV standard)
- Display uses RGB format for correct color representation
- History maintains full-resolution copies (up to 20 states)

### Performance
- History is limited to 20 states to prevent memory issues
- Large images may take longer to process
- For best performance, use images under 5000x5000 pixels

## Troubleshooting

**Issue**: Application doesn't start
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Image upload fails
- **Solution**: Ensure the file format is supported (PNG, JPEG, or BMP)

**Issue**: Edits seem slow
- **Solution**: Try resizing large images first to improve performance

## API Reference

### ImageHistory Class
```python
history = ImageHistory()
history.add_state(image)  # Add new state
history.undo()            # Undo to previous state
history.redo()            # Redo to next state
history.can_undo()        # Check if undo is possible
history.can_redo()        # Check if redo is possible
```

### ImageEditor Class
```python
# Transform
ImageEditor.resize_image(image, width, height)
ImageEditor.rotate_image(image, angle)
ImageEditor.flip_image(image, direction)

# Adjustments
ImageEditor.adjust_brightness(image, factor)
ImageEditor.adjust_contrast(image, factor)

# Filters
ImageEditor.apply_blur(image, kernel_size)
ImageEditor.apply_sharpen(image)
ImageEditor.apply_edge_detection(image)
ImageEditor.convert_to_grayscale(image)

# Crop
ImageEditor.crop_image(image, x, y, width, height)
```
