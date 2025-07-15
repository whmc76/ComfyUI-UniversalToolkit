"""
Load Audio Node
~~~~~~~~~~~~~~

Loads audio files from path with various processing options.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import math
import os
from pathlib import Path

import librosa
import soundfile as sf
import torch

FLOAT_MAX = 99999999999999999.0


class LoadAudioPlusFromPath_UTK:
    CATEGORY = "UniversalToolkit/Audio"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": "./audio.mp3"}),
                "gain_db": ("FLOAT", {"default": 0, "min": -100, "max": 100}),
                "offset_seconds": ("FLOAT", {"default": 0, "min": 0, "max": FLOAT_MAX}),
                "duration_seconds": (
                    "FLOAT",
                    {"default": 0, "min": 0, "max": FLOAT_MAX},
                ),
                "resample_to_hz": ("FLOAT", {"default": 0, "min": 0, "max": FLOAT_MAX}),
                "make_stereo": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("AUDIO", "INT", "INT", "FLOAT")
    RETURN_NAMES = ("audio", "sample_rate", "channels", "duration")
    FUNCTION = "execute"

    def db_to_scalar(self, db: float):
        return 10 ** (db / 20)

    @classmethod
    def IS_CHANGED(cls, path: str, *args):
        if os.path.exists(path):
            mtime = os.path.getmtime(path)
        else:
            mtime = None
        return (mtime, path, *args)

    def execute(
        self,
        path: str,
        gain_db: float,
        offset_seconds: float,
        duration_seconds: float,
        resample_to_hz: float,
        make_stereo: bool,
    ):
        # 路径预处理：去除首尾单双引号，替换分隔符，兼容Windows绝对路径
        path = path.strip().strip('"').strip("'")
        path = path.replace("\\", "/").replace("\\", "/")
        if os.name == "nt" and len(path) > 2 and path[1] == ":":
            path = path.replace("\\", "/")
        # 文件存在性检查，异常时详细提示
        if not os.path.isfile(path):
            raise FileNotFoundError(
                f"音频文件不存在或路径错误: {path}\n请检查路径是否正确，注意不要包含多余的引号或空格，Windows下建议使用/或\\分隔符。"
            )
        # 加载音频，异常时详细提示
        try:
            sr = int(resample_to_hz) if resample_to_hz > 0 else None
            duration = duration_seconds if duration_seconds > 0 else None
            mix, sr = librosa.load(
                path, sr=sr, mono=False, offset=offset_seconds, duration=duration
            )
        except Exception as e:
            raise RuntimeError(
                f"音频加载失败: {e}\n请确认文件格式是否受支持，路径是否包含特殊字符。"
            )
        # shape调整
        if len(mix.shape) == 1:
            mix = torch.stack([mix], dim=0)
        if make_stereo:
            if mix.shape[0] == 1:
                mix = torch.cat([mix, mix], dim=0)
            elif mix.shape[0] == 2:
                pass
            else:
                raise ValueError(
                    f"Input audio has {mix.shape[0]} channels, cannot convert to stereo (2 channels)"
                )
        mix = torch.from_numpy(mix)  # 保证为Tensor
        mix = torch.unsqueeze(mix, 0)  # shape: [1, 2, N] 或 [1, 1, N]
        if gain_db != 0.0:
            gain_scalar = 10 ** (gain_db / 20)
            mix = gain_scalar * mix
        sample_rate = int(sr)
        channels = int(mix.shape[1])
        duration_val = float(mix.shape[2] / sample_rate) if sample_rate > 0 else 0.0
        return (
            {"sample_rate": sample_rate, "waveform": mix},
            sample_rate,
            channels,
            duration_val,
        )


# Node mappings
NODE_CLASS_MAPPINGS = {
    "LoadAudioPlusFromPath_UTK": LoadAudioPlusFromPath_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadAudioPlusFromPath_UTK": "Load Audio Plus From Path (UTK)",
}
