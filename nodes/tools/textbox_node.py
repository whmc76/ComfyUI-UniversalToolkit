"""
Textbox Node
~~~~~~~~~~~

Adds text boxes to images with customizable styling.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
import textwrap
import copy
from PIL import Image, ImageFont, ImageDraw
from typing import cast
from ..image_utils import pil2tensor, tensor2pil
from .any_type import AnyType

any = AnyType("*")

class TextboxNode_UTK:
    """
    Textbox Node for adding text boxes to images
    """
    
    def __init__(self):
        self.NODE_NAME = 'TextboxNode_UTK'

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "image": ("IMAGE",),
                "text": ("STRING", {"default": "Text", "multiline": True}),
                "font_size": ("INT", {"default": 24, "min": 8, "max": 200, "step": 1}),
                "text_color": ("STRING", {"default": "#FFFFFF"}),
                "background_color": ("STRING", {"default": "#000000"}),
                "background_opacity": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 1.0, "step": 0.1}),
                "padding": ("INT", {"default": 10, "min": 0, "max": 100, "step": 1}),
                "border_radius": ("INT", {"default": 5, "min": 0, "max": 50, "step": 1}),
                "border_width": ("INT", {"default": 0, "min": 0, "max": 20, "step": 1}),
                "border_color": ("STRING", {"default": "#FFFFFF"}),
                "max_width": ("INT", {"default": 200, "min": 50, "max": 1000, "step": 10}),
                "x_position": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "y_position": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "alignment": (["center", "left", "right"],),
            },
            "optional": {
                "font_path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = 'add_textbox'
    CATEGORY = "UniversalToolkit/Image"
    DESCRIPTION = "Adds a text box to an image with customizable styling."

    def add_textbox(self, image, text, font_size, text_color, background_color, 
                   background_opacity, padding, border_radius, border_width, 
                   border_color, max_width, x_position, y_position, alignment, font_path=""):
        
        results = []
        
        for img in image:
            # Convert tensor to PIL
            pil_img = tensor2pil(img)
            img_width, img_height = pil_img.size
            
            # Create a copy to work with
            result_img = pil_img.copy()
            
            # Calculate text box position
            box_x = int(x_position * img_width)
            box_y = int(y_position * img_height)
            
            # Create text image
            text_img = self._create_text_box(
                text, font_size, text_color, background_color, background_opacity,
                padding, border_radius, border_width, border_color, max_width, 
                alignment, font_path
            )
            
            # Calculate position to center the text box
            text_width, text_height = text_img.size
            paste_x = box_x - text_width // 2
            paste_y = box_y - text_height // 2
            
            # Ensure text box stays within image bounds
            paste_x = max(0, min(paste_x, img_width - text_width))
            paste_y = max(0, min(paste_y, img_height - text_height))
            
            # Paste text box onto image
            if text_img.mode == 'RGBA':
                result_img.paste(text_img, (paste_x, paste_y), text_img)
            else:
                result_img.paste(text_img, (paste_x, paste_y))
            
            # Convert back to tensor
            result_tensor = pil2tensor(result_img)
            results.append(result_tensor)
        
        return (torch.cat(results, dim=0),)

    def _create_text_box(self, text, font_size, text_color, background_color, 
                        background_opacity, padding, border_radius, border_width, 
                        border_color, max_width, alignment, font_path=""):
        
        # Try to use custom font or fall back to default
        try:
            if font_path and font_path.strip():
                font = ImageFont.truetype(font_path, font_size)
            else:
                # Use default font
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Wrap text
        lines = textwrap.wrap(text, width=max_width // (font_size // 2), break_long_words=True)
        
        # Calculate text dimensions
        line_heights = []
        line_widths = []
        for line in lines:
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
            line_widths.append(line_width)
            line_heights.append(line_height)
        
        # Calculate box dimensions
        box_width = max(line_widths) + padding * 2
        box_height = sum(line_heights) + padding * 2 + (len(lines) - 1) * (font_size // 4)
        
        # Add border space
        if border_width > 0:
            box_width += border_width * 2
            box_height += border_width * 2
        
        # Create background
        background = Image.new('RGBA', (box_width, box_height), (0, 0, 0, 0))
        
        # Draw background rectangle
        if background_opacity > 0:
            bg_color = self._hex_to_rgba(background_color, background_opacity)
            self._draw_rounded_rectangle(background, 0, 0, box_width, box_height, 
                                       border_radius, bg_color)
        
        # Draw border
        if border_width > 0:
            border_rgba = self._hex_to_rgba(border_color, 1.0)
            self._draw_rounded_rectangle(background, 0, 0, box_width, box_height, 
                                       border_radius, border_rgba, border_width)
        
        # Draw text
        draw = ImageDraw.Draw(background)
        y_offset = padding + border_width
        
        for i, line in enumerate(lines):
            # Calculate x position based on alignment
            if alignment == "left":
                x_offset = padding + border_width
            elif alignment == "center":
                x_offset = (box_width - line_widths[i]) // 2
            else:  # right
                x_offset = box_width - line_widths[i] - padding - border_width
            
            # Draw text
            draw.text((x_offset, y_offset), line, fill=text_color, font=font)
            y_offset += line_heights[i] + (font_size // 4)
        
        return background

    def _hex_to_rgba(self, hex_color, alpha=1.0):
        """Convert hex color to RGBA tuple"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b, int(255 * alpha))

    def _draw_rounded_rectangle(self, img, x1, y1, x2, y2, radius, fill, border_width=0):
        """Draw a rounded rectangle"""
        draw = ImageDraw.Draw(img)
        
        if border_width > 0:
            # Draw border
            draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, 
                                 outline=fill, width=border_width)
        else:
            # Draw filled rectangle
            draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill)


# Node mappings
NODE_CLASS_MAPPINGS = {
    "TextboxNode_UTK": TextboxNode_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextboxNode_UTK": "Textbox Node (UTK)",
} 