"""
Image Concatenate Multi Node (UTK)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

版本: 1.4.0
最后更新: 2024-12-19
作者: May

变更日志：
- v1.4.0: 修复节点分类，从KJNodes/image改为UniversalToolkit/Image，保持与其他image节点一致性。
- v1.3.0: 移除grid_size参数，增加gap参数，支持拼接间距设置。
- v1.2.0: 默认启用智能拼接（smart），支持2~4图，自动等比缩放，逐步拼接，输出接近正方形。
- v1.1.x: 支持sequential/smart两种模式，拼接逻辑优化。
- v1.0.0: 初始版本，基础多图拼接。

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch
import math

class ImageConcatenateMulti_UTK:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_1": ("IMAGE", ),
                "image_2": ("IMAGE", ),
                "mode": (["sequential", "smart"], {"default": "smart"}),
                "direction": (
                    ['right', 'down', 'left', 'up'],
                    {"default": 'right'}
                ),
                "match_image_size": ("BOOLEAN", {"default": False}),
                "max_size": ("INT", {"default": 4096, "min": 64, "max": 8192, "step": 64}),
                "background_color": (["black", "white", "gray", "transparent"], {"default": "black"}),
                "gap": ("INT", {"default": 0, "min": 0, "max": 256, "step": 1}),
            },
            "optional": {
                "image_3": ("IMAGE", ),
                "image_4": ("IMAGE", ),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "combine"
    CATEGORY = "UniversalToolkit/Image"
    DESCRIPTION = """
Creates an image from multiple images.  
你可以设置inputcount来决定输入端口数量，
并支持顺序拼接(sequential)和正方形智能布局(square)两种模式。
"""

    def combine(self, mode, direction, match_image_size, max_size, background_color, gap, image_1, image_2, image_3=None, image_4=None):
        images = [image_1, image_2]
        if image_3 is not None:
            images.append(image_3)
        if image_4 is not None:
            images.append(image_4)
        if mode == "smart":
            img = images[0]
            for ni in images[1:]:
                img, = self._smart_pair_concatenate(img, ni, max_size, background_color, gap)
            return (img,)
        image = images[0]
        for new_image in images[1:]:
            image, = self._sequential_concatenate(
                image, new_image, direction, match_image_size, max_size, background_color, gap
            )
        return (image,)

    def _sequential_concatenate(self, image1, image2, direction, match_image_size, max_size, background_color, gap):
        h1, w1 = image1.shape[1:3]
        h2, w2 = image2.shape[1:3]
        if direction == 'auto':
            horizontal_ratio = (w1 + w2) / max(h1, h2)
            vertical_ratio = max(w1, w2) / (h1 + h2)
            direction = 'right' if abs(horizontal_ratio - 1) <= abs(vertical_ratio - 1) else 'down'
        if match_image_size:
            if direction in ['right', 'left']:
                target_height = max(h1, h2)
                if h1 < target_height:
                    scale = target_height / h1
                    new_width = int(w1 * scale)
                    image1 = torch.nn.functional.interpolate(
                        image1.permute(0, 3, 1, 2),
                        size=(target_height, new_width),
                        mode='bilinear',
                        align_corners=False
                    ).permute(0, 2, 3, 1)
                if h2 < target_height:
                    scale = target_height / h2
                    new_width = int(w2 * scale)
                    image2 = torch.nn.functional.interpolate(
                        image2.permute(0, 3, 1, 2),
                        size=(target_height, new_width),
                        mode='bilinear',
                        align_corners=False
                    ).permute(0, 2, 3, 1)
            else:
                target_width = max(w1, w2)
                if w1 < target_width:
                    scale = target_width / w1
                    new_height = int(h1 * scale)
                    image1 = torch.nn.functional.interpolate(
                        image1.permute(0, 3, 1, 2),
                        size=(new_height, target_width),
                        mode='bilinear',
                        align_corners=False
                    ).permute(0, 2, 3, 1)
                if w2 < target_width:
                    scale = target_width / w2
                    new_height = int(h2 * scale)
                    image2 = torch.nn.functional.interpolate(
                        image2.permute(0, 3, 1, 2),
                        size=(new_height, target_width),
                        mode='bilinear',
                        align_corners=False
                    ).permute(0, 2, 3, 1)
        h1, w1 = image1.shape[1:3]
        h2, w2 = image2.shape[1:3]
        if direction in ['right', 'left']:
            final_height = max(h1, h2)
            final_width = w1 + w2 + (gap if gap > 0 else 0)
        else:
            final_height = h1 + h2 + (gap if gap > 0 else 0)
            final_width = max(w1, w2)
        if max(final_height, final_width) > max_size:
            scale = max_size / max(final_height, final_width)
            new_h1 = int(h1 * scale)
            new_w1 = int(w1 * scale)
            new_h2 = int(h2 * scale)
            new_w2 = int(w2 * scale)
            image1 = torch.nn.functional.interpolate(
                image1.permute(0, 3, 1, 2),
                size=(new_h1, new_w1),
                mode='bilinear',
                align_corners=False
            ).permute(0, 2, 3, 1)
            image2 = torch.nn.functional.interpolate(
                image2.permute(0, 3, 1, 2),
                size=(new_h2, new_w2),
                mode='bilinear',
                align_corners=False
            ).permute(0, 2, 3, 1)
            h1, w1 = image1.shape[1:3]
            h2, w2 = image2.shape[1:3]
            if direction in ['right', 'left']:
                final_height = max(h1, h2)
                final_width = w1 + w2 + (gap if gap > 0 else 0)
            else:
                final_height = h1 + h2 + (gap if gap > 0 else 0)
                final_width = max(w1, w2)
        if background_color == "transparent":
            output = torch.zeros((1, final_height, final_width, image1.shape[-1]), dtype=image1.dtype, device=image1.device)
        else:
            color_value = 1.0 if background_color == "white" else 0.0 if background_color == "black" else 0.5
            output = torch.full((1, final_height, final_width, image1.shape[-1]), color_value, dtype=image1.dtype, device=image1.device)
        if direction == 'right':
            x1 = 0
            x2 = w1 + (gap if gap > 0 else 0)
            y1 = (final_height - h1) // 2
            y2 = (final_height - h2) // 2
        elif direction == 'left':
            x1 = w2 + (gap if gap > 0 else 0)
            x2 = 0
            y1 = (final_height - h1) // 2
            y2 = (final_height - h2) // 2
        elif direction == 'down':
            x1 = (final_width - w1) // 2
            x2 = (final_width - w2) // 2
            y1 = 0
            y2 = h1 + (gap if gap > 0 else 0)
        else:  # up
            x1 = (final_width - w1) // 2
            x2 = (final_width - w2) // 2
            y1 = h2 + (gap if gap > 0 else 0)
            y2 = 0
        output[:, y1:y1+h1, x1:x1+w1] = image1
        output[:, y2:y2+h2, x2:x2+w2] = image2
        return (output,)

    def _square_concatenate(self, images, max_size, background_color):
        batch_size = images.shape[0]
        grid_size = math.ceil(math.sqrt(batch_size))
        rows = cols = grid_size
        original_heights = []
        original_widths = []
        for i in range(batch_size):
            h, w = images[i].shape[:2]
            original_heights.append(h)
            original_widths.append(w)
        total_area = sum(h * w for h, w in zip(original_heights, original_widths))
        target_canvas_size = math.sqrt(total_area)
        if target_canvas_size > max_size:
            target_canvas_size = max_size
        cell_width = int(target_canvas_size / cols)
        cell_height = int(target_canvas_size / rows)
        cell_width = max(cell_width, 64)
        cell_height = max(cell_height, 64)
        final_width = cell_width * cols
        final_height = cell_height * rows
        if background_color == "transparent":
            output = torch.zeros((1, final_height, final_width, images.shape[-1]), dtype=images.dtype, device=images.device)
        else:
            color_value = 1.0 if background_color == "white" else 0.0 if background_color == "black" else 0.5
            output = torch.full((1, final_height, final_width, images.shape[-1]), color_value, dtype=images.dtype, device=images.device)
        for i in range(batch_size):
            row = i // cols
            col = i % cols
            x_offset = col * cell_width
            y_offset = row * cell_height
            scaled_image = torch.nn.functional.interpolate(
                images[i].unsqueeze(0).permute(0, 3, 1, 2),
                size=(cell_height, cell_width),
                mode='bilinear',
                align_corners=False
            ).permute(0, 2, 3, 1).squeeze(0)
            output[0, y_offset:y_offset+cell_height, x_offset:x_offset+cell_width] = scaled_image
        return (output,)

    def _smart_pair_concatenate(self, img1, img2, max_size, background_color, gap):
        b, h1, w1, c = img1.shape
        b2, h2, w2, c2 = img2.shape
        target_height = max(h1, h2)
        scale1_h = target_height / h1
        scale2_h = target_height / h2
        w1_h = int(w1 * scale1_h)
        w2_h = int(w2 * scale2_h)
        target_width = max(w1, w2)
        scale1_w = target_width / w1
        scale2_w = target_width / w2
        h1_w = int(h1 * scale1_w)
        h2_w = int(h2 * scale2_w)
        out_w_h = w1_h + w2_h + (gap if gap > 0 else 0)
        out_h_h = target_height
        out_w_w = target_width
        out_h_w = h1_w + h2_w + (gap if gap > 0 else 0)
        ratio_h = max(out_w_h, out_h_h) / min(out_w_h, out_h_h)
        ratio_w = max(out_w_w, out_h_w) / min(out_w_w, out_h_w)
        if abs(ratio_h - 1) <= abs(ratio_w - 1):
            img1r = torch.nn.functional.interpolate(img1.permute(0, 3, 1, 2), size=(target_height, w1_h), mode='bilinear', align_corners=False).permute(0, 2, 3, 1)
            img2r = torch.nn.functional.interpolate(img2.permute(0, 3, 1, 2), size=(target_height, w2_h), mode='bilinear', align_corners=False).permute(0, 2, 3, 1)
            final_height = target_height
            final_width = w1_h + w2_h + (gap if gap > 0 else 0)
            if max(final_height, final_width) > max_size:
                scale = max_size / max(final_height, final_width)
                new_height = int(final_height * scale)
                new_w1 = int(w1_h * scale)
                new_w2 = int(w2_h * scale)
                img1r = torch.nn.functional.interpolate(img1r.permute(0, 3, 1, 2), size=(new_height, new_w1), mode='bilinear', align_corners=False).permute(0, 2, 3, 1)
                img2r = torch.nn.functional.interpolate(img2r.permute(0, 3, 1, 2), size=(new_height, new_w2), mode='bilinear', align_corners=False).permute(0, 2, 3, 1)
                final_height = new_height
                final_width = new_w1 + new_w2 + (gap if gap > 0 else 0)
            if background_color == "transparent":
                output = torch.zeros((1, final_height, final_width, img1.shape[-1]), dtype=img1.dtype, device=img1.device)
            else:
                color_value = 1.0 if background_color == "white" else 0.0 if background_color == "black" else 0.5
                output = torch.full((1, final_height, final_width, img1.shape[-1]), color_value, dtype=img1.dtype, device=img1.device)
            output[:, :, :img1r.shape[2]] = img1r
            output[:, :, img1r.shape[2]+(gap if gap > 0 else 0):] = img2r
        else:
            img1r = torch.nn.functional.interpolate(img1.permute(0, 3, 1, 2), size=(h1_w, target_width), mode='bilinear', align_corners=False).permute(0, 2, 3, 1)
            img2r = torch.nn.functional.interpolate(img2.permute(0, 3, 1, 2), size=(h2_w, target_width), mode='bilinear', align_corners=False).permute(0, 2, 3, 1)
            final_height = h1_w + h2_w + (gap if gap > 0 else 0)
            final_width = target_width
            if max(final_height, final_width) > max_size:
                scale = max_size / max(final_height, final_width)
                new_width = int(final_width * scale)
                new_h1 = int(h1_w * scale)
                new_h2 = int(h2_w * scale)
                img1r = torch.nn.functional.interpolate(img1r.permute(0, 3, 1, 2), size=(new_h1, new_width), mode='bilinear', align_corners=False).permute(0, 2, 3, 1)
                img2r = torch.nn.functional.interpolate(img2r.permute(0, 3, 1, 2), size=(new_h2, new_width), mode='bilinear', align_corners=False).permute(0, 2, 3, 1)
                final_height = new_h1 + new_h2 + (gap if gap > 0 else 0)
                final_width = new_width
            if background_color == "transparent":
                output = torch.zeros((1, final_height, final_width, img1.shape[-1]), dtype=img1.dtype, device=img1.device)
            else:
                color_value = 1.0 if background_color == "white" else 0.0 if background_color == "black" else 0.5
                output = torch.full((1, final_height, final_width, img1.shape[-1]), color_value, dtype=img1.dtype, device=img1.device)
            output[:, :img1r.shape[1], :] = img1r
            output[:, img1r.shape[1]+(gap if gap > 0 else 0):, :] = img2r
        return (output,)

NODE_CLASS_MAPPINGS = {
    "ImageConcatenateMulti_UTK": ImageConcatenateMulti_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageConcatenateMulti_UTK": "Image Concatenate Multi (UTK)",
} 