"""
Save Image Plus Node
~~~~~~~~~~~~~~~~~~~~

Save images with custom DPI, format, quality and metadata for print-ready output.
Supports PNG, JPEG, TIFF, WebP formats with configurable DPI (default 300 DPI for printing).

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import os
import json

import numpy as np
import folder_paths
from PIL import Image
from PIL.PngImagePlugin import PngInfo


class SaveImagePlus_UTK:
    """Save images with custom DPI, format and metadata for print-ready output."""

    CATEGORY = "UniversalToolkit/Image"
    OUTPUT_NODE = True
    DESCRIPTION = (
        "Save images with custom DPI metadata for professional print output. "
        "Supports PNG, JPEG, TIFF, WebP. Default 300 DPI is standard for print quality. "
        "Optionally embeds ComfyUI workflow, author and description metadata."
    )

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": (
                    "STRING",
                    {
                        "default": "ComfyUI/PrintReady",
                        "tooltip": "Filename prefix. Use '/' for subfolders, e.g. 'prints/my_image'.",
                    },
                ),
                "file_format": (
                    ["PNG", "JPEG", "TIFF", "WEBP"],
                    {
                        "default": "PNG",
                        "tooltip": "Output file format. TIFF is best for professional print workflows.",
                    },
                ),
                "dpi": (
                    "INT",
                    {
                        "default": 300,
                        "min": 72,
                        "max": 1200,
                        "step": 1,
                        "tooltip": "DPI (dots per inch) embedded in file metadata. 300 = standard print, 72 = screen.",
                    },
                ),
                "quality": (
                    "INT",
                    {
                        "default": 95,
                        "min": 1,
                        "max": 100,
                        "step": 1,
                        "tooltip": "Compression quality for JPEG/WEBP (1-100). Has no effect on PNG/TIFF.",
                    },
                ),
                "png_compress_level": (
                    "INT",
                    {
                        "default": 6,
                        "min": 0,
                        "max": 9,
                        "step": 1,
                        "tooltip": "PNG ZLIB compression level (0=none/fastest, 9=max/slowest). Only affects PNG.",
                    },
                ),
                "save_workflow": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "Embed ComfyUI workflow JSON into the image metadata (PNG/TIFF only).",
                    },
                ),
            },
            "optional": {
                "author": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "Author name to embed in image metadata.",
                    },
                ),
                "description": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Image description to embed in metadata.",
                    },
                ),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_image_plus"

    def save_image_plus(
        self,
        images,
        filename_prefix,
        file_format,
        dpi,
        quality,
        png_compress_level,
        save_workflow,
        author="",
        description="",
        prompt=None,
        extra_pnginfo=None,
    ):
        full_output_folder, filename, counter, subfolder, filename_prefix = (
            folder_paths.get_save_image_path(
                filename_prefix,
                self.output_dir,
                images[0].shape[1],
                images[0].shape[0],
            )
        )

        ext_map = {"PNG": "png", "JPEG": "jpg", "TIFF": "tif", "WEBP": "webp"}
        ext = ext_map[file_format]
        dpi_tuple = (dpi, dpi)
        results = []

        for batch_number, image in enumerate(images):
            # Tensor → uint8 numpy → PIL
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            filename_with_batch = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch}_{counter:05}_.{ext}"
            file_path = os.path.join(full_output_folder, file)

            if file_format == "PNG":
                self._save_png(
                    img, file_path, dpi_tuple, png_compress_level,
                    save_workflow, author, description, prompt, extra_pnginfo,
                )

            elif file_format == "JPEG":
                self._save_jpeg(img, file_path, dpi_tuple, quality, author, description)

            elif file_format == "TIFF":
                self._save_tiff(
                    img, file_path, dpi_tuple, save_workflow,
                    author, description, prompt, extra_pnginfo,
                )

            elif file_format == "WEBP":
                self._save_webp(img, file_path, dpi_tuple, quality, author, description)

            results.append({"filename": file, "subfolder": subfolder, "type": self.type})
            counter += 1

            print(f"✅ SaveImagePlus (UTK): Saved '{file}' [{file_format}, {dpi} DPI]")

        return {"ui": {"images": results}}

    # ------------------------------------------------------------------ #
    #  Format-specific save helpers                                        #
    # ------------------------------------------------------------------ #

    def _save_png(
        self, img, path, dpi_tuple, compress_level,
        save_workflow, author, description, prompt, extra_pnginfo
    ):
        metadata = PngInfo()
        if save_workflow:
            if prompt is not None:
                metadata.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for key, value in extra_pnginfo.items():
                    metadata.add_text(key, json.dumps(value))
        if author:
            metadata.add_text("Author", author)
        if description:
            metadata.add_text("Description", description)

        img.save(
            path,
            format="PNG",
            pnginfo=metadata,
            compress_level=compress_level,
            dpi=dpi_tuple,
        )

    def _save_jpeg(self, img, path, dpi_tuple, quality, author, description):
        # JPEG requires RGB
        if img.mode != "RGB":
            img = img.convert("RGB")

        save_kwargs = {"format": "JPEG", "quality": quality, "dpi": dpi_tuple}

        # Optionally embed author/description via EXIF using piexif
        exif_bytes = self._build_jpeg_exif(dpi_tuple[0], author, description)
        if exif_bytes is not None:
            save_kwargs["exif"] = exif_bytes

        img.save(path, **save_kwargs)

    def _save_tiff(
        self, img, path, dpi_tuple, save_workflow,
        author, description, prompt, extra_pnginfo
    ):
        from PIL import TiffImagePlugin

        tiffinfo = TiffImagePlugin.ImageFileDirectory_v2()

        # Standard TIFF tags
        # 270 = ImageDescription, 305 = Software, 315 = Artist
        desc_parts = []
        if description:
            desc_parts.append(description)
        if save_workflow and prompt is not None:
            desc_parts.append("ComfyUI workflow: " + json.dumps(prompt))
        if save_workflow and extra_pnginfo is not None:
            for key, value in extra_pnginfo.items():
                desc_parts.append(f"{key}: {json.dumps(value)}")

        if desc_parts:
            tiffinfo[270] = "\n\n".join(desc_parts)

        if author:
            tiffinfo[315] = author

        tiffinfo[305] = "ComfyUI SaveImagePlus (UTK)"

        img.save(
            path,
            format="TIFF",
            dpi=dpi_tuple,
            compression="tiff_lzw",
            tiffinfo=tiffinfo,
        )

    def _save_webp(self, img, path, dpi_tuple, quality, author, description):
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        save_kwargs = {"format": "WEBP", "quality": quality}

        # WebP supports EXIF for DPI metadata
        exif_bytes = self._build_jpeg_exif(dpi_tuple[0], author, description)
        if exif_bytes is not None:
            save_kwargs["exif"] = exif_bytes

        img.save(path, **save_kwargs)

    # ------------------------------------------------------------------ #
    #  EXIF helper (piexif optional)                                       #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _build_jpeg_exif(dpi: int, author: str, description: str):
        """Build EXIF bytes with DPI, author, description using piexif if available."""
        try:
            import piexif  # optional dependency

            ifd = {
                piexif.ImageIFD.XResolution: (dpi, 1),
                piexif.ImageIFD.YResolution: (dpi, 1),
                piexif.ImageIFD.ResolutionUnit: 2,  # 2 = inch (DPI)
            }
            if author:
                ifd[piexif.ImageIFD.Artist] = author.encode("utf-8")
            if description:
                ifd[piexif.ImageIFD.ImageDescription] = description.encode("utf-8")

            exif_dict = {"0th": ifd}
            return piexif.dump(exif_dict)
        except ImportError:
            return None


NODE_CLASS_MAPPINGS = {
    "SaveImagePlus_UTK": SaveImagePlus_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImagePlus_UTK": "Save Image Plus (UTK)",
}
