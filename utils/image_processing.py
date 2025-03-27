import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
import random

def process_satellite_image(image):
    """
    Process a satellite image to detect deforestation.
    
    Parameters:
    -----------
    image : PIL.Image
        The satellite image to process
        
    Returns:
    --------
    tuple
        (processed_image, deforested_areas)
        where processed_image is a PIL Image with highlighted deforestation
        and deforested_areas is a list of dictionaries with bounding box coordinates
    """
    # Convert PIL image to numpy array for processing
    img_array = np.array(image)
    
    # Create a copy of the image for highlighting deforestation
    analyzed_img = image.copy()
    draw = ImageDraw.Draw(analyzed_img)
    
    # In a real application, this is where you would apply an actual
    # deforestation detection algorithm. Here we're simulating detection
    # by randomly generating "deforested" areas.
    
    # Get image dimensions
    width, height = image.size
    
    # Generate random deforested areas
    num_areas = random.randint(3, 8)
    deforested_areas = []
    
    for _ in range(num_areas):
        # Generate random box dimensions (between 5-15% of image size)
        box_width = random.randint(int(width * 0.05), int(width * 0.15))
        box_height = random.randint(int(height * 0.05), int(height * 0.15))
        
        # Generate random position
        x1 = random.randint(0, width - box_width)
        y1 = random.randint(0, height - box_height)
        x2 = x1 + box_width
        y2 = y1 + box_height
        
        # Add to list of deforested areas
        area = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "confidence": random.uniform(0.75, 0.98),
            "area_km2": round(box_width * box_height / 1000, 2)  # Simulated area
        }
        deforested_areas.append(area)
        
        # Draw red box with some transparency
        draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=3)
        
        # Add a semi-transparent red fill
        overlay = Image.new('RGBA', analyzed_img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle([(x1, y1), (x2, y2)], fill=(255, 0, 0, 75))
        
        # Convert analyzed_img to RGBA if it isn't already
        if analyzed_img.mode != 'RGBA':
            analyzed_img = analyzed_img.convert('RGBA')
            
        # Paste the overlay onto the analyzed image
        analyzed_img = Image.alpha_composite(analyzed_img, overlay)
    
    # Convert back to RGB for display compatibility
    analyzed_img = analyzed_img.convert('RGB')
    
    return analyzed_img, deforested_areas

def enhance_satellite_image(image, brightness=1.0, contrast=1.0, color=1.2):
    """
    Enhance a satellite image for better visualization.
    
    Parameters:
    -----------
    image : PIL.Image
        The satellite image to enhance
    brightness : float
        Brightness enhancement factor
    contrast : float
        Contrast enhancement factor
    color : float
        Color enhancement factor
        
    Returns:
    --------
    PIL.Image
        The enhanced image
    """
    # Enhance brightness
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)
    
    # Enhance color
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(color)
    
    return image
