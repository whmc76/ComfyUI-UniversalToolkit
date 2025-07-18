import json


class LoadKontextPresets_UTK:
    data = {
        "prefix": "You are a creative prompt engineer. Your mission is to analyze the provided image and generate exactly 1 distinct image transformation *instructions*. IMPORTANT: You must respond in English only.",
        "presets": [
            # === 核心编辑类 ===
            {
                "name": "Core-Universal Editor (万能编辑)",
                "brief": "You are a task-aware prompt translator for single-image editing using the Kontext format with the Flux model. Your role is to convert the user's natural language instruction into a clean, precise, and visually consistent image editing directive. Follow these strict rules: 1. Do not describe the original image - assume the model sees it. 2. Only describe what needs to change using clear verbs like replace, add, remove, insert, transform into, convert to. 3. Always state what must remain unchanged: for persons preserve facial features, expression, pose, hairstyle, skin tone, body proportion, clothing texture, and lighting; for objects preserve shape, scale, material, texture, surface details, lighting, reflections, and shadow behavior. 4. For background changes describe only the new scene, keep the main subject in exact same position, scale, lighting, and focus, ensure visual integration. 5. For style transfer name the visual style specifically and maintain original composition. 6. For text editing use quotes for target text and specify font retention if needed. 7. For composite edits ensure product stays visually dominant and unchanged with seamless integration. 8. Break complex changes into clear simple steps. 9. Output must be one paragraph in natural English starting with change description, including what to preserve, ending with visual consistency requirements. Based on the user's specific request: $user_prompt$, provide a precise editing instruction that follows these guidelines.",
            },
            # === 图像合成类 ===
            {
                "name": "Composite-Context Deep Fusion (情境深度融合)",
                "brief": "The provided image is a composite with a head and body from drastically different contexts (lighting, style, condition). Your mission is to generate instructions for a complete narrative and physical transformation of the head to flawlessly match the body and scene. The instructions must guide the AI to: 1. **Cinematic Re-Lighting**: Describe in vivid detail the scene's light sources (color, direction, hardness) and how this light should sculpt the head's features with new, appropriate shadows and highlights. 2. **Contextual Storytelling**: Instruct to add physical evidence of the scene's story onto the head, such as grime from a battle, sweat from exertion, or rain droplets from a storm. 3. **Color Grading Unification**: Detail how to apply the scene's specific color grade (e.g., cool desaturated tones, warm golden hour hues) to the head. 4. **Asset & Hair Adaptation**: Command the modification or removal of out-of-place elements (like clean jewelry in a gritty scene) and the restyling of the hair to fit the environment (e.g., messy, windblown, wet). 5. **Flawless Final Integration**: As the final step, describe the process of blending the neckline to be completely invisible, ensuring a uniform film grain and texture across the entire person.",
            },
            {
                "name": "Composite-Seamless Integration (无痕融合)",
                "brief": "This image is a composite with minor inconsistencies between the head and body. Your task is to generate instructions for a subtle but master-level integration. Focus on creating a photorealistic and utterly convincing final image. The instructions should detail: 1. **Micro-Lighting Adjustment**: Fine-tune the lighting and shadows around the neck and jawline to create a perfect match. 2. **Skin Tone & Texture Unification**: Describe the process of unifying the skin tones for a seamless look, and more importantly, harmonizing the micro-textures like pores, fine hairs, and film grain across the blended area. 3. **Edge Blending Perfection**: Detail how to create an invisible transition at the neckline, making it appear as if it was never separate.",
            },
            # === 场景环境类 ===
            {
                "name": "Scene-Scene Teleportation (场景传送)",
                "brief": "Imagine the main subject of the image is suddenly teleported to a completely different and unexpected environment, while maintaining their exact pose. Based on the user's specific request: $user_prompt$, describe this new, richly detailed scene. The instruction must detail how the new environment's lighting and atmosphere should realistically affect the subject, including any necessary adjustments to clothing, accessories, or physical appearance to match the new setting.",
            },
            {
                "name": "Scene-Season Change (季节变换)",
                "brief": "Transform the entire scene to be convincingly set in a different season. Based on the user's specific request: $user_prompt$, describe the seasonal transformation in detail. Include atmospheric effects like weather conditions, seasonal lighting, foliage changes, and appropriate clothing adjustments for the subject. Make sure the transformation feels natural and seasonally appropriate.",
            },
            {
                "name": "Scene-Fantasy World (幻想领域)",
                "brief": "Transport the entire scene and its subject into a specific, richly detailed fantasy or sci-fi universe. Based on the user's specific request: $user_prompt$, describe the complete aesthetic overhaul. Replace modern elements with fantasy/sci-fi equivalents, transform clothing and accessories to match the new universe, and ensure the subject's appearance fits the magical or futuristic setting.",
            },
            {
                "name": "Scene-Furniture Removal (清空家具)",
                "brief": "Imagine the room in the image has been completely emptied for renovation. Based on the user's specific request: $user_prompt$, describe the furniture removal process. Specify what items need to be removed, how to realistically recreate the empty surfaces, and any necessary adjustments to lighting or architectural details to maintain the room's integrity.",
            },
            {
                "name": "Scene-Interior Design (室内设计)",
                "brief": "Redesign this space in a specific, evocative style. Based on the user's specific request: $user_prompt$, describe the complete interior redesign. Specify furniture, color schemes, lighting, decor elements, and overall aesthetic while keeping the room's core structure intact. Create a cohesive design that reflects the desired style and mood.",
            },
            # === 摄影技术类 ===
            {
                "name": "Photo-Camera Movement (移动镜头)",
                "brief": "Propose a dramatic and purposeful camera movement that reveals a new perspective or emotion in the scene. Based on the user's specific request: $user_prompt$, describe the *type* of shot and its *narrative purpose*. Explain how this camera movement enhances the story or emotion, and detail any necessary adjustments to composition, lighting, or focus to achieve the desired cinematic effect.",
            },
            {
                "name": "Photo-Relighting (重新布光)",
                "brief": "Completely transform the mood and story of the image by proposing a new, cinematic lighting scheme. Based on the user's specific request: $user_prompt$, describe the lighting transformation in detail. Specify light sources, their positions, intensities, colors, and how they create the desired mood. Include any necessary adjustments to shadows, highlights, and overall atmosphere.",
            },
            {
                "name": "Photo-Camera Zoom (画面缩放)",
                "brief": "Describe a specific zoom action that serves a narrative purpose. Based on the user's specific request: $user_prompt$, propose either a dramatic 'push-in' (zoom in) or a revealing 'pull-out' (zoom out). Explain the narrative purpose of this zoom, what new information or emotion it reveals, and any necessary adjustments to focus, depth of field, or composition.",
            },
            {
                "name": "Photo-Professional Product Photography (专业产品图)",
                "brief": "Place the product in $user_prompt$, ensuring its shape, texture, colors, and surface details remain unchanged. This professional photography transformation can include: 1. **Studio Environment Setup**: Create high-end commercial photography settings with professional lighting, backdrops, and staging elements. 2. **Lifestyle Integration**: Place the product in realistic lifestyle contexts like home environments, office settings, outdoor scenes, or social situations. 3. **Commercial Presentation**: Transform into catalog-style photography with clean backgrounds, product-focused composition, and professional styling. 4. **Atmospheric Contexts**: Integrate products into mood-setting environments like luxury settings, minimalist spaces, or themed atmospheres. 5. **Seasonal Campaigns**: Adapt the scene for seasonal marketing contexts while maintaining product prominence. 6. **Brand Storytelling**: Create narrative-driven scenes that tell a story about the product's use or benefits. Adjust lighting, shadows, and reflections to match the new environment while keeping the product as the visual focus. Do not alter any features of the product itself, only integrate it naturally into the specified scene. Specify the professional photography setup, including studio lighting arrangement, background treatment, composition style, and any props or lifestyle elements that enhance the product's appeal.",
            },
            {
                "name": "Photo-Tilt-Shift Miniature (微缩世界)",
                "brief": "Convert the entire scene into a charming and highly detailed miniature model world. Based on the user's specific request: $user_prompt$, describe the tilt-shift miniature effect. Specify the depth of field adjustments, color saturation changes, and any modifications needed to enhance the toy-like, miniature appearance. Include details about focus areas and blur zones.",
            },
            {
                "name": "Photo-Reflection Addition (添加倒影)",
                "brief": "Introduce a new, reflective surface into the scene to create a more dynamic composition. Based on the user's specific request: $user_prompt$, describe the reflective surface and its placement. Specify the type of reflection (mirror-like, water, glass, etc.), its quality and distortion, and how it enhances the overall composition and mood of the scene.",
            },
            {
                "name": "Photo-Character Pose & Viewpoint Change (角色姿势视角变换)",
                "brief": "Adjust the character to $user_prompt$, with the camera positioned according to the specified angle and position, while the character is performing the described action, maintaining all facial features, hairstyle, clothing details, body proportions, and overall style. This transformation can include: 1. **Camera Angle Changes**: Modify viewing angles from front, side, back, high angle, low angle, or diagonal perspectives while maintaining character consistency. 2. **Pose Adjustments**: Change body positioning, gestures, and stance while keeping natural body language and realistic proportions. 3. **Viewpoint Variations**: Create different narrative perspectives like close-up, medium shot, full body, or environmental shots. 4. **Dynamic Poses**: Transform static poses into action-oriented or expressive positions while maintaining character identity. 5. **Environmental Integration**: Adjust character positioning within the scene context while preserving scene composition. 6. **Emotional Expression**: Modify pose to convey specific emotions or attitudes while keeping facial features consistent. Ensure lighting, shadows, and perspective remain natural and consistent with the original scene. Specify the exact camera angle, position, and character action while maintaining perfect character consistency.",
            },
            # === 人物变换类 ===
            {
                "name": "Character-Hair Style Change (更换发型)",
                "brief": "Describe a complete hair transformation for the subject. Based on the user's specific request: $user_prompt$, detail the new hairstyle, including cut, color, texture, and styling. Explain how this hair change reflects the desired persona or story, and include any necessary adjustments to accessories or clothing to complement the new look.",
            },
            {
                "name": "Character-Body Physique Transformation (身材改造)",
                "brief": "Modify the body shape by $user_prompt$, ensuring all other visual features remain unchanged. This transformation can include various body modifications such as: 1. **Muscle Development**: Add or reduce muscle mass, define specific muscle groups (arms, chest, abs, legs), or create different bodybuilding styles (bodybuilder, athletic, lean muscular). 2. **Body Proportions**: Adjust height (taller or shorter), body frame size, shoulder width, waist size, and overall body proportions. 3. **Weight Changes**: Add or reduce body fat, create slim/lean physique, or add healthy weight distribution. 4. **Body Type Variations**: Transform into different body types like ectomorph (slim), mesomorph (athletic), endomorph (larger frame), or combinations. 5. **Aesthetic Goals**: Create specific aesthetic outcomes like 'dad bod', 'fitness model', 'strongman', 'swimmer's build', 'runner's physique', or 'yoga instructor' body. 6. **Gender-Specific Transformations**: For male subjects - create masculine features, broader shoulders, defined jawline; for female subjects - create feminine curves, toned muscles, or athletic build. Keep the face, hairstyle, clothing style, textures, colors, and proportions of unrelated body parts exactly as they are. Maintain realistic lighting, shadows, and perspective so the adjusted body shape appears natural and seamlessly integrated into the scene. Specify the exact body transformation details, including muscle definition, body fat percentage, height adjustments, and any necessary clothing modifications to showcase or accommodate the new physique.",
            },
            {
                "name": "Character-Age Transformation (时光旅人)",
                "brief": "Visibly and realistically age or de-age the main subject. Based on the user's specific request: $user_prompt$, describe the age transformation in detail. Specify facial changes, hair modifications, skin texture adjustments, and any other age-related alterations. Ensure the transformation looks natural and appropriate for the target age.",
            },
            {
                "name": "Character-Fashion Makeover (衣橱改造)",
                "brief": "Replace the current outfit with $user_prompt$, ensuring the face, hairstyle, body shape, pose, and all other visual features remain unchanged. This fashion transformation can include: 1. **Complete Outfit Changes**: Replace entire clothing ensemble with new styles, from casual to formal, sporty to elegant, or seasonal variations. 2. **Style Transformations**: Convert between different fashion aesthetics like streetwear, business attire, vintage, bohemian, minimalist, or avant-garde. 3. **Seasonal Adaptations**: Adjust clothing for different weather conditions and seasons while maintaining style coherence. 4. **Occasion-Specific Dressing**: Create appropriate attire for specific events like weddings, parties, work, sports, or casual outings. 5. **Accessory Integration**: Add or modify accessories like jewelry, bags, shoes, hats, or scarves to complement the new outfit. 6. **Cultural Fashion**: Incorporate traditional or cultural clothing styles while maintaining modern appeal. Maintain the original lighting, shadows, and fabric texture realism, with the new clothing appearing naturally worn and consistent with the character's body. Do not alter any other elements in the scene. Specify the exact clothing items, styling details, and how this fashion change reflects the desired aesthetic or persona.",
            },
            # === 艺术风格类 ===
            {
                "name": "Art-Image Colorization (图像上色)",
                "brief": "Describe a specific artistic style for colorizing a black and white image. Based on the user's specific request: $user_prompt$, detail the colorization approach. Specify color palette choices, artistic style influences, mood considerations, and any special effects that enhance the colorization. Go beyond simple colorization to create an artistic interpretation.",
            },
            {
                "name": "Art-Cartoon/Anime Style (卡通漫画化)",
                "brief": "Redraw the entire image in a specific animated or illustrated style. Based on the user's specific request: $user_prompt$, describe the cartoon/anime transformation. Specify the artistic style, visual characteristics, color treatment, and any stylistic elements that define the chosen animation or illustration approach.",
            },
            {
                "name": "Art-Artistic Style Imitation (艺术风格模仿)",
                "brief": "Repaint the entire image in the style of a famous art movement. Based on the user's specific request: $user_prompt$, describe the artistic style transformation. Specify the art movement, its defining characteristics, brushwork techniques, color palette, and any other stylistic elements that capture the essence of the chosen artistic style.",
            },
            {
                "name": "Art-Pixel Art (像素艺术)",
                "brief": "Deconstruct the image into pixel art aesthetic. Based on the user's specific request: $user_prompt$, describe the pixel art transformation. Specify color palette limitations, pixel resolution, dithering techniques, and any retro gaming influences that create authentic pixel art appearance.",
            },
            {
                "name": "Art-Pencil Sketch (铅笔手绘)",
                "brief": "Transform the image into a pencil sketch style. Based on the user's specific request: $user_prompt$, describe the pencil sketch transformation. Specify line quality, shading techniques, paper texture effects, and any artistic considerations that create an authentic hand-drawn pencil sketch appearance.",
            },
            {
                "name": "Art-Oil Painting (油画风格)",
                "brief": "Transform the image into an oil painting style. Based on the user's specific request: $user_prompt$, describe the oil painting transformation. Specify brushwork techniques, color palette choices, texture effects, and any artistic elements that create an authentic oil painting aesthetic.",
            },
            {
                "name": "Art-Movie Poster (电影海报)",
                "brief": "Transform the image into a compelling movie poster. Based on the user's specific request: $user_prompt$, describe the movie poster transformation. Specify the film genre, visual treatment, typography elements, and any cinematic effects that create an authentic movie poster appearance.",
            },
            {
                "name": "Art-Technical Blueprint (蓝图视角)",
                "brief": "Convert the image into a technical blueprint. Based on the user's specific request: $user_prompt$, describe the blueprint transformation. Specify the technical drawing style, measurement annotations, schematic elements, and any architectural or engineering details that create an authentic technical blueprint appearance.",
            },
            # === 实用功能类 ===
            {
                "name": "Utility-Material Transformation (材质置换)",
                "brief": "Re-imagine the main subject as a sculpture made from an unexpected material. Based on the user's specific request: $user_prompt$, describe the material transformation. Specify the new material's properties, how it affects the subject's appearance, lighting interactions, and any textural or reflective qualities that define the material.",
            },
            {
                "name": "Utility-Pattern Extraction (花纹提取)",
                "brief": "Extract the visible pattern or logo from the $user_prompt$ in the image and convert it into a seamless flat texture. Remove all lighting, shading, wrinkles, folds, and perspective distortions. Ensure the output is a clean, high-resolution top-down view of the pattern with no character, background, or surrounding elements included. Preserve the original colors, fine details, and relative scale of the pattern as seen on the specified object. The extraction should isolate the pattern completely, eliminating any 3D effects, shadows, or environmental influences while maintaining the authentic visual characteristics and color palette of the original design.",
            },
            {
                "name": "Utility-Text Removal (移除文字)",
                "brief": "Remove all text from the image as a meticulous restoration project. Based on the user's specific request: $user_prompt$, describe the text removal process. Specify which text elements need to be removed, how to reconstruct underlying surfaces, and any restoration techniques needed to create a seamless, text-free image.",
            },
        ],
        "suffix": "Your response must consist of concise instruction ready for the image editing AI. Do not add any conversational text, explanations, or deviations; only the instructions.",
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
