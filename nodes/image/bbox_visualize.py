"""
Bbox Visualize Node for ComfyUI Universal Toolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bbox visualization functionality adapted from kjnodes.
Draws bounding boxes on images for visualization purposes.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch

# Define BBOX type for ComfyUI
# BBOX is typically a list/tensor of [x, y, width, height] or [x1, y1, x2, y2]
# We'll register it as a custom type
if not hasattr(torch, 'BBOX'):
    # Register BBOX as a custom type that can hold bbox coordinates
    class BBOX:
        pass


class BboxVisualize_UTK:
    """
    Bbox Visualize node that draws bounding boxes on images.
    
    This node takes images and bounding box coordinates, then draws
    rectangular frames on the images to visualize the bounding boxes.
    Useful for debugging object detection, cropping operations, or
    highlighting specific regions in images.
    """
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "visualizebbox"
    CATEGORY = "UniversalToolkit/Image"
    
    DESCRIPTION = """
Visualizes the specified bbox on the image.
"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "bboxes": ("BBOX",),
                "line_width": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1}),
                "bbox_format": (["xywh", "xyxy"], {"default": "xywh"}),
            },
        }

    def visualizebbox(self, bboxes, images, line_width, bbox_format):
        """
        Visualizes the specified bbox on the image.
        Adapted from kjnodes implementation.
        """
        image_list = []
        for image, bbox in zip(images, bboxes):
            if bbox_format == "xywh":
                x_min, y_min, width, height = bbox
            elif bbox_format == "xyxy":
                x_min, y_min, x_max, y_max = bbox
                width = x_max - x_min
                height = y_max - y_min
            else:
                raise ValueError(f"Unknown bbox_format: {bbox_format}")

            # Ensure bbox coordinates are integers
            x_min = int(x_min)
            y_min = int(y_min)
            width = int(width)
            height = int(height)

            # Permute the image dimensions
            image = image.permute(2, 0, 1)

            # Clone the image to draw bounding boxes
            img_with_bbox = image.clone()

            # Define the color for the bbox, e.g., red
            color = torch.tensor([1, 0, 0], dtype=torch.float32)

            # Ensure color tensor matches the image channels
            if color.shape[0] != img_with_bbox.shape[0]:
                color = color.unsqueeze(1).expand(-1, line_width)

            # Draw lines for each side of the bbox with the specified line width
            for lw in range(line_width):
                # Top horizontal line
                if y_min + lw < img_with_bbox.shape[1]:
                    img_with_bbox[:, y_min + lw, x_min:x_min + width] = color[:, None]

                # Bottom horizontal line
                if y_min + height - lw < img_with_bbox.shape[1]:
                    img_with_bbox[:, y_min + height - lw, x_min:x_min + width] = color[:, None]

                # Left vertical line
                if x_min + lw < img_with_bbox.shape[2]:
                    img_with_bbox[:, y_min:y_min + height, x_min + lw] = color[:, None]

                # Right vertical line
                if x_min + width - lw < img_with_bbox.shape[2]:
                    img_with_bbox[:, y_min:y_min + height, x_min + width - lw] = color[:, None]

            # Permute the image dimensions back
            img_with_bbox = img_with_bbox.permute(1, 2, 0).unsqueeze(0)
            image_list.append(img_with_bbox)

        return (torch.cat(image_list, dim=0),)


# Node registration
NODE_CLASS_MAPPINGS = {
    "BboxVisualize_UTK": BboxVisualize_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BboxVisualize_UTK": "Bbox Visualize (UTK)",
}
