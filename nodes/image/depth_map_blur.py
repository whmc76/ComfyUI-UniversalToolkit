"""
Depth Map Blur Node
~~~~~~~~~~~~~~~~~~

Applies depth-based blur effects to images using depth maps.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import os
import cv2
import torch
import numpy as np
import folder_paths

class DepthMapBlur_UTK:
    CATEGORY = "UniversalToolkit/Image"
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "depth_map": ("IMAGE",),
                "blur_strength": ("FLOAT", {
                    "default": 64.0,
                    "min": 0.0,
                    "max": 256.0,
                    "step": 1.0
                }),
                "focal_depth": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "focus_spread": ("FLOAT", {
                    "default": 1,
                    "min": 1.0,
                    "max": 8.0,
                    "step": 0.1
                }),
                "steps": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 32,
                }),
                "focal_range": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "mask_blur": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 127,
                    "step": 2
                }),
            },
        }
    
    RETURN_TYPES = ("IMAGE","MASK")
    RETURN_NAMES = ()
    FUNCTION = "depthblur_image"
    DESCRIPTION = """
    blur_strength: Represents the blur strength. This parameter controls the overall intensity of the blur effect; the higher the value, the more blurred the image becomes.

    focal_depth: Represents the focal depth. This parameter is used to determine which depth level in the image should remain sharp, while other levels are blurred based on depth differences.

    focus_spread: Represents the focus spread range. This parameter controls the size of the blur transition area near the focal depth; the larger the value, the wider the transition area, and the smoother the blur effect spreads around the focus.

    steps: Represents the number of steps in the blur process. This parameter determines the calculation precision of the blur effect; the more steps, the finer the blur effect, but this also increases the computational load.

    focal_range: Represents the focal range. This parameter is used to adjust the depth range within the focal depth that remains sharp; the larger the value, the wider the area around the focal depth that remains sharp.
    
    mask_blur: Represents the mask blur strength for blurring the depth map. This parameter controls the intensity of the depth map's blur treatment, used for preprocessing the depth map before calculating the final blur effect, to achieve a more natural blur transition.
    """
    CATEGORY = "UniversalToolkit"

    def depthblur_image(self, image: torch.Tensor, depth_map: torch.Tensor, blur_strength: float, focal_depth: float, focus_spread:float, steps: int, focal_range: float, mask_blur: int):
        batch_size, height, width, _ = image.shape
        image_result = torch.zeros_like(image)
        mask_result = torch.zeros((batch_size, height, width), dtype=torch.float32)

        for b in range(batch_size):
            tensor_image = image[b].numpy()
            tensor_image_depth = depth_map[b].numpy()

            # Apply blur
            blur_image,depth_mask = self.apply_depthblur(tensor_image, tensor_image_depth, blur_strength, focal_depth, focus_spread, steps, focal_range, mask_blur)

            tensor_image = torch.from_numpy(blur_image).unsqueeze(0)
            tensor_mask = torch.from_numpy(depth_mask).unsqueeze(0)

            image_result[b] = tensor_image
            mask_result[b] = tensor_mask

        return (image_result,mask_result)

    def apply_depthblur(self, image, depth_map, blur_strength, focal_depth, focus_spread, steps, focal_range, mask_blur):
        def make_odd(x):
            x = int(round(x))
            return x if x % 2 == 1 else x + 1

        # Normalize the input image if needed
        needs_normalization = image.max() > 1
        if needs_normalization:
            image = image.astype(np.float32) / 255

        # Normalize the depth map if needed
        depth_map = depth_map.astype(np.float32) / 255 if depth_map.max() > 1 else depth_map

        # Resize depth map to match the image dimensions
        depth_map_resized = cv2.resize(depth_map, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_LINEAR)
        if len(depth_map_resized.shape) > 2:
            depth_map_resized = cv2.cvtColor(depth_map_resized, cv2.COLOR_BGR2GRAY)

        # Adjust the depth map based on the focal plane
        depth_mask = np.abs(depth_map_resized - focal_depth)
        depth_mask = np.clip(depth_mask / np.max(depth_mask), 0, 1)

        # Process the depth_mask
        depth_mask[depth_mask < focal_range] = 0
        depth_mask[depth_mask >= focal_range] = (depth_mask[depth_mask >= focal_range] - focal_range) / (1 - focal_range)

        # Apply mask blur
        mask_blur = max(1, make_odd(mask_blur))
        depth_mask = cv2.GaussianBlur(depth_mask, (mask_blur, mask_blur), 0)

        # Generate blurred versions of the image
        blur_ksize = max(1, make_odd(blur_strength))
        blurred_images = [cv2.GaussianBlur(image, (blur_ksize, blur_ksize), sigmaX=0) for _ in range(steps)]

        # Use the adjusted depth map as a mask for applying blurred images
        # 这里简单实现：直接用最重的模糊图和原图按mask混合
        final_image = image * (1 - depth_mask[..., None]) + blurred_images[-1] * depth_mask[..., None]

        # Convert back to original range if the image was normalized
        if needs_normalization:
            final_image = np.clip(final_image * 255, 0, 255).astype(np.uint8)

        return final_image, depth_mask

# Node mappings
NODE_CLASS_MAPPINGS = {
    "DepthMapBlur_UTK": DepthMapBlur_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DepthMapBlur_UTK": "Depth Map Blur (UTK)",
} 