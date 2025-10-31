class BestContextWindow_UTK:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "total_frames": ("INT", {"default": 1, "min": 0}),
                "min_window_frames": ("INT", {"default": 61, "min": 1}),
                "max_window_frames": ("INT", {"default": 81, "min": 1}),
            }
        }

    RETURN_TYPES = (
        "INT",  # best_window
        "INT",  # padding (冗余帧数)
        "INT",  # padded_total 实际处理帧数
        "INT",  # segments 段数k
    )
    RETURN_NAMES = (
        "best_window",
        "padding",
        "padded_total",
        "segments",
    )
    FUNCTION = "compute"
    CATEGORY = "UniversalToolkit/Tools"

    @staticmethod
    def _best_window(total_frames: int, min_window: int, max_window: int) -> tuple[int, int, int, int]:
        # sanitize inputs
        if max_window is None or max_window < 1:
            max_window = 1
        if total_frames is None or total_frames < 0:
            total_frames = 0
        if min_window is None or min_window < 1:
            min_window = 1
        if max_window < min_window:
            max_window = min_window

        # generate candidates that satisfy 4n+1 and within [min_window, max_window]
        candidates = []
        # align start to first (4n+1) >= min_window
        start = min_window if min_window % 4 == 1 else (min_window + (4 - ((min_window - 1) % 4) - 1))
        for w in range(start, max_window + 1):
            if w % 4 == 1:
                candidates.append(w)

        if not candidates:
            # Fallback: choose closest valid 4n+1 not exceeding max_window
            # compute nearest below max_window
            w = max_window - ((max_window - 1) % 4)
            if w < 1:
                w = 1
            candidates = [w]

        # choose window minimizing padding to next multiple; tie -> larger window
        def metrics(w: int):
            k = (total_frames + w - 1) // w  # ceil(total_frames / w)
            padding = k * w - total_frames
            padded_total = k * w
            return padding, padded_total, k

        best_w = candidates[0]
        best_pad, best_padded_total, best_k = metrics(best_w)
        for w in candidates[1:]:
            pad, padded_total, k = metrics(w)
            if pad < best_pad or (pad == best_pad and w > best_w):
                best_w, best_pad, best_padded_total, best_k = w, pad, padded_total, k

        return best_w, best_pad, best_padded_total, best_k

    def compute(self, total_frames: int, min_window_frames: int, max_window_frames: int):
        best_w, padding, padded_total, k = self._best_window(int(total_frames), int(min_window_frames), int(max_window_frames))
        return (best_w, padding, padded_total, k)


NODE_CLASS_MAPPINGS = {
    "BestContextWindow_UTK": BestContextWindow_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BestContextWindow_UTK": "Best Context Window (UTK)",
}


