import torch
from PIL import Image
from .imagefunc import log, tensor2pil, pil2tensor
from .imagefunc import chop_mode,chop_image



class ColorOverlay:

    def __init__(self):
        self.NODE_NAME = 'ColorOverlay'

    @classmethod
    def INPUT_TYPES(self):

        return {
            "required": {
                "background_image": ("IMAGE", ),  #
                "layer_image": ("IMAGE",),  #
                "invert_mask": ("BOOLEAN", {"default": True}),  # 反转mask
                "blend_mode": (chop_mode,),  # 混合模式
                "opacity": ("INT", {"default": 100, "min": 0, "max": 100, "step": 1}),  # 透明度
                "color": ("STRING", {"default": "#FFBF30"}),  # 渐变开始颜色
            },
            "optional": {
                "layer_mask": ("MASK",),  #
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = 'color_overlay'
    CATEGORY = '😺dzNodes/LayerStyle'

    def color_overlay(self, background_image, layer_image,
                  invert_mask, blend_mode, opacity, color,
                  layer_mask=None
                  ):

        b_images = []
        l_images = []
        l_masks = []
        ret_images = []
        for b in background_image:
            b_images.append(torch.unsqueeze(b, 0))
        for l in layer_image:
            l_images.append(torch.unsqueeze(l, 0))
            m = tensor2pil(l)
            if m.mode == 'RGBA':
                l_masks.append(m.split()[-1])
        if layer_mask is not None:
            if layer_mask.dim() == 2:
                layer_mask = torch.unsqueeze(layer_mask, 0)
            l_masks = []
            for m in layer_mask:
                if invert_mask:
                    m = 1 - m
                l_masks.append(tensor2pil(torch.unsqueeze(m, 0)).convert('L'))
        if len(l_masks) == 0:
            log(f"Error: {self.NODE_NAME} skipped, because the available mask is not found.", message_type='error')
            return (background_image,)

        max_batch = max(len(b_images), len(l_images), len(l_masks))
        _color = Image.new("RGB", tensor2pil(l_images[0]).size, color=color)
        for i in range(max_batch):
            background_image = b_images[i] if i < len(b_images) else b_images[-1]
            layer_image = l_images[i] if i < len(l_images) else l_images[-1]
            _mask = l_masks[i] if i < len(l_masks) else l_masks[-1]
            # preprocess
            _canvas = tensor2pil(background_image).convert('RGB')
            _layer = tensor2pil(layer_image).convert('RGB')
            if _mask.size != _layer.size:
                _mask = Image.new('L', _layer.size, 'white')
                log(f"Warning: {self.NODE_NAME} mask mismatch, dropped!", message_type='warning')

            # 合成layer
            _comp = chop_image(_layer, _color, blend_mode, opacity)
            _canvas.paste(_comp, mask=_mask)

            ret_images.append(pil2tensor(_canvas))

        log(f"{self.NODE_NAME} Processed {len(ret_images)} image(s).", message_type='finish')
        return (torch.cat(ret_images, dim=0),)

NODE_CLASS_MAPPINGS = {
    "LayerStyle: ColorOverlay": ColorOverlay
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LayerStyle: ColorOverlay": "LayerStyle: ColorOverlay"
}