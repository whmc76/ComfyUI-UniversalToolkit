"""
Separate Masks Node for ComfyUI Universal Toolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Separate masks functionality adapted from kjnodes.
Separates a mask into multiple masks based on connected components.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
import numpy as np
from comfy.utils import ProgressBar


class SeparateMasks_UTK:
    """
    Separate Masks node that divides a mask into multiple masks based on connected components.
    
    This node analyzes input masks and separates them into individual masks for each
    connected component that meets the size threshold requirements. Useful for isolating
    different objects or regions within a single mask.
    """
    
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("masks",)
    FUNCTION = "separate_masks"
    CATEGORY = "UniversalToolkit/Mask"
    OUTPUT_NODE = True
    
    DESCRIPTION = """
Separates a mask into multiple masks based on connected components.

The node identifies connected components (continuous regions) in the input mask
and creates separate masks for each component that meets the size thresholds.
Components are sorted by their horizontal position (left to right).

Modes:
- **area**: Preserves the exact shape of each component
- **box**: Creates rectangular bounding boxes around each component  
- **convex_polygons**: Creates simplified convex polygon approximations

Size thresholds filter out small noise or unwanted components.
Components smaller than the specified width/height are ignored.

Useful for:
- Separating multiple objects in a single mask
- Filtering components by size
- Creating individual masks for batch processing
- Object isolation and analysis
"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK", {"tooltip": "Input mask to separate into components"}),
                "size_threshold_width": ("INT", {
                    "default": 256, 
                    "min": 0, 
                    "max": 4096, 
                    "step": 1,
                    "tooltip": "Minimum width for components to be included"
                }),
                "size_threshold_height": ("INT", {
                    "default": 256, 
                    "min": 0, 
                    "max": 4096, 
                    "step": 1,
                    "tooltip": "Minimum height for components to be included"
                }),
                "mode": (["area", "box", "convex_polygons"], {
                    "default": "area",
                    "tooltip": "Method for creating separated masks"
                }),
                "max_poly_points": ("INT", {
                    "default": 8, 
                    "min": 3, 
                    "max": 32, 
                    "step": 1,
                    "tooltip": "Maximum points for polygon approximation (convex_polygons mode)"
                }),
            },
        }

    def polygon_to_mask(self, polygon, shape):
        """Convert polygon points to mask."""
        try:
            import cv2
        except ImportError:
            raise Exception("OpenCV is required for polygon operations. Please install: pip install opencv-python")
            
        mask = np.zeros((shape[0], shape[1]), dtype=np.uint8)

        if len(polygon.shape) == 2:  # Check if polygon points are valid
            polygon = polygon.astype(np.int32)
            cv2.fillPoly(mask, [polygon], 1)
        return mask

    def get_mask_polygon(self, mask_np, max_points):
        """Extract polygon approximation from mask."""
        try:
            import cv2
        except ImportError:
            raise Exception("OpenCV is required for polygon operations. Please install: pip install opencv-python")
            
        contours, _ = cv2.findContours(mask_np, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        
        largest_contour = max(contours, key=cv2.contourArea)
        hull = cv2.convexHull(largest_contour)
        
        # Initialize with smaller epsilon for more points
        perimeter = cv2.arcLength(hull, True)
        epsilon = perimeter * 0.01  # Start smaller
        
        min_eps = perimeter * 0.001  # Much smaller minimum
        max_eps = perimeter * 0.2   # Smaller maximum
        
        best_approx = None
        best_diff = float('inf')
        max_iterations = 20
        
        for i in range(max_iterations):
            curr_eps = (min_eps + max_eps) / 2
            approx = cv2.approxPolyDP(hull, curr_eps, True)
            points_diff = len(approx) - max_points
            
            if abs(points_diff) < best_diff:
                best_approx = approx
                best_diff = abs(points_diff)
            
            if len(approx) > max_points:
                min_eps = curr_eps * 1.1  # More gradual adjustment
            elif len(approx) < max_points:
                max_eps = curr_eps * 0.9  # More gradual adjustment
            else:
                return approx.squeeze()
            
            if abs(max_eps - min_eps) < perimeter * 0.0001:  # Relative tolerance
                break
        
        # If we didn't find exact match, return best approximation
        return best_approx.squeeze() if best_approx is not None else hull.squeeze()

    def separate_masks(self, mask, size_threshold_width, size_threshold_height, mode, max_poly_points):
        """
        Separate mask into individual component masks.
        
        Args:
            mask: Input mask tensor
            size_threshold_width: Minimum width for components
            size_threshold_height: Minimum height for components
            mode: Separation mode ('area', 'box', 'convex_polygons')
            max_poly_points: Maximum points for polygon approximation
            
        Returns:
            Tuple containing separated masks tensor
        """
        try:
            from scipy.ndimage import label
        except ImportError:
            raise Exception("SciPy is required for connected component analysis. Please install: pip install scipy")
        
        B, H, W = mask.shape
        separated = []

        mask = mask.round()
        
        for b in range(B):
            mask_np = mask[b].cpu().numpy().astype(np.uint8)
            structure = np.ones((3, 3), dtype=np.int8)
            labeled, ncomponents = label(mask_np, structure=structure)
            pbar = ProgressBar(ncomponents)
            
            for component in range(1, ncomponents + 1):
                component_mask_np = (labeled == component).astype(np.uint8)
                
                # Find bounding box
                rows = np.any(component_mask_np, axis=1)
                cols = np.any(component_mask_np, axis=0)
                
                if not np.any(rows) or not np.any(cols):
                    pbar.update(1)
                    continue
                    
                y_min, y_max = np.where(rows)[0][[0, -1]]
                x_min, x_max = np.where(cols)[0][[0, -1]]
                
                width = x_max - x_min + 1
                height = y_max - y_min + 1
                centroid_x = (x_min + x_max) / 2  # Calculate x centroid
                
                print(f"Component {component}: width={width}, height={height}, x_pos={centroid_x}")
                
                # Check size thresholds
                if width >= size_threshold_width and height >= size_threshold_height:
                    if mode == "convex_polygons":
                        polygon = self.get_mask_polygon(component_mask_np, max_poly_points)
                        if polygon is not None:
                            poly_mask = self.polygon_to_mask(polygon, (H, W))
                            poly_mask = torch.tensor(poly_mask, device=mask.device, dtype=torch.float32)
                            separated.append((centroid_x, poly_mask))
                    elif mode == "box":
                        # Create bounding box mask
                        box_mask = np.zeros((H, W), dtype=np.uint8)
                        box_mask[y_min:y_max+1, x_min:x_max+1] = 1
                        box_mask = torch.tensor(box_mask, device=mask.device, dtype=torch.float32)
                        separated.append((centroid_x, box_mask))
                    else:  # mode == "area"
                        area_mask = torch.tensor(component_mask_np, device=mask.device, dtype=torch.float32)
                        separated.append((centroid_x, area_mask))
                        
                pbar.update(1)
        
        if len(separated) > 0:
            # Sort by x position and extract only the masks
            separated.sort(key=lambda x: x[0])
            separated = [x[1] for x in separated]
            out_masks = torch.stack(separated, dim=0)
            return (out_masks,)
        else:
            # Return empty mask if no components found
            empty_mask = torch.zeros((1, H, W), device=mask.device, dtype=torch.float32)
            return (empty_mask,)


# Node registration
NODE_CLASS_MAPPINGS = {
    "SeparateMasks_UTK": SeparateMasks_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeparateMasks_UTK": "Separate Masks (UTK)",
}
