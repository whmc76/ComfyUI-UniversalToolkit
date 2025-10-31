import torch
from typing import Tuple, Optional


class GetImageRangeFromBatch_UTK:
    """
    从批次中获取指定范围的图像或遮罩
    支持从图像批次或遮罩批次中提取指定索引范围的元素
    """
    
    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "get_range_from_batch"
    CATEGORY = "UniversalToolkit/Tools"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "start_index": ("INT", {
                    "default": 0,
                    "min": -1,
                    "max": 4096,
                    "step": 1,
                    "tooltip": "起始索引，-1表示从末尾开始"
                }),
                "num_frames": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "tooltip": "要提取的帧数"
                }),
            },
            "optional": {
                "images": ("IMAGE", {
                    "tooltip": "输入的图像批次"
                }),
                "masks": ("MASK", {
                    "tooltip": "输入的遮罩批次"
                }),
            }
        }
    
    def get_range_from_batch(self, start_index: int, num_frames: int, 
                           images: Optional[torch.Tensor] = None, 
                           masks: Optional[torch.Tensor] = None) -> Tuple[Optional[torch.Tensor], Optional[torch.Tensor]]:
        """
        从批次中获取指定范围的图像或遮罩
        
        Args:
            start_index: 起始索引，-1表示从末尾开始
            num_frames: 要提取的帧数
            images: 输入的图像批次 (可选)
            masks: 输入的遮罩批次 (可选)
            
        Returns:
            Tuple[Optional[torch.Tensor], Optional[torch.Tensor]]: 提取的图像和遮罩
        """
        chosen_images = None
        chosen_masks = None
        
        # 处理图像批次
        if images is not None:
            if start_index == -1:
                # 从末尾开始计算起始索引
                start_index = max(0, len(images) - num_frames)
            
            if start_index < 0 or start_index >= len(images):
                raise ValueError(f"图像起始索引 {start_index} 超出范围 [0, {len(images)-1}]")
            
            end_index = min(start_index + num_frames, len(images))
            chosen_images = images[start_index:end_index]
            
            print(f"📸 从图像批次中提取: 索引 {start_index} 到 {end_index-1}，共 {len(chosen_images)} 张图像")
        
        # 处理遮罩批次
        if masks is not None:
            if start_index == -1:
                # 从末尾开始计算起始索引
                start_index = max(0, len(masks) - num_frames)
            
            if start_index < 0 or start_index >= len(masks):
                raise ValueError(f"遮罩起始索引 {start_index} 超出范围 [0, {len(masks)-1}]")
            
            end_index = min(start_index + num_frames, len(masks))
            chosen_masks = masks[start_index:end_index]
            
            print(f"🎭 从遮罩批次中提取: 索引 {start_index} 到 {end_index-1}，共 {len(chosen_masks)} 个遮罩")
        
        # 检查是否至少有一个输入
        if images is None and masks is None:
            raise ValueError("至少需要提供图像或遮罩输入")
        
        return (chosen_images, chosen_masks)


# 节点映射
NODE_CLASS_MAPPINGS = {
    "GetImageRangeFromBatch_UTK": GetImageRangeFromBatch_UTK
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GetImageRangeFromBatch_UTK": "Get Image or Mask Range From Batch (UTK)"
}
