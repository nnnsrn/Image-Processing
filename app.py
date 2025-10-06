"""
Smart Image Editing Application (Mini Adobe AI)
A Streamlit-based image editor supporting PNG, JPEG, and BMP formats
with basic editing tools and undo/redo functionality.
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
from typing import Optional, List, Tuple


class ImageHistory:
    """Implements undo/redo functionality using a stack-based approach."""
    
    def __init__(self):
        self.history: List[np.ndarray] = []
        self.current_index: int = -1
        self.max_history: int = 20  # Limit history to prevent memory issues
    
    def add_state(self, image: np.ndarray) -> None:
        """Add a new state to history."""
        # Remove any states after current index (when user made new changes after undo)
        self.history = self.history[:self.current_index + 1]
        
        # Add new state
        self.history.append(image.copy())
        self.current_index += 1
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.current_index -= 1
    
    def undo(self) -> Optional[np.ndarray]:
        """Undo to previous state."""
        if self.can_undo():
            self.current_index -= 1
            return self.history[self.current_index].copy()
        return None
    
    def redo(self) -> Optional[np.ndarray]:
        """Redo to next state."""
        if self.can_redo():
            self.current_index += 1
            return self.history[self.current_index].copy()
        return None
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self.current_index > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self.current_index < len(self.history) - 1
    
    def get_current(self) -> Optional[np.ndarray]:
        """Get current state."""
        if self.current_index >= 0:
            return self.history[self.current_index].copy()
        return None
    
    def clear(self) -> None:
        """Clear history."""
        self.history = []
        self.current_index = -1


class ImageEditor:
    """Main image editing class with various image processing functions."""
    
    @staticmethod
    def load_image(uploaded_file) -> Optional[np.ndarray]:
        """Load image from uploaded file."""
        try:
            # Read image using PIL
            image = Image.open(uploaded_file)
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            # Convert to numpy array (OpenCV format)
            img_array = np.array(image)
            # Convert RGB to BGR for OpenCV
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            return img_array
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")
            return None
    
    @staticmethod
    def save_image(image: np.ndarray, format: str = 'PNG') -> bytes:
        """Convert image to bytes for download."""
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Convert to PIL Image
        pil_image = Image.fromarray(image_rgb)
        # Save to bytes
        buf = io.BytesIO()
        pil_image.save(buf, format=format)
        buf.seek(0)
        return buf.getvalue()
    
    @staticmethod
    def resize_image(image: np.ndarray, width: int, height: int) -> np.ndarray:
        """Resize image to specified dimensions."""
        return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    
    @staticmethod
    def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
        """Rotate image by specified angle."""
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(image, rotation_matrix, (width, height))
    
    @staticmethod
    def flip_image(image: np.ndarray, direction: str) -> np.ndarray:
        """Flip image horizontally or vertically."""
        if direction == 'Horizontal':
            return cv2.flip(image, 1)
        elif direction == 'Vertical':
            return cv2.flip(image, 0)
        return image
    
    @staticmethod
    def adjust_brightness(image: np.ndarray, factor: float) -> np.ndarray:
        """Adjust image brightness."""
        # Convert to PIL for easier manipulation
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        enhancer = ImageEnhance.Brightness(pil_image)
        enhanced = enhancer.enhance(factor)
        # Convert back to OpenCV format
        result = np.array(enhanced)
        return cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    
    @staticmethod
    def adjust_contrast(image: np.ndarray, factor: float) -> np.ndarray:
        """Adjust image contrast."""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        enhancer = ImageEnhance.Contrast(pil_image)
        enhanced = enhancer.enhance(factor)
        result = np.array(enhanced)
        return cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    
    @staticmethod
    def apply_blur(image: np.ndarray, kernel_size: int) -> np.ndarray:
        """Apply Gaussian blur to image."""
        if kernel_size % 2 == 0:
            kernel_size += 1  # Kernel size must be odd
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    @staticmethod
    def apply_sharpen(image: np.ndarray) -> np.ndarray:
        """Apply sharpening filter to image."""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        sharpened = pil_image.filter(ImageFilter.SHARPEN)
        result = np.array(sharpened)
        return cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    
    @staticmethod
    def apply_edge_detection(image: np.ndarray) -> np.ndarray:
        """Apply edge detection using Canny algorithm."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        # Convert back to BGR
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    @staticmethod
    def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    @staticmethod
    def crop_image(image: np.ndarray, x: int, y: int, width: int, height: int) -> np.ndarray:
        """Crop image to specified region."""
        return image[y:y+height, x:x+width]


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'history' not in st.session_state:
        st.session_state.history = ImageHistory()
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    if 'original_image' not in st.session_state:
        st.session_state.original_image = None
    if 'filename' not in st.session_state:
        st.session_state.filename = None


def main():
    """Main application function."""
    st.set_page_config(
        page_title="Smart Image Editor",
        page_icon="🎨",
        layout="wide"
    )
    
    initialize_session_state()
    
    st.title("🎨 Smart Image Editing Application")
    st.markdown("*Mini Adobe AI - A powerful image editor with basic and AI-powered features*")
    
    # Sidebar for file operations and editing tools
    with st.sidebar:
        st.header("📁 File Operations")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=['png', 'jpg', 'jpeg', 'bmp'],
            help="Supported formats: PNG, JPEG, BMP"
        )
        
        if uploaded_file is not None:
            # Load new image
            if st.session_state.filename != uploaded_file.name:
                image = ImageEditor.load_image(uploaded_file)
                if image is not None:
                    st.session_state.current_image = image
                    st.session_state.original_image = image.copy()
                    st.session_state.filename = uploaded_file.name
                    # Clear history and add initial state
                    st.session_state.history.clear()
                    st.session_state.history.add_state(image)
        
        # Undo/Redo buttons
        if st.session_state.current_image is not None:
            st.markdown("---")
            st.header("↩️ History")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("⬅️ Undo", disabled=not st.session_state.history.can_undo()):
                    undone_image = st.session_state.history.undo()
                    if undone_image is not None:
                        st.session_state.current_image = undone_image
                        st.rerun()
            
            with col2:
                if st.button("➡️ Redo", disabled=not st.session_state.history.can_redo()):
                    redone_image = st.session_state.history.redo()
                    if redone_image is not None:
                        st.session_state.current_image = redone_image
                        st.rerun()
            
            # Reset button
            if st.button("🔄 Reset to Original"):
                st.session_state.current_image = st.session_state.original_image.copy()
                st.session_state.history.clear()
                st.session_state.history.add_state(st.session_state.current_image)
                st.rerun()
            
            # Download button
            st.markdown("---")
            st.header("💾 Save Image")
            
            save_format = st.selectbox(
                "Select format",
                options=['PNG', 'JPEG', 'BMP']
            )
            
            image_bytes = ImageEditor.save_image(
                st.session_state.current_image,
                format=save_format
            )
            
            st.download_button(
                label=f"Download as {save_format}",
                data=image_bytes,
                file_name=f"edited_image.{save_format.lower()}",
                mime=f"image/{save_format.lower()}"
            )
    
    # Main area for image display and editing
    if st.session_state.current_image is not None:
        # Create tabs for different editing categories
        tab1, tab2, tab3, tab4 = st.tabs([
            "📐 Transform",
            "🎨 Adjustments",
            "🔍 Filters",
            "✂️ Crop"
        ])
        
        with tab1:
            st.subheader("Transform Image")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Resize**")
                current_height, current_width = st.session_state.current_image.shape[:2]
                new_width = st.number_input(
                    "Width",
                    min_value=1,
                    max_value=5000,
                    value=current_width,
                    key="resize_width"
                )
                new_height = st.number_input(
                    "Height",
                    min_value=1,
                    max_value=5000,
                    value=current_height,
                    key="resize_height"
                )
                
                if st.button("Apply Resize"):
                    resized = ImageEditor.resize_image(
                        st.session_state.current_image,
                        new_width,
                        new_height
                    )
                    st.session_state.current_image = resized
                    st.session_state.history.add_state(resized)
                    st.success("Image resized!")
                    st.rerun()
            
            with col2:
                st.markdown("**Rotate**")
                rotation_angle = st.slider(
                    "Rotation Angle",
                    min_value=-180,
                    max_value=180,
                    value=0,
                    key="rotation_angle"
                )
                
                if st.button("Apply Rotation"):
                    rotated = ImageEditor.rotate_image(
                        st.session_state.current_image,
                        rotation_angle
                    )
                    st.session_state.current_image = rotated
                    st.session_state.history.add_state(rotated)
                    st.success("Image rotated!")
                    st.rerun()
            
            st.markdown("**Flip**")
            flip_direction = st.radio(
                "Flip Direction",
                options=['Horizontal', 'Vertical'],
                key="flip_direction"
            )
            
            if st.button("Apply Flip"):
                flipped = ImageEditor.flip_image(
                    st.session_state.current_image,
                    flip_direction
                )
                st.session_state.current_image = flipped
                st.session_state.history.add_state(flipped)
                st.success("Image flipped!")
                st.rerun()
        
        with tab2:
            st.subheader("Image Adjustments")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Brightness**")
                brightness = st.slider(
                    "Brightness Factor",
                    min_value=0.0,
                    max_value=3.0,
                    value=1.0,
                    step=0.1,
                    key="brightness"
                )
                
                if st.button("Apply Brightness"):
                    adjusted = ImageEditor.adjust_brightness(
                        st.session_state.current_image,
                        brightness
                    )
                    st.session_state.current_image = adjusted
                    st.session_state.history.add_state(adjusted)
                    st.success("Brightness adjusted!")
                    st.rerun()
            
            with col2:
                st.markdown("**Contrast**")
                contrast = st.slider(
                    "Contrast Factor",
                    min_value=0.0,
                    max_value=3.0,
                    value=1.0,
                    step=0.1,
                    key="contrast"
                )
                
                if st.button("Apply Contrast"):
                    adjusted = ImageEditor.adjust_contrast(
                        st.session_state.current_image,
                        contrast
                    )
                    st.session_state.current_image = adjusted
                    st.session_state.history.add_state(adjusted)
                    st.success("Contrast adjusted!")
                    st.rerun()
        
        with tab3:
            st.subheader("Apply Filters")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Blur**")
                blur_kernel = st.slider(
                    "Blur Intensity",
                    min_value=1,
                    max_value=25,
                    value=5,
                    step=2,
                    key="blur_kernel"
                )
                
                if st.button("Apply Blur"):
                    blurred = ImageEditor.apply_blur(
                        st.session_state.current_image,
                        blur_kernel
                    )
                    st.session_state.current_image = blurred
                    st.session_state.history.add_state(blurred)
                    st.success("Blur applied!")
                    st.rerun()
            
            with col2:
                st.markdown("**Sharpen**")
                st.write("")  # Spacing
                if st.button("Apply Sharpen"):
                    sharpened = ImageEditor.apply_sharpen(
                        st.session_state.current_image
                    )
                    st.session_state.current_image = sharpened
                    st.session_state.history.add_state(sharpened)
                    st.success("Sharpen applied!")
                    st.rerun()
            
            with col3:
                st.markdown("**Grayscale**")
                st.write("")  # Spacing
                if st.button("Convert to Grayscale"):
                    grayscale = ImageEditor.convert_to_grayscale(
                        st.session_state.current_image
                    )
                    st.session_state.current_image = grayscale
                    st.session_state.history.add_state(grayscale)
                    st.success("Converted to grayscale!")
                    st.rerun()
            
            st.markdown("**Edge Detection**")
            if st.button("Apply Edge Detection"):
                edges = ImageEditor.apply_edge_detection(
                    st.session_state.current_image
                )
                st.session_state.current_image = edges
                st.session_state.history.add_state(edges)
                st.success("Edge detection applied!")
                st.rerun()
        
        with tab4:
            st.subheader("Crop Image")
            st.info("Enter crop coordinates and dimensions")
            
            current_height, current_width = st.session_state.current_image.shape[:2]
            
            col1, col2 = st.columns(2)
            
            with col1:
                crop_x = st.number_input(
                    "X (Left)",
                    min_value=0,
                    max_value=current_width-1,
                    value=0,
                    key="crop_x"
                )
                crop_width = st.number_input(
                    "Width",
                    min_value=1,
                    max_value=current_width-crop_x,
                    value=min(current_width-crop_x, 100),
                    key="crop_width"
                )
            
            with col2:
                crop_y = st.number_input(
                    "Y (Top)",
                    min_value=0,
                    max_value=current_height-1,
                    value=0,
                    key="crop_y"
                )
                crop_height = st.number_input(
                    "Height",
                    min_value=1,
                    max_value=current_height-crop_y,
                    value=min(current_height-crop_y, 100),
                    key="crop_height"
                )
            
            if st.button("Apply Crop"):
                cropped = ImageEditor.crop_image(
                    st.session_state.current_image,
                    crop_x,
                    crop_y,
                    crop_width,
                    crop_height
                )
                st.session_state.current_image = cropped
                st.session_state.history.add_state(cropped)
                st.success("Image cropped!")
                st.rerun()
        
        # Display current image
        st.markdown("---")
        st.subheader("Current Image")
        
        # Convert BGR to RGB for display
        display_image = cv2.cvtColor(st.session_state.current_image, cv2.COLOR_BGR2RGB)
        st.image(display_image, use_column_width=True)
        
        # Display image info
        height, width, channels = st.session_state.current_image.shape
        st.caption(f"Image dimensions: {width}x{height} | Channels: {channels}")
        
    else:
        # Welcome message when no image is loaded
        st.info("👈 Please upload an image using the sidebar to get started!")
        
        st.markdown("""
        ### Features:
        - 📁 **File Operations**: Open and save images in PNG, JPEG, and BMP formats
        - ↩️ **Undo/Redo**: Full history management with stack-based implementation
        - 📐 **Transform**: Resize, rotate, and flip images
        - 🎨 **Adjustments**: Control brightness and contrast
        - 🔍 **Filters**: Apply blur, sharpen, grayscale, and edge detection
        - ✂️ **Crop**: Precise image cropping with coordinate controls
        
        ### How to Use:
        1. Upload an image using the file uploader in the sidebar
        2. Use the tabs to access different editing tools
        3. Apply edits and use Undo/Redo to manage changes
        4. Download your edited image in your preferred format
        """)


if __name__ == "__main__":
    main()
