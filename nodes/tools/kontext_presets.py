import json


class LoadKontextPresets_UTK:
    data = {
        "prefix": "You are a creative prompt engineer. Your mission is to analyze the provided image and generate exactly 1 distinct image transformation *instructions*. IMPORTANT: You must respond in English only.",
        "presets": [
            # === 拼接/合成图片处理类 ===
            {
                "name": "Context Deep Fusion (情境深度融合)",
                "brief": "IMPORTANT: Respond in English only. The provided image is a composite with a head and body from drastically different contexts (lighting, style, condition). Your mission is to generate instructions for a complete narrative and physical transformation of the head to flawlessly match the body and scene. The instructions must guide the AI to: 1. **Cinematic Re-Lighting**: Describe in vivid detail the scene's light sources (color, direction, hardness) and how this light should sculpt the head's features with new, appropriate shadows and highlights. 2. **Contextual Storytelling**: Instruct to add physical evidence of the scene's story onto the head, such as grime from a battle, sweat from exertion, or rain droplets from a storm. 3. **Color Grading Unification**: Detail how to apply the scene's specific color grade (e.g., cool desaturated tones, warm golden hour hues) to the head. 4. **Asset & Hair Adaptation**: Command the modification or removal of out-of-place elements (like clean jewelry in a gritty scene) and the restyling of the hair to fit the environment (e.g., messy, windblown, wet). 5. **Flawless Final Integration**: As the final step, describe the process of blending the neckline to be completely invisible, ensuring a uniform film grain and texture across the entire person.",
            },
            {
                "name": "Seamless Integration (无痕融合)",
                "brief": "IMPORTANT: Respond in English only. This image is a composite with minor inconsistencies between the head and body. Your task is to generate instructions for a subtle but master-level integration. Focus on creating a photorealistic and utterly convincing final image. The instructions should detail: 1. **Micro-Lighting Adjustment**: Fine-tune the lighting and shadows around the neck and jawline to create a perfect match. 2. **Skin Tone & Texture Unification**: Describe the process of unifying the skin tones for a seamless look, and more importantly, harmonizing the micro-textures like pores, fine hairs, and film grain across the blended area. 3. **Edge Blending Perfection**: Detail how to create an invisible transition at the neckline, making it appear as if it was never separate.",
            },
            # === 场景变换类 ===
            {
                "name": "Scene Teleportation (场景传送)",
                "brief": "IMPORTANT: Respond in English only. Imagine the main subject of the image is suddenly teleported to a completely different and unexpected environment, while maintaining their exact pose. Based on the user's specific request: $user_prompt$, describe this new, richly detailed scene. The instruction must detail how the new environment's lighting and atmosphere should realistically affect the subject, including any necessary adjustments to clothing, accessories, or physical appearance to match the new setting.",
            },
            {
                "name": "Season Change (季节变换)",
                "brief": "IMPORTANT: Respond in English only. Transform the entire scene to be convincingly set in a different season. Based on the user's specific request: $user_prompt$, describe the seasonal transformation in detail. Include atmospheric effects like weather conditions, seasonal lighting, foliage changes, and appropriate clothing adjustments for the subject. Make sure the transformation feels natural and seasonally appropriate.",
            },
            {
                "name": "Fantasy World (幻想领域)",
                "brief": "IMPORTANT: Respond in English only. Transport the entire scene and its subject into a specific, richly detailed fantasy or sci-fi universe. Based on the user's specific request: $user_prompt$, describe the complete aesthetic overhaul. Replace modern elements with fantasy/sci-fi equivalents, transform clothing and accessories to match the new universe, and ensure the subject's appearance fits the magical or futuristic setting.",
            },
            # === 摄影技术类 ===
            {
                "name": "Camera Movement (移动镜头)",
                "brief": "IMPORTANT: Respond in English only. Propose a dramatic and purposeful camera movement that reveals a new perspective or emotion in the scene. Based on the user's specific request: $user_prompt$, describe the *type* of shot and its *narrative purpose*. Explain how this camera movement enhances the story or emotion, and detail any necessary adjustments to composition, lighting, or focus to achieve the desired cinematic effect.",
            },
            {
                "name": "Relighting (重新布光)",
                "brief": "IMPORTANT: Respond in English only. Completely transform the mood and story of the image by proposing a new, cinematic lighting scheme. Based on the user's specific request: $user_prompt$, describe the lighting transformation in detail. Specify light sources, their positions, intensities, colors, and how they create the desired mood. Include any necessary adjustments to shadows, highlights, and overall atmosphere.",
            },
            {
                "name": "Camera Zoom (画面缩放)",
                "brief": "IMPORTANT: Respond in English only. Describe a specific zoom action that serves a narrative purpose. Based on the user's specific request: $user_prompt$, propose either a dramatic 'push-in' (zoom in) or a revealing 'pull-out' (zoom out). Explain the narrative purpose of this zoom, what new information or emotion it reveals, and any necessary adjustments to focus, depth of field, or composition.",
            },
            {
                "name": "Professional Product Photography (专业产品图)",
                "brief": "IMPORTANT: Respond in English only. Re-imagine this image as a high-end commercial product photograph. Based on the user's specific request: $user_prompt$, describe the professional photography setup. Specify the studio lighting arrangement, background treatment, composition style, and any props or lifestyle elements that enhance the product's appeal. Focus on creating an aspirational, commercial-quality image.",
            },
            {
                "name": "Tilt-Shift Miniature (微缩世界)",
                "brief": "IMPORTANT: Respond in English only. Convert the entire scene into a charming and highly detailed miniature model world. Based on the user's specific request: $user_prompt$, describe the tilt-shift miniature effect. Specify the depth of field adjustments, color saturation changes, and any modifications needed to enhance the toy-like, miniature appearance. Include details about focus areas and blur zones.",
            },
            {
                "name": "Reflection Addition (添加倒影)",
                "brief": "IMPORTANT: Respond in English only. Introduce a new, reflective surface into the scene to create a more dynamic composition. Based on the user's specific request: $user_prompt$, describe the reflective surface and its placement. Specify the type of reflection (mirror-like, water, glass, etc.), its quality and distortion, and how it enhances the overall composition and mood of the scene.",
            },
            # === 人物变换类 ===
            {
                "name": "Hair Style Change (更换发型)",
                "brief": "IMPORTANT: Respond in English only. Describe a complete hair transformation for the subject. Based on the user's specific request: $user_prompt$, detail the new hairstyle, including cut, color, texture, and styling. Explain how this hair change reflects the desired persona or story, and include any necessary adjustments to accessories or clothing to complement the new look.",
            },
            {
                "name": "Bodybuilding Transformation (肌肉猛男化)",
                "brief": "IMPORTANT: Respond in English only. Dramatically transform the subject into a hyper-realistic, massively muscled bodybuilder. Based on the user's specific request: $user_prompt$, describe the bodybuilding transformation in detail. Specify muscle development, body proportions, skin texture changes, and any necessary clothing modifications to accommodate and showcase the new physique.",
            },
            {
                "name": "Age Transformation (时光旅人)",
                "brief": "IMPORTANT: Respond in English only. Visibly and realistically age or de-age the main subject. Based on the user's specific request: $user_prompt$, describe the age transformation in detail. Specify facial changes, hair modifications, skin texture adjustments, and any other age-related alterations. Ensure the transformation looks natural and appropriate for the target age.",
            },
            {
                "name": "Fashion Makeover (衣橱改造)",
                "brief": "IMPORTANT: Respond in English only. Give the subject a complete fashion makeover into a specific style. Based on the user's specific request: $user_prompt$, describe the entire outfit transformation. Specify clothing items, accessories, styling details, and how this fashion change reflects the desired aesthetic or persona. Include any necessary adjustments to hair or makeup to complement the new look.",
            },
            # === 环境变换类 ===
            {
                "name": "Furniture Removal (清空家具)",
                "brief": "IMPORTANT: Respond in English only. Imagine the room in the image has been completely emptied for renovation. Based on the user's specific request: $user_prompt$, describe the furniture removal process. Specify what items need to be removed, how to realistically recreate the empty surfaces, and any necessary adjustments to lighting or architectural details to maintain the room's integrity.",
            },
            {
                "name": "Interior Design (室内设计)",
                "brief": "IMPORTANT: Respond in English only. Redesign this space in a specific, evocative style. Based on the user's specific request: $user_prompt$, describe the complete interior redesign. Specify furniture, color schemes, lighting, decor elements, and overall aesthetic while keeping the room's core structure intact. Create a cohesive design that reflects the desired style and mood.",
            },
            # === 艺术风格类 ===
            {
                "name": "Image Colorization (图像上色)",
                "brief": "IMPORTANT: Respond in English only. Describe a specific artistic style for colorizing a black and white image. Based on the user's specific request: $user_prompt$, detail the colorization approach. Specify color palette choices, artistic style influences, mood considerations, and any special effects that enhance the colorization. Go beyond simple colorization to create an artistic interpretation.",
            },
            {
                "name": "Cartoon/Anime Style (卡通漫画化)",
                "brief": "IMPORTANT: Respond in English only. Redraw the entire image in a specific animated or illustrated style. Based on the user's specific request: $user_prompt$, describe the cartoon/anime transformation. Specify the artistic style, visual characteristics, color treatment, and any stylistic elements that define the chosen animation or illustration approach.",
            },
            {
                "name": "Artistic Style Imitation (艺术风格模仿)",
                "brief": "IMPORTANT: Respond in English only. Repaint the entire image in the style of a famous art movement. Based on the user's specific request: $user_prompt$, describe the artistic style transformation. Specify the art movement, its defining characteristics, brushwork techniques, color palette, and any other stylistic elements that capture the essence of the chosen artistic style.",
            },
            {
                "name": "Pixel Art (像素艺术)",
                "brief": "IMPORTANT: Respond in English only. Deconstruct the image into pixel art aesthetic. Based on the user's specific request: $user_prompt$, describe the pixel art transformation. Specify color palette limitations, pixel resolution, dithering techniques, and any retro gaming influences that create authentic pixel art appearance.",
            },
            {
                "name": "Pencil Sketch (铅笔手绘)",
                "brief": "IMPORTANT: Respond in English only. Transform the image into a pencil sketch style. Based on the user's specific request: $user_prompt$, describe the pencil sketch transformation. Specify line quality, shading techniques, paper texture effects, and any artistic considerations that create an authentic hand-drawn pencil sketch appearance.",
            },
            {
                "name": "Oil Painting (油画风格)",
                "brief": "IMPORTANT: Respond in English only. Transform the image into an oil painting style. Based on the user's specific request: $user_prompt$, describe the oil painting transformation. Specify brushwork techniques, color palette choices, texture effects, and any artistic elements that create an authentic oil painting aesthetic.",
            },
            # === 特殊效果类 ===
            {
                "name": "Material Transformation (材质置换)",
                "brief": "IMPORTANT: Respond in English only. Re-imagine the main subject as a sculpture made from an unexpected material. Based on the user's specific request: $user_prompt$, describe the material transformation. Specify the new material's properties, how it affects the subject's appearance, lighting interactions, and any textural or reflective qualities that define the material.",
            },
            {
                "name": "Movie Poster (电影海报)",
                "brief": "IMPORTANT: Respond in English only. Transform the image into a compelling movie poster. Based on the user's specific request: $user_prompt$, describe the movie poster transformation. Specify the film genre, visual treatment, typography elements, and any cinematic effects that create an authentic movie poster appearance.",
            },
            {
                "name": "Technical Blueprint (蓝图视角)",
                "brief": "IMPORTANT: Respond in English only. Convert the image into a technical blueprint. Based on the user's specific request: $user_prompt$, describe the blueprint transformation. Specify the technical drawing style, measurement annotations, schematic elements, and any architectural or engineering details that create an authentic technical blueprint appearance.",
            },
            # === 实用功能类 ===
            {
                "name": "Text Removal (移除文字)",
                "brief": "IMPORTANT: Respond in English only. Remove all text from the image as a meticulous restoration project. Based on the user's specific request: $user_prompt$, describe the text removal process. Specify which text elements need to be removed, how to reconstruct underlying surfaces, and any restoration techniques needed to create a seamless, text-free image.",
            },
            # === 视角变换类 ===
            {
                "name": "Character Viewpoint Change (角色视角变换)",
                "brief": "IMPORTANT: Respond in English only. Generate a $user_prompt$ view of the same character, keeping all visual features identical, including facial structure, hairstyle, expression, body proportions, clothing design, and rendering style. Only change the viewpoint angle. Ensure that lighting direction, shading, and character identity remain consistent with the original image, with no alterations to details other than the perspective. The instruction must specify the exact camera angle and position while maintaining perfect character consistency.",
            },
        ],
        "suffix": "Your response must consist of concise instruction ready for the image editing AI. Do not add any conversational text, explanations, or deviations; only the instructions. Remember to respond in English only.",
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "preset": ([preset["name"] for preset in cls.data.get("presets", [])],),
            },
            "optional": {
                "user_prompt": ("STRING", {"default": "", "multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Prompt",)
    FUNCTION = "get_preset"
    CATEGORY = "utils"

    @classmethod
    def get_brief_by_name(cls, name):
        for preset in cls.data.get("presets", []):
            if preset["name"] == name:
                return preset["brief"]
        return None

    def get_preset(cls, preset, user_prompt=""):
        # Find the selected preset
        brief_text = ""
        for p in cls.data.get("presets", []):
            if p["name"] == preset:
                brief_text = p["brief"]
                break

        # Replace the placeholder with user prompt
        if user_prompt and user_prompt.strip():
            brief_text = brief_text.replace("$user_prompt$", user_prompt.strip())
        else:
            # If no user prompt provided, remove the placeholder and provide a generic instruction
            brief_text = brief_text.replace(
                "$user_prompt$", "the user's desired transformation"
            )

        brief = "The Brief:" + brief_text
        fullString = (
            cls.data.get("prefix") + "\n" + brief + "\n" + cls.data.get("suffix")
        )
        return (fullString,)


NODE_CLASS_MAPPINGS = {
    "LoadKontextPresets_UTK": LoadKontextPresets_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadKontextPresets_UTK": "Kontext VLM System Presets (UTK)",
}
