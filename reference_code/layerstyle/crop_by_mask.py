import torch

from .imagefunc import log, tensor2pil, pil2tensor, mask2image, image2mask, gaussian_blur, min_bounding_rect, max_inscribed_rect, mask_area
from .imagefunc import num_round_up_to_multiple, draw_rect



class CropByMask:

    def __init__(self):
        self.NODE_NAME = 'CropByMask'

    @classmethod
    def INPUT_TYPES(self):
        detect_mode = ['min_bounding_rect', 'max_inscribed_rect', 'mask_area']
        return {
            "required": {
                "image": ("IMAGE", ),  #
                "mask_for_crop": ("MASK",),
                "invert_mask": ("BOOLEAN", {"default": False}),  # 反转mask#
                "detect": (detect_mode,),
                "top_reserve": ("INT", {"default": 20, "min": -9999, "max": 9999, "step": 1}),
                "bottom_reserve": ("INT", {"default": 20, "min": -9999, "max": 9999, "step": 1}),
                "left_reserve": ("INT", {"default": 20, "min": -9999, "max": 9999, "step": 1}),
                "right_reserve": ("INT", {"default": 20, "min": -9999, "max": 9999, "step": 1}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "BOX", "IMAGE",)
    RETURN_NAMES = ("croped_image", "croped_mask", "crop_box", "box_preview")
    FUNCTION = 'crop_by_mask'
    CATEGORY = '😺dzNodes/LayerUtility'

    def crop_by_mask(self, image, mask_for_crop, invert_mask, detect,
                  top_reserve, bottom_reserve, left_reserve, right_reserve
                  ):

        ret_images = []
        ret_masks = []
        l_images = []
        l_masks = []


        for l in image:
            l_images.append(torch.unsqueeze(l, 0))
        if mask_for_crop.dim() == 2:
            mask_for_crop = torch.unsqueeze(mask_for_crop, 0)
        # 如果有多张mask输入，使用第一张
        if mask_for_crop.shape[0] > 1:
            log(f"Warning: Multiple mask inputs, using the first.", message_type='warning')
            mask_for_crop = torch.unsqueeze(mask_for_crop[0], 0)
        if invert_mask:
            mask_for_crop = 1 - mask_for_crop
        l_masks.append(tensor2pil(torch.unsqueeze(mask_for_crop, 0)).convert('L'))

        _mask = mask2image(mask_for_crop)
        bluredmask = gaussian_blur(_mask, 20).convert('L')
        x = 0
        y = 0
        width = 0
        height = 0
        if detect == "min_bounding_rect":
            (x, y, width, height) = min_bounding_rect(bluredmask)
        elif detect == "max_inscribed_rect":
            (x, y, width, height) = max_inscribed_rect(bluredmask)
        else:
            (x, y, width, height) = mask_area(_mask)

        width = num_round_up_to_multiple(width, 8)
        height = num_round_up_to_multiple(height, 8)
        log(f"{self.NODE_NAME}: Box detected. x={x},y={y},width={width},height={height}")
        canvas_width, canvas_height = tensor2pil(torch.unsqueeze(image[0], 0)).convert('RGB').size
        x1 = x - left_reserve if x - left_reserve > 0 else 0
        y1 = y - top_reserve if y - top_reserve > 0 else 0
        x2 = x + width + right_reserve if x + width + right_reserve < canvas_width else canvas_width
        y2 = y + height + bottom_reserve if y + height + bottom_reserve < canvas_height else canvas_height
        preview_image = tensor2pil(mask_for_crop).convert('RGB')
        preview_image = draw_rect(preview_image, x, y, width, height, line_color="#F00000", line_width=(width+height)//100)
        preview_image = draw_rect(preview_image, x1, y1, x2 - x1, y2 - y1,
                                  line_color="#00F000", line_width=(width+height)//200)
        crop_box = (x1, y1, x2, y2)
        for i in range(len(l_images)):
            _canvas = tensor2pil(l_images[i]).convert('RGB')
            _mask = l_masks[0]
            ret_images.append(pil2tensor(_canvas.crop(crop_box)))
            ret_masks.append(image2mask(_mask.crop(crop_box)))

        log(f"{self.NODE_NAME} Processed {len(ret_images)} image(s).", message_type='finish')
        return (torch.cat(ret_images, dim=0), torch.cat(ret_masks, dim=0), list(crop_box), pil2tensor(preview_image),)


NODE_CLASS_MAPPINGS = {
    "LayerUtility: CropByMask": CropByMask
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LayerUtility: CropByMask": "LayerUtility: CropByMask"
}