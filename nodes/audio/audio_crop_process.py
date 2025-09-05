"""
Audio Crop Process Node
~~~~~~~~~~~~~~~~~~~~~~

Processes audio with cropping, resampling, and gain adjustments.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import torch

FLOAT_MAX = 99999999999999999.0


class AudioCropProcessUTK:
    CATEGORY = "UniversalToolkit/Audio"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
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

    @classmethod
    def IS_CHANGED(cls, *args):
        return args

    def execute(
        self,
        audio,
        gain_db: float,
        offset_seconds: float,
        duration_seconds: float,
        resample_to_hz: float,
        make_stereo: bool,
    ):
        waveform = audio["waveform"]  # [B, C, N]
        sample_rate = int(audio["sample_rate"])
        # 裁剪offset和duration
        if duration_seconds > 0:
            # 只有当duration大于0时才进行裁剪
            start = int(offset_seconds * sample_rate)
            end = int(start + duration_seconds * sample_rate)
            waveform = waveform[:, :, start:end]
        elif offset_seconds > 0:
            # 如果duration为0但offset大于0，只应用offset裁剪
            start = int(offset_seconds * sample_rate)
            waveform = waveform[:, :, start:]
        # 如果duration和offset都为0，则不进行任何裁剪
        # 重采样
        if resample_to_hz > 0 and int(resample_to_hz) != sample_rate:
            import torchaudio

            waveform = torchaudio.functional.resample(
                waveform, sample_rate, int(resample_to_hz)
            )
            sample_rate = int(resample_to_hz)
        # 增益
        if gain_db != 0.0:
            gain_scalar = 10 ** (gain_db / 20)
            waveform = waveform * gain_scalar
        # 强制立体声
        if make_stereo and waveform.shape[1] == 1:
            waveform = torch.cat([waveform, waveform], dim=1)
        elif make_stereo and waveform.shape[1] != 2:
            raise ValueError(
                f"Input audio has {waveform.shape[1]} channels, cannot convert to stereo (2 channels)"
            )
        channels = int(waveform.shape[1])
        duration_val = (
            float(waveform.shape[2] / sample_rate) if sample_rate > 0 else 0.0
        )
        return (
            {"sample_rate": sample_rate, "waveform": waveform},
            sample_rate,
            channels,
            duration_val,
        )


# Node mappings
NODE_CLASS_MAPPINGS = {
    "AudioCropProcessUTK": AudioCropProcessUTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AudioCropProcessUTK": "Audio Crop Process (UTK)",
}
