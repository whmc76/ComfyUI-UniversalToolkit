"""
Color Match Node for ComfyUI Universal Toolkit - Standalone Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Color matching functionality adapted from kjnodes.
This is a standalone version that follows the project's existing architecture.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor


class ColorMatch_UTK:
    """
    Color matching node that enables color transfer across images.
    
    This node is based on the color-matcher library and provides various methods
    for transferring color characteristics from a reference image to a target image.
    Useful for automatic color-grading of photographs, paintings, and film sequences.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_target": ("IMAGE", {"tooltip": "Target image to apply color matching to"}),
                "image_ref": ("IMAGE", {"tooltip": "Reference image to match colors from"}),
                "method": (
                    [   
                        'mkl',
                        'hm', 
                        'reinhard', 
                        'mvgd', 
                        'hm-mvgd-hm', 
                        'hm-mkl-hm',
                    ], {
                       "default": 'mkl',
                       "tooltip": "Color matching method to use"
                    }
                ),
            },
            "optional": {
                "strength": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.0, 
                    "max": 10.0, 
                    "step": 0.01,
                    "tooltip": "Strength of the color matching effect"
                }),
                "multithread": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Use multithreading for batch processing"
                }),
            }
        }
    
    CATEGORY = "UniversalToolkit/Image"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "colormatch"
    
    DESCRIPTION = """
Color-matcher enables color transfer across images which comes in handy for automatic  
color-grading of photographs, paintings and film sequences as well as light-field  
and stopmotion corrections.  

The methods behind the mappings are based on the approach from Reinhard et al.,  
the Monge-Kantorovich Linearization (MKL) as proposed by Pitie et al. and our analytical solution  
to a Multi-Variate Gaussian Distribution (MVGD) transfer in conjunction with classical histogram   
matching. As shown below our HM-MVGD-HM compound outperforms existing methods.   

Methods:
- mkl: Monge-Kantorovich Linearization
- hm: Histogram Matching  
- reinhard: Reinhard et al. method
- mvgd: Multi-Variate Gaussian Distribution
- hm-mvgd-hm: Histogram Matching + MVGD + Histogram Matching
- hm-mkl-hm: Histogram Matching + MKL + Histogram Matching

Reference: https://github.com/hahnec/color-matcher/
"""
    
    def colormatch(self, image_target, image_ref, method, strength=1.0, multithread=True):
        """
        Apply color matching from reference image to target image.
        
        Args:
            image_target: Target image tensor to be color matched
            image_ref: Reference image tensor
            method: Color matching method to use
            strength: Strength of the color matching effect (0.0 to 10.0)
            multithread: Whether to use multithreading for batch processing
            
        Returns:
            Tuple containing the color matched image tensor
        """
        try:
            from color_matcher import ColorMatcher
        except ImportError:
            raise Exception(
                "Can't import color-matcher. Please install it using: pip install color-matcher"
            )
        
        # Move tensors to CPU for processing
        image_ref = image_ref.cpu()
        image_target = image_target.cpu()
        batch_size = image_target.size(0)
        
        # Remove batch dimension if single image
        images_target = image_target.squeeze()
        images_ref = image_ref.squeeze()

        # Convert to numpy arrays
        image_ref_np = images_ref.numpy()
        images_target_np = images_target.numpy()

        def process(i):
            """Process a single image in the batch."""
            cm = ColorMatcher()
            
            # Handle batch vs single image
            image_target_np_i = images_target_np if batch_size == 1 else images_target[i].numpy()
            image_ref_np_i = image_ref_np if image_ref.size(0) == 1 else images_ref[i].numpy()
            
            try:
                # Apply color matching
                image_result = cm.transfer(src=image_target_np_i, ref=image_ref_np_i, method=method)
                
                # Apply strength blending
                image_result = image_target_np_i + strength * (image_result - image_target_np_i)
                
                return torch.from_numpy(image_result)
            except Exception as e:
                print(f"Color matching error for image {i}: {e}")
                return torch.from_numpy(image_target_np_i)  # Return original as fallback

        # Process images (with or without multithreading)
        if multithread and batch_size > 1:
            max_threads = min(os.cpu_count() or 1, batch_size)
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                out = list(executor.map(process, range(batch_size)))
        else:
            out = [process(i) for i in range(batch_size)]

        # Stack results and ensure proper format
        out = torch.stack(out, dim=0).to(torch.float32)
        out.clamp_(0, 1)  # Ensure values are in valid range
        
        return (out,)


# Node registration - Following the project's existing pattern
NODE_CLASS_MAPPINGS = {
    "ColorMatch_UTK": ColorMatch_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ColorMatch_UTK": "Color Match (UTK)",
}
