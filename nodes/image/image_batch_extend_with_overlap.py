"""
Image Batch Extend With Overlap Node (UTK)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Port from comfyui-kjnodes. Helper for video/image sequence extension with
overlap blending. Outputs source images, start frames for extension, and
extended sequence (when new_images is provided).

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch


def _overlap_modes():
    modes = ["cut", "linear_blend", "ease_in_out", "filmic_crossfade"]
    try:
        import kornia  # noqa: F401
        modes.append("perceptual_crossfade")
    except Exception:
        pass
    return modes


class ImageBatchExtendWithOverlap_UTK:
    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE")
    RETURN_NAMES = ("source_images", "start_images", "extended_images")
    OUTPUT_TOOLTIPS = (
        "The original source images (passthrough)",
        "The input images used as the starting point for extension",
        "The extended images with overlap, if no new images are provided this will be empty",
    )
    FUNCTION = "imagesfrombatch"
    CATEGORY = "UniversalToolkit/Image"
    DESCRIPTION = """
Helper node for video generation extension.
First input source and overlap amount to get the starting frames for the extension.
Then on another copy of the node provide the newly generated frames and choose how to overlap them.
"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "source_images": ("IMAGE", {"tooltip": "The source images to extend"}),
                "overlap": ("INT", {"default": 13, "min": 1, "max": 4096, "step": 1, "tooltip": "Number of overlapping frames between source and new images"}),
                "overlap_side": (["source", "new_images"], {"default": "source", "tooltip": "Which side to overlap on"}),
                "overlap_mode": (_overlap_modes(), {"default": "linear_blend", "tooltip": "Method to use for overlapping frames"}),
            },
            "optional": {
                "new_images": ("IMAGE", {"tooltip": "The new images to extend with"}),
            },
        }

    def imagesfrombatch(self, source_images, overlap, overlap_side, overlap_mode, new_images=None):
        if overlap >= len(source_images):
            return (source_images, source_images, source_images)

        if new_images is not None:
            if source_images.shape[1:3] != new_images.shape[1:3]:
                raise ValueError(
                    f"Source and new images must have the same shape: {source_images.shape[1:3]} vs {new_images.shape[1:3]}"
                )
            prefix = source_images[:-overlap]
            if overlap_side == "source":
                blend_src = source_images[-overlap:]
                blend_dst = new_images[:overlap]
            else:
                blend_src = new_images[:overlap]
                blend_dst = source_images[-overlap:]
            suffix = new_images[overlap:]

            if overlap_mode == "linear_blend":
                alpha = torch.linspace(0, 1, overlap + 2, device=blend_src.device, dtype=blend_src.dtype)[1:-1]
                alpha = alpha.view(-1, 1, 1, 1)
                blended_images = (1 - alpha) * blend_src + alpha * blend_dst
                extended_images = torch.cat((prefix, blended_images, suffix), dim=0)

            elif overlap_mode == "filmic_crossfade":
                gamma = 2.2
                alpha = torch.linspace(0, 1, overlap + 2, device=blend_src.device, dtype=blend_src.dtype)[1:-1]
                alpha = alpha.view(-1, 1, 1, 1)
                linear_src = torch.pow(blend_src, gamma)
                linear_dst = torch.pow(blend_dst, gamma)
                blended = (1 - alpha) * linear_src + alpha * linear_dst
                blended_images = torch.pow(blended, 1.0 / gamma)
                extended_images = torch.cat((prefix, blended_images, suffix), dim=0)

            elif overlap_mode == "perceptual_crossfade":
                try:
                    import kornia
                except ImportError:
                    # Fallback to linear_blend if kornia not available at run time
                    alpha = torch.linspace(0, 1, overlap + 2, device=blend_src.device, dtype=blend_src.dtype)[1:-1]
                    alpha = alpha.view(-1, 1, 1, 1)
                    blended_images = (1 - alpha) * blend_src + alpha * blend_dst
                    extended_images = torch.cat((prefix, blended_images, suffix), dim=0)
                else:
                    alpha = torch.linspace(0, 1, overlap + 2, device=blend_src.device, dtype=blend_src.dtype)[1:-1]
                    src_nchw = blend_src.movedim(-1, 1)
                    dst_nchw = blend_dst.movedim(-1, 1)
                    lab_src = kornia.color.rgb_to_lab(src_nchw)
                    lab_dst = kornia.color.rgb_to_lab(dst_nchw)
                    alpha = alpha.view(-1, 1, 1, 1)
                    blended_lab = (1 - alpha) * lab_src + alpha * lab_dst
                    blended_rgb = kornia.color.lab_to_rgb(blended_lab)
                    blended_images = blended_rgb.movedim(1, -1)
                    extended_images = torch.cat((prefix, blended_images, suffix), dim=0)

            elif overlap_mode == "ease_in_out":
                t = torch.linspace(0, 1, overlap + 2, device=blend_src.device, dtype=blend_src.dtype)[1:-1]
                eased_t = 3 * t * t - 2 * t * t * t
                eased_t = eased_t.view(-1, 1, 1, 1)
                blended_images = (1 - eased_t) * blend_src + eased_t * blend_dst
                extended_images = torch.cat((prefix, blended_images, suffix), dim=0)

            else:  # cut
                if overlap_side == "new_images":
                    extended_images = torch.cat((source_images, new_images[overlap:]), dim=0)
                else:
                    extended_images = torch.cat((source_images[:-overlap], new_images), dim=0)
        else:
            dev = source_images.device
            dtype = source_images.dtype
            extended_images = torch.zeros((1, 64, 64, 3), device=dev, dtype=dtype)

        start_images = source_images[-overlap:]
        return (source_images, start_images, extended_images)


NODE_CLASS_MAPPINGS = {
    "ImageBatchExtendWithOverlap_UTK": ImageBatchExtendWithOverlap_UTK,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageBatchExtendWithOverlap_UTK": "Image Batch Extend With Overlap (UTK)",
}
