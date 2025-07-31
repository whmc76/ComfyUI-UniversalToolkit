#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
视频提示词生成器 ComfyUI 自定义节点 (双语版本)
Video Prompt Generator ComfyUI Custom Node (Bilingual Version)

原作者 / Original Author: flybirdxx
项目地址 / Project URL: https://github.com/flybirdxx/ComfyUI_Prompt_Helper
许可证 / License: MIT License

基于 Denge AI 的视频提示词生成工具创建
支持中文和英文两种语言
"""

import json
import os
import locale

# 获取当前文件所在的目录路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 检测系统语言
def detect_system_language():
    """检测系统语言并返回支持的语言代码"""
    try:
        # 获取系统语言设置
        system_locale = locale.getdefaultlocale()[0]
        if system_locale:
            # 如果是中文相关的locale，返回zh
            if system_locale.startswith('zh'):
                return 'zh'
            # 其他情况返回英文
            else:
                return 'en'
    except Exception as e:
        pass
    
    # 默认返回中文
    return 'zh'

# 获取系统默认语言
DEFAULT_LANGUAGE = detect_system_language()

# 构建 JSON 文件的完整路径
PRESETS_FILE_PATH = os.path.join(CURRENT_DIR, 'prompt_presets.json')
UI_LABELS_FILE_PATH = os.path.join(CURRENT_DIR, 'prompt_ui_labels.json')

# 从 JSON 文件加载预设数据
def load_video_presets():
    try:
        with open(PRESETS_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading prompt_presets.json: {e}")
        return {}

# 从 JSON 文件加载UI标签
def load_ui_labels():
    try:
        with open(UI_LABELS_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading prompt_ui_labels.json: {e}")
        # 返回基本的英文标签作为回退
        return {
            "zh": {"language": "语言", "default_prompt": "一个美丽的场景"},
            "en": {"language": "Language", "default_prompt": "A beautiful scene"},
            "messages": {"zh": {}, "en": {}},
            "display_names": {"zh": "视频提示词生成器", "en": "Video Prompt Generator"}
        }

# 加载预设数据和UI标签
VIDEO_PRESETS = load_video_presets()
UI_LABELS_DATA = load_ui_labels()
UI_LABELS = UI_LABELS_DATA  # 保持向后兼容

class WanVideoPromptGenerator:
    """
    视频提示词生成器节点（双语版本）
    Video Prompt Generator Node (Bilingual Version)
    
    允许用户从14个不同的电影分类中选择选项来构建专业的电影化提示词
    Allows users to build professional cinematic prompts by selecting from 14 different film categories

    原作者 / Original Author: flybirdxx
    项目地址 / Project URL: https://github.com/flybirdxx/ComfyUI_Prompt_Helper
    许可证 / License: MIT License
    """
    
    @classmethod
    def INPUT_TYPES(s):
        """定义输入类型"""
        
        # 为每个分类创建选项列表，添加 "none" 选项在前面
        def get_options(category, language=DEFAULT_LANGUAGE):
            if language in VIDEO_PRESETS and category in VIDEO_PRESETS[language]:
                # 获取本地化的显示文本，而不是键名
                category_data = VIDEO_PRESETS[language][category]
                options = []
                
                # 先添加 "none" 选项，显示为本地化的文本
                if "none" in category_data:
                    none_text = UI_LABELS_DATA[language].get("none_option", "none")
                    options.append(none_text)
                
                # 添加其他选项的本地化文本
                for key, value in category_data.items():
                    if key != "none" and value:  # 跳过none和空值
                        options.append(value)
                
                return options
            none_text = UI_LABELS_DATA[language].get("none_option", "none")
            return [none_text]
        
        # 根据默认语言设置默认提示词和属性名称
        default_prompt = UI_LABELS[DEFAULT_LANGUAGE]["default_prompt"]
        labels = UI_LABELS[DEFAULT_LANGUAGE]
        
        # 本地化的属性名称映射
        return {
            "required": {
                labels["language"]: (["zh", "en"], {"default": DEFAULT_LANGUAGE}),
                labels["user_prompt"]: ("STRING", {
                    "multiline": True,
                    "default": default_prompt
                }),
                labels["shot_size"]: (get_options("shot_size"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["lighting_type"]: (get_options("lighting_type"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["light_source"]: (get_options("light_source"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["color_tone"]: (get_options("color_tone"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["camera_angle"]: (get_options("camera_angle"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["lens"]: (get_options("lens"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["camera_movement_basic"]: (get_options("camera_movement_basic"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["camera_movement_advanced"]: (get_options("camera_movement_advanced"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["time_of_day"]: (get_options("time_of_day"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["motion"]: (get_options("motion"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["visual_effects"]: (get_options("visual_effects"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["stylization_visual_style"]: (get_options("stylization_visual_style"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["character_emotion"]: (get_options("character_emotion"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["composition"]: (get_options("composition"), {"default": UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["prompt_format"]: ([
                    labels["format_professional"], 
                    labels["format_simple"], 
                    labels["format_detailed"]
                ], {"default": labels["format_professional"]})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("generated_prompt",)
    FUNCTION = "generate_video_prompt"
    CATEGORY = "UniversalToolkit/Tools"
    
    def generate_video_prompt(self, **kwargs):
        """生成视频提示词"""
        
        # 创建参数映射以支持本地化的参数名称
        # 将本地化的参数名映射回英文键名
        param_mapping = {}
        for lang_code in ["zh", "en"]:
            labels = UI_LABELS[lang_code]
            for en_key, localized_name in labels.items():
                if en_key in ["language", "user_prompt", "shot_size", "lighting_type", "light_source", 
                             "color_tone", "camera_angle", "lens", "camera_movement_basic", 
                             "camera_movement_advanced", "time_of_day", "motion", "visual_effects",
                             "stylization_visual_style", "character_emotion", "composition", "prompt_format"]:
                    param_mapping[localized_name] = en_key
        
        # 创建选项值的反向映射（本地化文本 -> 键名）
        def create_value_to_key_mapping(language):
            value_to_key = {}
            if language in VIDEO_PRESETS:
                for category, items in VIDEO_PRESETS[language].items():
                    for key, value in items.items():
                        if value:  # 只映射非空值
                            value_to_key[value] = key
                # 处理"无"选项
                none_text = UI_LABELS_DATA[language].get("none_option", "none")
                value_to_key[none_text] = "none"
                
                # 处理prompt_format选项的映射
                labels = UI_LABELS[language]
                value_to_key[labels["format_professional"]] = "professional"
                value_to_key[labels["format_simple"]] = "simple"
                value_to_key[labels["format_detailed"]] = "detailed"
            return value_to_key
        
        # 将本地化参数名和值映射为英文参数名和键名
        params = {}
        for key, value in kwargs.items():
            mapped_key = param_mapping.get(key, key)
            params[mapped_key] = value
        
        # 提取参数
        language = params.get("language", DEFAULT_LANGUAGE)
        
        # 创建当前语言的值到键的映射
        value_to_key = create_value_to_key_mapping(language)
        
        # 提取并转换参数值
        user_prompt = params.get("user_prompt", UI_LABELS[language]["default_prompt"])
        
        # 对于选项类型的参数，需要将本地化文本转换回键名
        def convert_value_to_key(value, default="none"):
            if not value:
                return default
            return value_to_key.get(value, value)
        
        shot_size = convert_value_to_key(params.get("shot_size"))
        lighting_type = convert_value_to_key(params.get("lighting_type"))
        light_source = convert_value_to_key(params.get("light_source"))
        color_tone = convert_value_to_key(params.get("color_tone"))
        camera_angle = convert_value_to_key(params.get("camera_angle"))
        lens = convert_value_to_key(params.get("lens"))
        camera_movement_basic = convert_value_to_key(params.get("camera_movement_basic"))
        camera_movement_advanced = convert_value_to_key(params.get("camera_movement_advanced"))
        time_of_day = convert_value_to_key(params.get("time_of_day"))
        motion = convert_value_to_key(params.get("motion"))
        visual_effects = convert_value_to_key(params.get("visual_effects"))
        stylization_visual_style = convert_value_to_key(params.get("stylization_visual_style"))
        character_emotion = convert_value_to_key(params.get("character_emotion"))
        composition = convert_value_to_key(params.get("composition"))
        prompt_format = convert_value_to_key(params.get("prompt_format"), "professional")
        
        # 验证语言参数
        if language not in VIDEO_PRESETS:
            messages = UI_LABELS_DATA.get("messages", {}).get(DEFAULT_LANGUAGE, {})
            unsupported_msg = messages.get("unsupported_language", "Unsupported language")
            fallback_msg = messages.get("fallback_to_default", ", fallback to default language")
            print(f"[VideoPromptGenerator] {unsupported_msg}: {language}{fallback_msg}: {DEFAULT_LANGUAGE}")
            language = DEFAULT_LANGUAGE
        
        # 获取当前语言的预设数据
        current_presets = VIDEO_PRESETS[language]
        current_labels = UI_LABELS[language]
        
        # 收集所有选择的元素
        selected_elements = []
        
        # 定义参数映射
        category_params = {
            "shot_size": shot_size,
            "lighting_type": lighting_type,
            "light_source": light_source,
            "color_tone": color_tone,
            "camera_angle": camera_angle,
            "lens": lens,
            "camera_movement_basic": camera_movement_basic,
            "camera_movement_advanced": camera_movement_advanced,
            "time_of_day": time_of_day,
            "motion": motion,
            "visual_effects": visual_effects,
            "stylization_visual_style": stylization_visual_style,
            "character_emotion": character_emotion,
            "composition": composition
        }
        
        # 提取选中的非空元素
        for category, value in category_params.items():
            if value != "none" and category in current_presets and value in current_presets[category]:
                element_text = current_presets[category][value]
                if element_text:  # 确保元素文本不为空
                    selected_elements.append(element_text)
        
        # 根据格式生成提示词
        if prompt_format == "professional":
            if selected_elements:
                cinematic_elements = "，".join(selected_elements) if language == "zh" else ", ".join(selected_elements)
                separator = "，" if language == "zh" else ", "
                generated_prompt = f"{user_prompt}{separator}{cinematic_elements}{current_labels['professional_suffix']}"
            else:
                generated_prompt = f"{user_prompt}{current_labels['professional_suffix']}"
                
        elif prompt_format == "detailed":
            if selected_elements:
                # 按类别组织元素
                shot_elements = []
                lighting_elements = []
                camera_elements = []
                style_elements = []
                
                # 分类整理元素
                shot_categories = ["shot_size", "camera_angle", "composition"]
                lighting_categories = ["lighting_type", "light_source", "color_tone", "time_of_day"]
                camera_categories = ["lens", "camera_movement_basic", "camera_movement_advanced", "motion"]
                style_categories = ["visual_effects", "stylization_visual_style", "character_emotion"]
                
                for category, value in category_params.items():
                    if value != "none" and category in current_presets and value in current_presets[category]:
                        element_text = current_presets[category][value]
                        if element_text:
                            if category in shot_categories:
                                shot_elements.append(element_text)
                            elif category in lighting_categories:
                                lighting_elements.append(element_text)
                            elif category in camera_categories:
                                camera_elements.append(element_text)
                            elif category in style_categories:
                                style_elements.append(element_text)
                
                # 构建详细提示词
                prompt_parts = [user_prompt]
                separator = "，" if language == "zh" else ", "
                
                if language == "zh":
                    if shot_elements:
                        prompt_parts.append(f"镜头构图：{separator.join(shot_elements)}")
                    if lighting_elements:
                        prompt_parts.append(f"灯光：{separator.join(lighting_elements)}")
                    if camera_elements:
                        prompt_parts.append(f"摄像机工作：{separator.join(camera_elements)}")
                    if style_elements:
                        prompt_parts.append(f"视觉风格：{separator.join(style_elements)}")
                else:
                    if shot_elements:
                        prompt_parts.append(f"Shot composition: {separator.join(shot_elements)}")
                    if lighting_elements:
                        prompt_parts.append(f"Lighting: {separator.join(lighting_elements)}")
                    if camera_elements:
                        prompt_parts.append(f"Camera work: {separator.join(camera_elements)}")
                    if style_elements:
                        prompt_parts.append(f"Visual style: {separator.join(style_elements)}")
                
                prompt_parts.append(current_labels['detailed_suffix'].lstrip(". "))
                connector = "。" if language == "zh" else ". "
                generated_prompt = connector.join(prompt_parts)
            else:
                connector = "。" if language == "zh" else ". "
                generated_prompt = f"{user_prompt}{connector}{current_labels['detailed_suffix'].lstrip('. ')}"
                
        else:  # simple format
            if selected_elements:
                # 选择最重要的几个元素
                key_elements = selected_elements[:3]  # 只取前3个元素
                separator = "，" if language == "zh" else ", "
                generated_prompt = f"{user_prompt}{separator}{separator.join(key_elements)}"
            else:
                generated_prompt = user_prompt
        
        # 本地化的输出信息
        messages = UI_LABELS_DATA.get("messages", {}).get(language, {})
        generated_msg = messages.get("generated_prompt", "Generated prompt with")
        elements_msg = messages.get("cinematic_elements", "cinematic elements")
        selected_msg = messages.get("selected_elements", "Selected elements")
        
        if language == "zh":
            print(f"视频提示词生成器 ({language}): {generated_msg} {len(selected_elements)} {elements_msg}")
        else:
            print(f"VideoPromptGenerator ({language}): {generated_msg} {len(selected_elements)} {elements_msg}")
        
        if selected_elements:
            print(f"{selected_msg}: {selected_elements}")
        
        return (generated_prompt,)

# ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "Video_Prompt_Helper": WanVideoPromptGenerator
}

# 节点显示名称的本地化映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "Video_Prompt_Helper": "Video Prompt Helper"
} 