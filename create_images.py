from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

def create_placeholder_image(filename, width, height, text, bg_color=(41, 128, 185), text_color=(255, 255, 255)):
    """Create a placeholder image with text"""
    # Create new image with background color
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    try:
        # Try to use a TrueType font if available
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Calculate text position to be in the center
    # In newer PIL versions, use textbbox instead of textsize
    try:
        # For newer PIL versions
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        text_width = right - left
        text_height = bottom - top
    except AttributeError:
        # Fallback for older PIL versions
        text_width, text_height = draw.textsize(text, font=font)
        
    position = ((width-text_width)//2, (height-text_height)//2)
    
    # Draw text on image
    draw.text(position, text, font=font, fill=text_color)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Save the image
    image.save(filename)
    print(f"Image created: {filename}")

def create_education_image():
    """Create an education-themed image"""
    filename = 'static/images/education.png'
    width, height = 600, 400
    text = "Education & Learning"
    create_placeholder_image(filename, width, height, text)

def create_about_image():
    """Create an about-themed image"""
    filename = 'static/images/about.png'
    width, height = 600, 400
    text = "About This Project"
    create_placeholder_image(filename, width, height, text, bg_color=(44, 62, 80))

if __name__ == "__main__":
    # Change to project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create images
    create_education_image()
    create_about_image()
    
    print("Images created successfully!")
