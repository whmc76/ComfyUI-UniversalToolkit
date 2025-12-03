"""
Load Video Frames Node for ComfyUI Universal Toolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Load frames from video files or image sequences and intelligently sample frames
based on target frame count and sampling mode.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import os
import cv2
import torch
from typing import Optional, Tuple, List
from PIL import Image

from ..image.image_converters import pil2tensor


class Extract_Video_Frames_UTK:
    """
    从视频文件或图片序列中智能抽取帧
    
    支持多种抽取模式：
    - 平均抽取：均匀分布在整个视频/序列中
    - 前面较多：前半部分抽取更多帧
    - 后面较多：后半部分抽取更多帧
    - 中间较多：中间部分抽取更多帧
    - 两端较多：开头和结尾抽取更多帧
    """
    
    CATEGORY = "UniversalToolkit/Tools"
    RETURN_TYPES = ("IMAGE", "INT")
    RETURN_NAMES = ("images", "frames_count")
    FUNCTION = "load_frames"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {
                    "default": "",
                    "tooltip": "视频文件路径（支持mp4, avi, mov等格式）"
                }),
                "target_frames": ("INT", {
                    "default": 8,
                    "min": 1,
                    "max": 1000,
                    "step": 1,
                    "tooltip": "目标抽取的帧数"
                }),
                "mode": (["average", "front_heavy", "back_heavy", "middle_heavy", "ends_heavy"], {
                    "default": "average",
                    "tooltip": "Frame extraction mode"
                }),
            },
            "optional": {
                "images": ("IMAGE", {
                    "tooltip": "图片序列输入（如果提供，将优先使用图片序列而不是视频）"
                }),
            }
        }
    
    def calculate_frame_indices(self, total_frames: int, target_frames: int, mode: str) -> List[int]:
        """
        根据模式和目标帧数计算要抽取的帧索引
        
        Args:
            total_frames: 总帧数
            target_frames: 目标抽取帧数
            mode: 抽取模式
            
        Returns:
            帧索引列表
        """
        if total_frames <= 0:
            return []
        
        if target_frames >= total_frames:
            # 如果目标帧数大于等于总帧数，返回所有帧
            return list(range(total_frames))
        
        indices = []
        
        if mode == "average":
            # 均匀分布
            step = total_frames / target_frames
            indices = [int(i * step) for i in range(target_frames)]
            # 确保最后一个索引不超过总帧数
            indices[-1] = min(indices[-1], total_frames - 1)
            
        elif mode == "front_heavy":
            # 前半部分抽取60%，后半部分抽取40%
            front_count = int(target_frames * 0.6)
            back_count = target_frames - front_count
            
            # 前半部分均匀抽取
            if front_count > 0:
                front_step = (total_frames // 2) / front_count
                front_indices = [int(i * front_step) for i in range(front_count)]
            else:
                front_indices = []
            
            # 后半部分均匀抽取
            if back_count > 0:
                back_start = total_frames // 2
                back_step = (total_frames - back_start) / back_count
                back_indices = [back_start + int(i * back_step) for i in range(back_count)]
            else:
                back_indices = []
            
            indices = front_indices + back_indices
            
        elif mode == "back_heavy":
            # 前半部分抽取40%，后半部分抽取60%
            front_count = int(target_frames * 0.4)
            back_count = target_frames - front_count
            
            # 前半部分均匀抽取
            if front_count > 0:
                front_step = (total_frames // 2) / front_count
                front_indices = [int(i * front_step) for i in range(front_count)]
            else:
                front_indices = []
            
            # 后半部分均匀抽取
            if back_count > 0:
                back_start = total_frames // 2
                back_step = (total_frames - back_start) / back_count
                back_indices = [back_start + int(i * back_step) for i in range(back_count)]
            else:
                back_indices = []
            
            indices = front_indices + back_indices
            
        elif mode == "middle_heavy":
            # 开头20%，中间60%，结尾20%
            start_count = int(target_frames * 0.2)
            middle_count = int(target_frames * 0.6)
            end_count = target_frames - start_count - middle_count
            
            # 开头部分
            if start_count > 0:
                start_step = (total_frames // 4) / max(start_count, 1)
                start_indices = [int(i * start_step) for i in range(start_count)]
            else:
                start_indices = []
            
            # 中间部分
            if middle_count > 0:
                middle_start = total_frames // 4
                middle_end = total_frames * 3 // 4
                middle_step = (middle_end - middle_start) / max(middle_count, 1)
                middle_indices = [middle_start + int(i * middle_step) for i in range(middle_count)]
            else:
                middle_indices = []
            
            # 结尾部分
            if end_count > 0:
                end_start = total_frames * 3 // 4
                end_step = (total_frames - end_start) / max(end_count, 1)
                end_indices = [end_start + int(i * end_step) for i in range(end_count)]
            else:
                end_indices = []
            
            indices = start_indices + middle_indices + end_indices
            
        elif mode == "ends_heavy":
            # 开头40%，中间20%，结尾40%
            start_count = int(target_frames * 0.4)
            middle_count = int(target_frames * 0.2)
            end_count = target_frames - start_count - middle_count
            
            # 开头部分
            if start_count > 0:
                start_step = (total_frames // 3) / max(start_count, 1)
                start_indices = [int(i * start_step) for i in range(start_count)]
            else:
                start_indices = []
            
            # 中间部分
            if middle_count > 0:
                middle_start = total_frames // 3
                middle_end = total_frames * 2 // 3
                middle_step = (middle_end - middle_start) / max(middle_count, 1)
                middle_indices = [middle_start + int(i * middle_step) for i in range(middle_count)]
            else:
                middle_indices = []
            
            # 结尾部分
            if end_count > 0:
                end_start = total_frames * 2 // 3
                end_step = (total_frames - end_start) / max(end_count, 1)
                end_indices = [end_start + int(i * end_step) for i in range(end_count)]
            else:
                end_indices = []
            
            indices = start_indices + middle_indices + end_indices
        
        # 去重并排序
        indices = sorted(list(set(indices)))
        # 确保索引在有效范围内
        indices = [idx for idx in indices if 0 <= idx < total_frames]
        
        # 如果去重后数量不足，补充帧
        while len(indices) < target_frames and len(indices) < total_frames:
            # 找到最大的间隔并补充
            if len(indices) == 0:
                indices.append(0)
            elif len(indices) == 1:
                if indices[0] < total_frames - 1:
                    indices.append(total_frames - 1)
                else:
                    break
            else:
                max_gap = 0
                insert_pos = 0
                for i in range(len(indices) - 1):
                    gap = indices[i + 1] - indices[i]
                    if gap > max_gap:
                        max_gap = gap
                        insert_pos = i + 1
                        insert_value = (indices[i] + indices[i + 1]) // 2
                
                if max_gap > 1:
                    indices.insert(insert_pos, insert_value)
                    indices.sort()
                else:
                    # 如果没有大间隔，在两端补充
                    if indices[0] > 0:
                        indices.insert(0, indices[0] - 1)
                    elif indices[-1] < total_frames - 1:
                        indices.append(min(indices[-1] + 1, total_frames - 1))
                    else:
                        break
        
        return indices[:target_frames]
    
    def load_video_frames(self, video_path: str, indices: List[int]) -> List[torch.Tensor]:
        """
        从视频文件中加载指定索引的帧
        
        Args:
            video_path: 视频文件路径
            indices: 要加载的帧索引列表
            
        Returns:
            帧张量列表
        """
        # 路径预处理
        video_path = video_path.strip().strip('"').strip("'")
        video_path = video_path.replace("\\", "/")
        
        if not os.path.isfile(video_path):
            raise FileNotFoundError(f"视频文件不存在: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"无法打开视频文件: {video_path}")
        
        # 为了保持原始顺序，先按索引顺序读取并存储到字典中
        frame_dict = {}
        sorted_indices = sorted(set(indices))  # 去重并排序以提高效率
        
        for target_idx in sorted_indices:
            # 跳转到目标帧
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_idx)
            
            ret, frame = cap.read()
            if not ret:
                print(f"警告: 无法读取第 {target_idx} 帧")
                continue
            
            # 转换BGR到RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 转换为PIL图像
            pil_image = Image.fromarray(frame_rgb)
            # 转换为tensor
            tensor = pil2tensor(pil_image)
            frame_dict[target_idx] = tensor
        
        cap.release()
        
        if len(frame_dict) == 0:
            raise RuntimeError("未能从视频中加载任何帧")
        
        # 按照原始indices顺序返回帧
        frames = [frame_dict[idx] for idx in indices if idx in frame_dict]
        
        return frames
    
    def load_image_sequence_frames(self, images: torch.Tensor, indices: List[int]) -> List[torch.Tensor]:
        """
        从图片序列中提取指定索引的帧
        
        Args:
            images: 图片批次张量 [batch, height, width, channels]
            indices: 要提取的帧索引列表
            
        Returns:
            帧张量列表
        """
        frames = []
        for idx in indices:
            if 0 <= idx < len(images):
                frames.append(images[idx])
            else:
                print(f"警告: 索引 {idx} 超出图片序列范围 [0, {len(images)-1}]")
        
        return frames
    
    def load_frames(
        self,
        video_path: str,
        target_frames: int,
        mode: str,
        images: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor]:
        """
        加载并抽取帧
        
        Args:
            video_path: 视频文件路径
            target_frames: 目标帧数
            mode: 抽取模式
            images: 可选的图片序列输入
            
        Returns:
            抽取的帧批次张量
        """
        # 优先使用图片序列输入
        if images is not None:
            total_frames = len(images)
            print(f"📸 从图片序列中抽取帧: 总帧数={total_frames}, 目标帧数={target_frames}, 模式={mode}")
            
            indices = self.calculate_frame_indices(total_frames, target_frames, mode)
            print(f"📊 计算得到的帧索引: {indices}")
            
            # 按照indices的顺序提取帧（保持计算出的顺序）
            frame_tensors = self.load_image_sequence_frames(images, indices)
            
        elif video_path and video_path.strip():
            # 使用视频文件
            video_path = video_path.strip().strip('"').strip("'")
            
            # 先获取视频总帧数
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise RuntimeError(f"无法打开视频文件: {video_path}")
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()
            
            print(f"🎬 从视频中抽取帧: 文件={video_path}, 总帧数={total_frames}, FPS={fps:.2f}, 目标帧数={target_frames}, 模式={mode}")
            
            indices = self.calculate_frame_indices(total_frames, target_frames, mode)
            print(f"📊 计算得到的帧索引: {indices}")
            
            frame_tensors = self.load_video_frames(video_path, indices)
            
        else:
            raise ValueError("必须提供视频路径或图片序列输入")
        
        if len(frame_tensors) == 0:
            raise RuntimeError("未能加载任何帧")
        
        # 将所有帧堆叠成批次
        batch_tensor = torch.stack(frame_tensors, dim=0)
        frames_count = len(frame_tensors)
        
        print(f"✅ 成功加载 {frames_count} 帧，输出形状: {batch_tensor.shape}")
        
        return (batch_tensor, frames_count)


# 节点映射
NODE_CLASS_MAPPINGS = {
    "Extract_Video_Frames_UTK": Extract_Video_Frames_UTK
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Extract_Video_Frames_UTK": "Extract Video Frames (UTK)"
}

