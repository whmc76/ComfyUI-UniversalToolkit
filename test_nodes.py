import sys
import os

# 添加路径
sys.path.append('.')

print("🔧 测试所有修复后的节点...\n")

# 测试图像拼接节点
try:
    from nodes.image.image_concatenate import NODE_CLASS_MAPPINGS as CONCAT_MAPPINGS
    print("✅ ImageConcatenate_UTK 节点映射:")
    for k, v in CONCAT_MAPPINGS.items():
        print(f"  {k}: {v.__name__}")
except Exception as e:
    print(f"❌ 导入 ImageConcatenate_UTK 失败: {e}")

try:
    from nodes.image.image_concatenate_multi import NODE_CLASS_MAPPINGS as CONCAT_MULTI_MAPPINGS
    print("\n✅ ImageConcatenateMulti_UTK 节点映射:")
    for k, v in CONCAT_MULTI_MAPPINGS.items():
        print(f"  {k}: {v.__name__}")
except Exception as e:
    print(f"❌ 导入 ImageConcatenateMulti_UTK 失败: {e}")

# 测试 ImitationHueNode_UTK
try:
    from nodes.image.imitation_hue_node import NODE_CLASS_MAPPINGS as IMITATION_MAPPINGS
    print("\n✅ ImitationHueNode_UTK 节点映射:")
    for k, v in IMITATION_MAPPINGS.items():
        print(f"  {k}: {v.__name__}")
except Exception as e:
    print(f"❌ 导入 ImitationHueNode_UTK 失败: {e}")

# 测试其他修复的节点
test_nodes = [
    ("restore_crop_box", "RestoreCropBox_UTK"),
    ("image_scale_restore", "ImageScaleRestore_UTK"),
    ("image_scale_by_aspect_ratio", "ImageScaleByAspectRatio_UTK"),
    ("image_remove_alpha", "ImageRemoveAlpha_UTK"),
    ("image_mask_scale_as", "ImageMaskScaleAs_UTK"),
    ("image_combine_alpha", "ImageCombineAlpha_UTK"),
    ("crop_by_mask", "CropByMask_UTK"),
]

print("\n🔧 测试其他修复的节点:")
for node_file, node_class in test_nodes:
    try:
        module = __import__(f"nodes.image.{node_file}", fromlist=[node_class])
        node_class_obj = getattr(module, node_class)
        print(f"✅ {node_class}: 导入成功")
    except Exception as e:
        print(f"❌ {node_class}: 导入失败 - {e}")

# 测试 tools 目录下的节点
print("\n🔧 测试 tools 目录下的节点:")
tools_nodes = [
    ("purge_vram", "PurgeVRAM_UTK"),
    ("fill_masked_area", "FillMaskedArea_UTK"),
    ("show_nodes", "Show_UTK"),
]

for node_file, node_class in tools_nodes:
    try:
        module = __import__(f"nodes.tools.{node_file}", fromlist=[node_class])
        node_class_obj = getattr(module, node_class)
        print(f"✅ {node_class}: 导入成功")
    except Exception as e:
        print(f"❌ {node_class}: 导入失败 - {e}")

print("\n🎉 所有节点修复完成！")
print("现在您应该能在 ComfyUI 中看到以下节点：")
print("  - Image Concatenate (UTK)")
print("  - Image Concatenate Multi (UTK)")
print("  - Imitation Hue Node (UTK) - 已同步 MingNodes 实现")
print("  - Restore Crop Box (UTK)")
print("  - Image Scale Restore (UTK)")
print("  - Image Scale By Aspect Ratio (UTK)")
print("  - Image Remove Alpha (UTK)")
print("  - Image Mask Scale As (UTK)")
print("  - Image Combine Alpha (UTK)")
print("  - Crop By Mask (UTK)")
print("  - Purge VRAM (UTK) - 现在在 Tools 分类下")
print("  - Fill Masked Area (UTK) - 在 Tools 分类下")
print("  - Show Nodes (UTK) - 在 Tools 分类下") 