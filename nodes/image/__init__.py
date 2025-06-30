"""
ComfyUI Universal Toolkit - Image Nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Image processing nodes for ComfyUI Universal Toolkit.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import os
import importlib

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# 自动导入本目录下所有节点文件的注册表
for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith('.py') and filename not in ('__init__.py', 'image_utils.py', 'image_converters.py'):
        modulename = filename[:-3]
        module = importlib.import_module(f'.{modulename}', __package__)
        if hasattr(module, 'NODE_CLASS_MAPPINGS'):
            NODE_CLASS_MAPPINGS.update(getattr(module, 'NODE_CLASS_MAPPINGS'))
        if hasattr(module, 'NODE_DISPLAY_NAME_MAPPINGS'):
            NODE_DISPLAY_NAME_MAPPINGS.update(getattr(module, 'NODE_DISPLAY_NAME_MAPPINGS')) 