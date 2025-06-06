from PIL import Image
import numpy as np
import torch
import re

class EmptyUnitGenerator:
    CATEGORY = "UniversalToolkit"
    @classmethod
    def INPUT_TYPES(cls):
        # 标准比例选项
        STANDARD_RATIOS = [
            ("1:1", [(1024, 1024), (2048, 2048)]),
            ("3:2", [(1200, 800), (800, 1200)]),
            ("4:3", [(1600, 1200), (1200, 1600)]),
            ("8:5", [(1280, 800), (800, 1280)]),
            ("16:9", [(1920, 1080), (1080, 1920)]),
            ("21:9", [(2520, 1080), (1080, 2520)]),
        ]
        standard_options = []
        for ratio, sizes in STANDARD_RATIOS:
            for w, h in sizes:
                orientation = "横向" if w >= h else "纵向"
                standard_options.append(f"{ratio} {orientation} ({w}x{h})")

        # 社交媒体分辨率
        social_options = [
            "Instagram Portrait - 1080x1350",
            "Instagram Square - 1080x1080",
            "Instagram Landscape - 1080x608",
            "Instagram Stories/Reels - 1080x1920",
            "Facebook Landscape - 1080x1350",
            "Facebook Marketplace - 1200x1200",
            "Facebook Stories - 1080x1920",
            "TikTok - 1080x1920",
            "YouTube Banner - 2560x1440",
            "LinkedIn Profile Banner - 1584x396",
            "LinkedIn Page Cover - 1128x191",
            "LinkedIn Post - 1200x627",
            "Pinterest Pin Image - 1000x1500",
            "CivitAI Cover - 1600x400",
            "OpenArt App - 1500x1000",
        ]

        return {
            "required": {
                "ratio_type": (["standard", "social media"], {"default": "standard", "label": "比例类型"}),
                "ratio": (standard_options, {"default": standard_options[0], "label": "尺寸/比例", "dynamic": True, "depends_on": ["ratio_type"]}),
                "image_color": (["white", "black", "gray", "red", "green", "blue"], {"default": "white", "label": "Image Color"}),
                "batch": ("INT", {"default": 1, "min": 1, "max": 16, "step": 1, "label": "输出组数(batch)"}),
            },
            "optional": {},
            "dynamic": {
                "ratio": lambda params: standard_options if params.get("ratio_type", "standard") == "standard" else social_options
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "LATENT")
    RETURN_NAMES = ("image", "mask", "latent")
    FUNCTION = "generate"

    def generate(self, ratio_type, ratio, image_color, batch):
        # 解析分辨率
        if ratio_type == "standard":
            m = re.search(r"\((\d+)x(\d+)\)", ratio)
            width, height = int(m.group(1)), int(m.group(2))
        else:
            m = re.search(r"(\d+)x(\d+)", ratio)
            width, height = int(m.group(1)), int(m.group(2))
        COLOR_OPTIONS = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "gray": (128, 128, 128),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
        }
        color_rgb = COLOR_OPTIONS[image_color]
        images = []
        masks = []
        latents = []
        for _ in range(batch):
            image = torch.from_numpy(np.array(Image.new("RGB", (width, height), color_rgb))).float() / 255.0
            mask = torch.from_numpy(np.array(Image.new("L", (width, height), 0))).unsqueeze(-1).float() / 255.0
            latent = torch.from_numpy(np.zeros((height, width, 4), dtype=np.float32))
            images.append(image)
            masks.append(mask)
            latents.append(latent)
        return tuple(images), tuple(masks), tuple(latents) 