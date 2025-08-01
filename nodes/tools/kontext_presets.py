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
                "brief": "Create a professional product photography scene strictly based on $user_prompt$, ensuring the product's shape, texture, colors, reflections, and surface details remain unchanged. The specified scene in $user_prompt$ is the highest priority and must be accurately represented — avoid default white or studio backgrounds unless explicitly mentioned. Apply a commercial-grade transformation with the following principles: 1. **Scene-Driven Environment**: Always render the environment exactly as described in $user_prompt$ (e.g., shopping mall display, outdoor park, urban street, café table). Do not default to minimal studio setups unless explicitly requested. 2. **Authentic Lighting & Shadows**: Match lighting style to the scene context (e.g., natural sunlight with soft shadows for outdoor settings, ambient mall lighting with mild reflections, warm tones for indoor settings). Keep shadows and highlights consistent with the product's placement. 3. **Professional Composition**: Use framing techniques such as rule of thirds, leading lines, and controlled depth of field. The product must remain the main subject while being naturally integrated with foreground and background elements described in $user_prompt$. 4. **Environmental Realism**: Blend the product seamlessly into the environment with matching perspective, scale, and surface reflections. The surroundings (e.g., floor, textures, props) must look natural and context-aware. 5. **Marketing-Grade Quality**: Maintain sharp focus on the product, with clean and professional color grading that complements both the product and its environment. Avoid any overly flat, artificial, or unprofessional look. 6. **Scene-Specific Detailing**: Include relevant background or prop elements that enhance realism and match $user_prompt$, but never distract from the product as the visual focal point. Final output must resemble a professional product shoot that fits the scene described in $user_prompt$, with no fallback to plain studio or white backgrounds unless explicitly required.",
            },
            {
                "name": "Photo-Product Lifestyle Scene (产品生活场景图)",
                "brief": "Transform the scene into a professional lifestyle photography setup as described in $user_prompt$, featuring a model naturally interacting with the product. The transformation must meet commercial-grade lifestyle photography standards and include: 1. **Model-Product Interaction**: Ensure the model engages with the product naturally (e.g., holding, using, wearing, or demonstrating it) in a realistic and appealing way that highlights its functionality and value. 2. **Lifestyle Environment Integration**: Place the model and product in the requested environment (e.g., home, outdoor, office, or urban lifestyle) with believable interactions and spatial coherence, ensuring the scene enhances the product's narrative. 3. **Professional Model Presentation**: Present the model with confident yet natural body language, realistic poses, and relatable expressions, ensuring all gestures and styling look authentic while meeting professional photography standards. 4. **Product Prominence**: Keep the product clearly visible, well-lit, and integrated into the action flow without being overshadowed by other elements. The product must remain the visual focal point. 5. **Commercial Photography Quality**: Use studio-level or natural lighting setups suitable for the environment, maintain sharp focus, clean composition (rule of thirds, depth of field), and professional color grading suitable for advertising or e-commerce. 6. **Authentic Storytelling**: Design the scene to tell a genuine and aspirational lifestyle story that feels both relatable and inspiring, showing how the product fits into everyday life. Describe the model's position, product interaction details, environmental elements, lighting setup, and any props or styling that enhance the product's commercial appeal while maintaining authenticity and consistency with $user_prompt$.",
            },
            {
                "name": "Photo-Model Hand Product Close-Up (模特手持特写)",
                "brief": "Transform the scene into a professional close-up lifestyle photography setup as described in $user_prompt$, focusing on the model's hands and product interaction. The transformation must meet commercial-grade close-up photography standards and include: 1. **Close-Up Composition**: Frame the shot tightly around the model's hands and the product, minimizing distracting background elements while keeping the product as the clear focal point. 2. **Model-Product Interaction**: Ensure the model's hands hold, use, or interact with the product naturally, showcasing its texture, design, and key features with authentic hand positioning and gesture. 3. **Professional Lighting**: Apply soft, directional lighting (e.g., studio softbox or natural window light) to highlight product surfaces and create realistic shadows and reflections that enhance depth. 4. **Product Emphasis**: Keep the product sharply in focus with macro or medium close-up framing, ensuring its shape, texture, and color remain unchanged and professionally presented. 5. **Lifestyle Touch**: Add subtle lifestyle elements (e.g., a table surface, partial props) to create context without overpowering the product, ensuring the scene looks realistic and engaging. 6. **Commercial Quality**: Use proper color grading, balanced contrast, and a professional finish suitable for e-commerce, social media marketing, or print ads. Describe hand positions, product angle, lighting setup, background tone, and any minimal props that enhance the visual storytelling while keeping the product as the hero element.",
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
                "name": "Art-Anime Style Redraw (动漫风格转绘)",
                "brief": "Redraw the entire image in a distinct cartoon or anime illustration style, adapting to $user_prompt$. Reinterpret the subject with a consistent anime/cartoon aesthetic while maintaining the core visual identity and proportions. The transformation should include: 1. **Adaptation to Recognizable Anime/Manga Styles**: Automatically match or blend the requested style with well-known influences (e.g., Studio Ghibli's painterly warmth, Makoto Shinkai's realistic lighting, CLAMP's elegant character designs, Tezuka Osamu's retro manga line art, or Akira Toriyama's dynamic shapes). 2. **Distinct Visual Characteristics**: Define line work (thin, delicate outlines or bold, thick manga strokes), shading style (cel shading, painterly anime, or retro halftones), and overall drawing techniques consistent with the chosen style. 3. **Color Treatment**: Apply color palettes suited to the style, such as high-saturation tones for shounen anime, soft pastel shades for slice-of-life, or muted cinematic colors for dramatic anime films. Ensure color grading matches the emotional tone. 4. **Character Redesign**: Adjust character proportions and facial features (e.g., large expressive eyes, simplified shapes, or stylized anatomy) while keeping the subject recognizable and respecting the specified style. 5. **Background & Composition**: Simplify, stylize, or repaint the background in the chosen anime/cartoon style (e.g., hand-painted Ghibli-like landscapes, flat-colored comic panels, or vibrant cityscapes). 6. **Stylistic Detailing**: Add stylistic effects like anime light flares, manga speed lines, screentones, or iconic art motifs when suitable for the scene. Provide a single paragraph describing the transformed image, detailing the chosen anime/cartoon style, line work, shading, color palette, background treatment, and stylistic elements, all tailored to $user_prompt$.",
            },
            {
                "name": "Art-Classic Art Movement Style (经典艺术风格模仿)",
                "brief": "Repaint the entire image by transforming it into the style of a famous art movement or artistic genre, adapting to $user_prompt$. Analyze the requested style and apply the defining visual characteristics of the chosen art movement, including: 1. **Art Movement Adaptation**: Automatically match the requested artistic style (e.g., Art Nouveau, Impressionism, Abstract Expressionism, Pop Art, Cubism, Surrealism, Renaissance, Bauhaus, Minimalism). If multiple styles are mentioned, blend them cohesively. 2. **Defining Characteristics**: Capture the key visual features of the style: line work, shapes, and composition approaches. For example, flowing organic lines and floral motifs for Art Nouveau, bold flat colors and comic-like outlines for Pop Art, or soft light and loose brushwork for Impressionism. 3. **Brushwork & Texture**: Apply brushstroke techniques and textural qualities characteristic of the style, such as visible impasto strokes for Impressionism or geometric precision for Cubism. 4. **Color Palette & Tone**: Use color schemes that align with the chosen style, e.g., pastel tones for Rococo, vivid primary colors for De Stijl, or deep contrasting hues for Baroque. 5. **Mood & Atmosphere**: Adjust lighting, shading, and overall ambiance to fully reflect the artistic mood of the movement. 6. **Faithful Transformation**: Maintain the subject's recognizability and key visual elements while fully reinterpreting them through the chosen style's lens. Provide a single paragraph describing the transformed image, specifying the art movement, brushstroke technique, color palette, compositional elements, and mood that define the style, all tailored to $user_prompt$.",
            },
            {
                "name": "Art-Hand-Drawn Master Style (手绘模仿大师)",
                "brief": "Transform the image into a hand-drawn artistic style, adapting to $user_prompt$. Apply the following principles to ensure an authentic hand-rendered appearance: 1. **Flexible Hand-Drawn Style**: Support multiple drawing approaches such as realistic pencil sketch, manga line art, loose doodles, architectural linework, traditional Chinese gongbi (工笔画), or expressive charcoal drawings, depending on $user_prompt$. 2. **Line Quality & Contour Work**: Adjust line density, thickness, and sharpness to reflect the chosen style (e.g., clean, fine outlines for manga; freehand, rough strokes for doodles; precise contour lines for gongbi). 3. **Shading & Texture Techniques**: Apply appropriate shading methods—cross-hatching, stippling, smooth gradients, or tonal layering—to create depth and dimension. Ensure the shading matches the intended hand-drawn aesthetic. 4. **Surface & Medium Effects**: Simulate realistic paper texture, smudging, or brush marks, depending on the chosen medium (e.g., coarse grain for charcoal, smooth rice paper texture for Chinese brush drawings). 5. **Artistic Composition**: Preserve the subject's proportions and structure while simplifying or abstracting details according to the selected hand-drawn style. 6. **Authentic Artistic Feel**: The final image should look like a hand-rendered artwork, as if created by an artist using traditional tools, with all marks and strokes intentionally placed. Provide one clear paragraph describing the chosen hand-drawn style, line quality, shading technique, texture effects, and overall artistic feel, tailored to $user_prompt$.",
            },
            {
                "name": "Art-Cinematic Style Imitation (模仿影视作品风格)",
                "brief": "Transform the image into a cinematic movie poster inspired by $user_prompt$, ensuring the result captures the authentic look and feel of a professional film poster. The transformation should include: 1. **Film Genre & Scene Adaptation**: Adapt the poster's mood and elements to match the film genre specified in $user_prompt$ (e.g., action, sci-fi, fantasy, romance, noir, horror, or documentary). If a particular movie or director's style is mentioned, replicate its cinematic aesthetic (e.g., Quentin Tarantino's retro style, Blade Runner's cyberpunk tone, Marvel's vibrant composition). 2. **Cinematic Visual Treatment**: Use dramatic color grading, depth of field, and cinematic lighting to give the poster a high-production-value look. Apply atmospheric effects when needed (e.g., fog, lens flares, film grain) to enhance the movie vibe. 3. **Poster Composition**: Arrange the elements with a clear visual hierarchy: main characters or product as the focal point, supporting elements arranged around it, and a balanced composition inspired by authentic movie posters. 4. **Typography & Title Design**: Add stylized typography elements (e.g., film title, tagline, director name) with fonts and placement consistent with the genre (e.g., bold sans-serif for action, handwritten script for romance, retro serif for vintage films). 5. **Movie Aesthetic Consistency**: If $user_prompt$ specifies a famous film or franchise, match its poster style (e.g., Star Wars space opera layout, Studio Ghibli's illustrated minimalism, or vintage Hollywood posters). 6. **Authentic Storytelling**: Convey the essence of a movie narrative by integrating visual clues (e.g., key props, character poses, environment details) that hint at the film's plot or emotional tone. Provide a single paragraph describing the poster's visual style, genre, typography, composition, and cinematic effects, all tailored to $user_prompt$ while maintaining a professional movie poster appearance.",
            },
            {
                "name": "Art-Design Diagram (设计图模式)",
                "brief": "Convert the image into a technical drawing or blueprint style, adapting to the user’s specific request: $user_prompt$. The transformation should reflect an authentic technical or schematic visualization, applying the following principles: 1. **Flexible Design Diagram Styles**: Support multiple technical drawing modes, such as architectural blueprints, mechanical engineering schematics, electronic circuit diagrams, industrial product drafts, exploded views, CAD line drawings, or industrial design sketch renders, depending on $user_prompt$. 2. **Line Precision & Drafting Quality**: Use precise, clean, and consistent line work to convey structural accuracy, including contour lines, construction lines, and hatching for depth. Adjust the weight of lines to highlight structural hierarchy. 3. **Annotations & Technical Elements**: Add schematic details like dimensions, arrows, labels, and measurement units. Include technical annotations (e.g., scale marks, section lines, or engineering symbols) to enhance authenticity. 4. **Blueprint & Schematic Styling**: If a blueprint look is requested, apply a white-line-on-blue-background aesthetic with a grid or drafting-paper texture. For mechanical/engineering diagrams, include metallic textures or grayscale CAD line rendering. 5. **Perspective & Projection**: Maintain orthographic or isometric projection when required, ensuring the subject is represented in a clear, technical layout (e.g., top view, side view, or exploded perspective). 6. **Authentic Technical Appearance**: Ensure the final image looks like a professional design document or technical blueprint, as if produced by an architect, engineer, or industrial designer. Provide a single paragraph describing the selected design diagram mode, line characteristics, annotation details, projection type, and overall blueprint aesthetic, all tailored to $user_prompt$.",
            },
            {
                "name": "Art-Digital Caricature Portrait (数字肖像漫画)",
                "brief": "Transform the image into a digital painting caricature style based on $user_prompt$, incorporating playful yet appealing exaggerations while maintaining the subject's recognizable identity. Apply the following principles: 1. **Caricature Style & Exaggeration**: Create tasteful exaggerations (larger eyes, expressive facial features, dynamic gestures) while keeping the subject identifiable, adjusting intensity to suit $user_prompt$ (softer stylization for elegant themes, more expressive for humorous themes). 2. **Painterly Aesthetic**: Apply visible brushstrokes, layered color blending, and painterly shading with textured hand-painted finish, adapting color tone and brush style to match $user_prompt$ (pastel tones, dark fantasy, warm retro). 3. **Background & Environment**: Generate a background environment based on $user_prompt$ (sunset cityscape, whimsical forest, vintage café) with semi-stylized look that complements the caricature subject without distraction. 4. **Lighting & Depth**: Use soft cinematic lighting and clear highlights to emphasize depth and texture, adjusting light direction and mood to match the environment described in $user_prompt$. 5. **Detail Preservation**: Maintain the subject's hairstyle, clothing details, and key facial traits while translating them into caricature style without distorting essential attributes. 6. **Composition & Quality**: Ensure the subject remains the main focal point with simplified painterly background, creating a professional digital caricature painting with vibrant colors, sharp focus on the subject, and clean visual storytelling. Describe the final image including caricature intensity, background environment, color palette, brush style, and lighting, all adapted to $user_prompt$ while preserving subject identity.",
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
                "name": "Utility-Text Addition (添加文字)",
                "brief": "Add visually embedded text to the image with the following specifications based on $user_prompt$: 1. **Text Content**: Specify the exact text to be added, including any special characters, numbers, or phrases. 2. **Text Placement**: Determine the precise location (e.g., upper left corner, center bottom, overlaid on a signboard, floating in the sky, on a wall, on clothing, on a product label). 3. **Text Style**: Apply the specified visual style (e.g., handwritten script, neon glow effect, comic book font, typewriter style, chalk on board, engraved metal, painted graffiti, digital LED display, vintage typography, calligraphy). 4. **Visual Integration**: Ensure the text blends naturally with the scene by matching lighting conditions, perspective, surface textures, and environmental factors. 5. **Contextual Adaptation**: Adjust text size, color, and opacity to fit the scene's mood and maintain readability while respecting the original composition. 6. **Surface Interaction**: If placed on surfaces, ensure the text follows the surface's contours, lighting, and material properties (e.g., text on glass should have transparency, text on metal should have reflections). The text should appear as if it was naturally part of the original scene, with appropriate shadows, highlights, and environmental effects.",
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
