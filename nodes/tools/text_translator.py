"""
Text Translator Node
~~~~~~~~~~~~~~~~~~~

A comprehensive text translation node supporting multiple free and paid translation APIs.

:copyright: (c) 2024 by May
:license: MIT, see LICENSE for more details.
"""

import json
import requests
import time
from typing import Dict, List, Optional, Tuple
import hashlib
import random


class TranslationProvider:
    """Base class for translation providers"""
    
    def __init__(self, name: str, is_free: bool, requires_key: bool = False):
        self.name = name
        self.is_free = is_free
        self.requires_key = requires_key
        self.priority = 0  # Lower number = higher priority
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        """Translate text. Returns (success, result)"""
        raise NotImplementedError


class GLM4FlashProvider(TranslationProvider):
    """GLM-4 Flash (Free) - AI-powered translation"""
    
    def __init__(self):
        super().__init__("GLM-4 Flash (Free)", True, False)
        self.priority = 1
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        try:
            print(f"    🔗 Connecting to GLM-4 Flash API...")
            
            # Map language codes to full names
            lang_map = {
                "zh": "Chinese", "en": "English", "ja": "Japanese", "ko": "Korean",
                "fr": "French", "de": "German", "es": "Spanish", "it": "Italian",
                "pt": "Portuguese", "ru": "Russian", "ar": "Arabic", "hi": "Hindi",
                "th": "Thai", "vi": "Vietnamese", "tr": "Turkish", "pl": "Polish",
                "nl": "Dutch", "sv": "Swedish", "da": "Danish", "no": "Norwegian",
                "fi": "Finnish", "cs": "Czech", "hu": "Hungarian", "ro": "Romanian",
                "bg": "Bulgarian", "hr": "Croatian", "sk": "Slovak", "sl": "Slovenian",
                "et": "Estonian", "lv": "Latvian", "lt": "Lithuanian", "el": "Greek",
                "he": "Hebrew", "fa": "Persian", "ur": "Urdu", "bn": "Bengali",
                "ta": "Tamil", "te": "Telugu", "ml": "Malayalam", "kn": "Kannada",
                "gu": "Gujarati", "pa": "Punjabi", "or": "Odia", "as": "Assamese",
                "ne": "Nepali", "si": "Sinhala", "my": "Burmese", "km": "Khmer",
                "lo": "Lao", "ka": "Georgian", "am": "Amharic", "sw": "Swahili",
                "zu": "Zulu", "af": "Afrikaans", "sq": "Albanian", "eu": "Basque",
                "be": "Belarusian", "bs": "Bosnian", "ca": "Catalan", "cy": "Welsh",
                "eo": "Esperanto", "gl": "Galician", "is": "Icelandic", "mk": "Macedonian",
                "mt": "Maltese", "sr": "Serbian", "uk": "Ukrainian", "uz": "Uzbek"
            }
            
            target_lang_name = lang_map.get(target_lang, target_lang)
            
            system_prompt = f"""You are a professional {target_lang_name} native translator who needs to fluently translate text into {target_lang_name}.

## Translation Rules
1. Output only the translated content, without explanations or additional content (such as "Here's the translation:" or "Translation as follows:")
2. The returned translation must maintain exactly the same number of paragraphs and format as the original text
3. If the text contains HTML tags, consider where the tags should be placed in the translation while maintaining fluency
4. For content that should not be translated (such as proper nouns, code, etc.), keep the original text.
5. If input contains %%, use %% in your output, if input has no %%, don't use %% in your output

## OUTPUT FORMAT:
- **Single paragraph input** → Output translation directly (no separators, no extra text)
- **Multi-paragraph input** → Use %% as paragraph separator between translations

## Examples
### Multi-paragraph Input:
Paragraph A
%%
Paragraph B
%%
Paragraph C
%%
Paragraph D

### Multi-paragraph Output:
Translation A
%%
Translation B
%%
Translation C
%%
Translation D

### Single paragraph Input:
Single paragraph content

### Single paragraph Output:
Direct translation without separators"""

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}' if api_key else 'Bearer your-api-key-here'
            }
            
            data = {
                "model": "glm-4-flash",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Translate to {target_lang_name}:\n\n{text}"}
                ],
                "temperature": 0.3,
                "max_tokens": 4000
            }
            
            print(f"    📤 Sending request: {source_lang} -> {target_lang}")
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            print(f"    📥 Response status: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                translated_text = result['choices'][0]['message']['content'].strip()
                print(f"    ✅ GLM-4 Flash success: {len(translated_text)} characters")
                return True, translated_text
            print(f"    ❌ GLM-4 Flash: Invalid response format")
            return False, "Translation failed"
            
        except Exception as e:
            print(f"    ❌ GLM-4 Flash error: {str(e)}")
            return False, f"GLM-4 Flash error: {str(e)}"


class SiliconFlowProvider(TranslationProvider):
    """Silicon Flow (Free) - AI-powered translation"""
    
    def __init__(self):
        super().__init__("Silicon Flow (Free)", True, False)
        self.priority = 2
        self.base_url = "https://api.siliconflow.cn/v1/chat/completions"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        try:
            print(f"    🔗 Connecting to Silicon Flow API...")
            
            # Map language codes to full names
            lang_map = {
                "zh": "Chinese", "en": "English", "ja": "Japanese", "ko": "Korean",
                "fr": "French", "de": "German", "es": "Spanish", "it": "Italian",
                "pt": "Portuguese", "ru": "Russian", "ar": "Arabic", "hi": "Hindi",
                "th": "Thai", "vi": "Vietnamese", "tr": "Turkish", "pl": "Polish",
                "nl": "Dutch", "sv": "Swedish", "da": "Danish", "no": "Norwegian",
                "fi": "Finnish", "cs": "Czech", "hu": "Hungarian", "ro": "Romanian",
                "bg": "Bulgarian", "hr": "Croatian", "sk": "Slovak", "sl": "Slovenian",
                "et": "Estonian", "lv": "Latvian", "lt": "Lithuanian", "el": "Greek",
                "he": "Hebrew", "fa": "Persian", "ur": "Urdu", "bn": "Bengali",
                "ta": "Tamil", "te": "Telugu", "ml": "Malayalam", "kn": "Kannada",
                "gu": "Gujarati", "pa": "Punjabi", "or": "Odia", "as": "Assamese",
                "ne": "Nepali", "si": "Sinhala", "my": "Burmese", "km": "Khmer",
                "lo": "Lao", "ka": "Georgian", "am": "Amharic", "sw": "Swahili",
                "zu": "Zulu", "af": "Afrikaans", "sq": "Albanian", "eu": "Basque",
                "be": "Belarusian", "bs": "Bosnian", "ca": "Catalan", "cy": "Welsh",
                "eo": "Esperanto", "gl": "Galician", "is": "Icelandic", "mk": "Macedonian",
                "mt": "Maltese", "sr": "Serbian", "uk": "Ukrainian", "uz": "Uzbek"
            }
            
            target_lang_name = lang_map.get(target_lang, target_lang)
            
            system_prompt = f"""You are a professional {target_lang_name} native translator who needs to fluently translate text into {target_lang_name}.

## Translation Rules
1. Output only the translated content, without explanations or additional content (such as "Here's the translation:" or "Translation as follows:")
2. The returned translation must maintain exactly the same number of paragraphs and format as the original text
3. If the text contains HTML tags, consider where the tags should be placed in the translation while maintaining fluency
4. For content that should not be translated (such as proper nouns, code, etc.), keep the original text.
5. If input contains %%, use %% in your output, if input has no %%, don't use %% in your output

## OUTPUT FORMAT:
- **Single paragraph input** → Output translation directly (no separators, no extra text)
- **Multi-paragraph input** → Use %% as paragraph separator between translations

## Examples
### Multi-paragraph Input:
Paragraph A
%%
Paragraph B
%%
Paragraph C
%%
Paragraph D

### Multi-paragraph Output:
Translation A
%%
Translation B
%%
Translation C
%%
Translation D

### Single paragraph Input:
Single paragraph content

### Single paragraph Output:
Direct translation without separators"""

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}' if api_key else 'Bearer your-api-key-here'
            }
            
            data = {
                "model": "Qwen/Qwen2.5-7B-Instruct",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Translate to {target_lang_name}:\n\n{text}"}
                ],
                "temperature": 0.3,
                "max_tokens": 4000
            }
            
            print(f"    📤 Sending request: {source_lang} -> {target_lang}")
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            print(f"    📥 Response status: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                translated_text = result['choices'][0]['message']['content'].strip()
                print(f"    ✅ Silicon Flow success: {len(translated_text)} characters")
                return True, translated_text
            print(f"    ❌ Silicon Flow: Invalid response format")
            return False, "Translation failed"
            
        except Exception as e:
            print(f"    ❌ Silicon Flow error: {str(e)}")
            return False, f"Silicon Flow error: {str(e)}"


class BaiduTranslateProvider(TranslationProvider):
    """Baidu Translate (Free) - Baidu translation service"""
    
    def __init__(self):
        super().__init__("Baidu Translate (Free)", True, False)
        self.priority = 3
        self.base_url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        try:
            print(f"    🔗 Connecting to Baidu Translate API...")
            
            # Baidu language code mapping
            lang_map = {
                "auto": "auto", "zh": "zh", "en": "en", "ja": "jp", "ko": "kor",
                "fr": "fra", "de": "de", "es": "spa", "it": "it", "pt": "pt",
                "ru": "ru", "ar": "ara", "hi": "hi", "th": "th", "vi": "vie",
                "tr": "tr", "pl": "pl", "nl": "nl", "sv": "swe", "da": "dan",
                "no": "nor", "fi": "fin", "cs": "cs", "hu": "hu", "ro": "rom",
                "bg": "bul", "hr": "hr", "sk": "sk", "sl": "slo", "et": "est",
                "lv": "lav", "lt": "lit", "el": "el", "he": "heb", "fa": "per",
                "ur": "urd", "bn": "ben", "ta": "tam", "te": "tel", "ml": "mal",
                "kn": "kan", "gu": "guj", "pa": "pan", "or": "ori", "as": "asm",
                "ne": "nep", "si": "sin", "my": "bur", "km": "hkm", "lo": "lao",
                "ka": "geo", "am": "amh", "sw": "swa", "zu": "zul", "af": "afr",
                "sq": "alb", "eu": "baq", "be": "bel", "bs": "bos", "ca": "cat",
                "cy": "wel", "eo": "epo", "gl": "glg", "is": "ice", "mk": "mac",
                "mt": "mlt", "sr": "srp", "uk": "ukr", "uz": "uzb"
            }
            
            baidu_source = lang_map.get(source_lang, "auto")
            baidu_target = lang_map.get(target_lang, "en")
            
            # Generate salt and sign for Baidu API
            import time
            import hashlib
            import random
            
            appid = api_key if api_key else "your_app_id"
            secret_key = "your_secret_key"  # This should be provided separately
            
            salt = str(int(time.time() * 1000) + random.randint(1, 1000))
            sign_str = appid + text + salt + secret_key
            sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
            
            params = {
                'q': text,
                'from': baidu_source,
                'to': baidu_target,
                'appid': appid,
                'salt': salt,
                'sign': sign
            }
            
            print(f"    📤 Sending request: {source_lang} -> {target_lang}")
            response = requests.get(self.base_url, params=params, timeout=10)
            print(f"    📥 Response status: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            if 'trans_result' in result and len(result['trans_result']) > 0:
                translated_text = result['trans_result'][0]['dst']
                print(f"    ✅ Baidu Translate success: {len(translated_text)} characters")
                return True, translated_text
            print(f"    ❌ Baidu Translate: Invalid response format")
            return False, "Translation failed"
            
        except Exception as e:
            print(f"    ❌ Baidu Translate error: {str(e)}")
            return False, f"Baidu Translate error: {str(e)}"


class YoudaoTranslateProvider(TranslationProvider):
    """Youdao Translate (Free) - Youdao translation service"""
    
    def __init__(self):
        super().__init__("Youdao Translate (Free)", True, False)
        self.priority = 4
        self.base_url = "https://openapi.youdao.com/api"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        try:
            print(f"    🔗 Connecting to Youdao Translate API...")
            
            # Youdao language code mapping
            lang_map = {
                "auto": "auto", "zh": "zh-CHS", "en": "en", "ja": "ja", "ko": "ko",
                "fr": "fr", "de": "de", "es": "es", "it": "it", "pt": "pt",
                "ru": "ru", "ar": "ar", "hi": "hi", "th": "th", "vi": "vi",
                "tr": "tr", "pl": "pl", "nl": "nl", "sv": "sv", "da": "da",
                "no": "no", "fi": "fi", "cs": "cs", "hu": "hu", "ro": "ro",
                "bg": "bg", "hr": "hr", "sk": "sk", "sl": "sl", "et": "et",
                "lv": "lv", "lt": "lt", "el": "el", "he": "he", "fa": "fa",
                "ur": "ur", "bn": "bn", "ta": "ta", "te": "te", "ml": "ml",
                "kn": "kn", "gu": "gu", "pa": "pa", "or": "or", "as": "as",
                "ne": "ne", "si": "si", "my": "my", "km": "km", "lo": "lo",
                "ka": "ka", "am": "am", "sw": "sw", "zu": "zu", "af": "af",
                "sq": "sq", "eu": "eu", "be": "be", "bs": "bs", "ca": "ca",
                "cy": "cy", "eo": "eo", "gl": "gl", "is": "is", "mk": "mk",
                "mt": "mt", "sr": "sr", "uk": "uk", "uz": "uz"
            }
            
            youdao_source = lang_map.get(source_lang, "auto")
            youdao_target = lang_map.get(target_lang, "en")
            
            # Generate salt and sign for Youdao API
            import time
            import hashlib
            import random
            
            app_key = api_key if api_key else "your_app_key"
            app_secret = "your_app_secret"  # This should be provided separately
            
            salt = str(int(time.time() * 1000) + random.randint(1, 1000))
            sign_str = app_key + text + salt + app_secret
            sign = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()
            
            data = {
                'q': text,
                'from': youdao_source,
                'to': youdao_target,
                'appKey': app_key,
                'salt': salt,
                'sign': sign,
                'signType': 'v3'
            }
            
            print(f"    📤 Sending request: {source_lang} -> {target_lang}")
            response = requests.post(self.base_url, data=data, timeout=10)
            print(f"    📥 Response status: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            if 'translation' in result and len(result['translation']) > 0:
                translated_text = result['translation'][0]
                print(f"    ✅ Youdao Translate success: {len(translated_text)} characters")
                return True, translated_text
            print(f"    ❌ Youdao Translate: Invalid response format")
            return False, "Translation failed"
            
        except Exception as e:
            print(f"    ❌ Youdao Translate error: {str(e)}")
            return False, f"Youdao Translate error: {str(e)}"


class GoogleTranslateProvider(TranslationProvider):
    """Google Translate (Free) - Using web interface"""
    
    def __init__(self):
        super().__init__("Google Translate (Free)", True, False)
        self.priority = 5
        self.base_url = "https://translate.googleapis.com/translate_a/single"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        try:
            print(f"    🔗 Connecting to Google Translate API...")
            params = {
                'client': 'gtx',
                'sl': source_lang,
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            print(f"    📤 Sending request: {source_lang} -> {target_lang}")
            response = requests.get(self.base_url, params=params, timeout=10)
            print(f"    📥 Response status: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            if result and len(result) > 0 and result[0]:
                translated_text = ''.join([item[0] for item in result[0] if item[0]])
                print(f"    ✅ Google Translate success: {len(translated_text)} characters")
                return True, translated_text
            print(f"    ❌ Google Translate: Invalid response format")
            return False, "Translation failed"
            
        except Exception as e:
            print(f"    ❌ Google Translate error: {str(e)}")
            return False, f"Google Translate error: {str(e)}"


class LibreTranslateProvider(TranslationProvider):
    """LibreTranslate (Free) - Open source translation"""
    
    def __init__(self):
        super().__init__("LibreTranslate (Free)", True, False)
        self.priority = 6
        self.base_url = "https://libretranslate.de/translate"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        try:
            print(f"    🔗 Connecting to LibreTranslate API...")
            data = {
                'q': text,
                'source': source_lang if source_lang != "auto" else "en",
                'target': target_lang,
                'format': 'text'
            }
            
            print(f"    📤 Sending request: {source_lang} -> {target_lang}")
            response = requests.post(self.base_url, data=data, timeout=10)
            print(f"    📥 Response status: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            if 'translatedText' in result:
                translated_text = result['translatedText']
                print(f"    ✅ LibreTranslate success: {len(translated_text)} characters")
                return True, translated_text
            print(f"    ❌ LibreTranslate: Invalid response format")
            return False, "Translation failed"
            
        except Exception as e:
            print(f"    ❌ LibreTranslate error: {str(e)}")
            return False, f"LibreTranslate error: {str(e)}"


class MyMemoryProvider(TranslationProvider):
    """MyMemory (Free) - Community translation"""
    
    def __init__(self):
        super().__init__("MyMemory (Free)", True, False)
        self.priority = 7
        self.base_url = "https://api.mymemory.translated.net/get"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        try:
            print(f"    🔗 Connecting to MyMemory API...")
            params = {
                'q': text,
                'langpair': f"{source_lang}|{target_lang}" if source_lang != "auto" else f"auto|{target_lang}"
            }
            
            print(f"    📤 Sending request: {source_lang} -> {target_lang}")
            response = requests.get(self.base_url, params=params, timeout=10)
            print(f"    📥 Response status: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            if result.get('responseStatus') == 200 and 'responseData' in result:
                translated_text = result['responseData']['translatedText']
                print(f"    ✅ MyMemory success: {len(translated_text)} characters")
                return True, translated_text
            print(f"    ❌ MyMemory: Invalid response (Status: {result.get('responseStatus', 'Unknown')})")
            return False, "Translation failed"
            
        except Exception as e:
            print(f"    ❌ MyMemory error: {str(e)}")
            return False, f"MyMemory error: {str(e)}"


class DeepLProvider(TranslationProvider):
    """DeepL (Paid) - High quality translation"""
    
    def __init__(self):
        super().__init__("DeepL (Paid)", False, True)
        self.priority = 8
        self.base_url = "https://api-free.deepl.com/v2/translate"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        if not api_key:
            print(f"    ❌ DeepL requires API key but none provided")
            return False, "DeepL requires API key"
        
        try:
            print(f"    🔗 Connecting to DeepL API...")
            data = {
                'auth_key': api_key,
                'text': text,
                'target_lang': target_lang.upper()
            }
            if source_lang != "auto":
                data['source_lang'] = source_lang.upper()
            
            print(f"    📤 Sending request: {source_lang} -> {target_lang}")
            response = requests.post(self.base_url, data=data, timeout=10)
            print(f"    📥 Response status: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            if 'translations' in result and len(result['translations']) > 0:
                translated_text = result['translations'][0]['text']
                print(f"    ✅ DeepL success: {len(translated_text)} characters")
                return True, translated_text
            print(f"    ❌ DeepL: Invalid response format")
            return False, "Translation failed"
            
        except Exception as e:
            print(f"    ❌ DeepL error: {str(e)}")
            return False, f"DeepL error: {str(e)}"


class AzureTranslatorProvider(TranslationProvider):
    """Azure Translator (Paid) - Microsoft translation service"""
    
    def __init__(self):
        super().__init__("Azure Translator (Paid)", False, True)
        self.priority = 9
        self.base_url = "https://api.cognitive.microsofttranslator.com/translate"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        if not api_key:
            print(f"    ❌ Azure Translator requires API key but none provided")
            return False, "Azure Translator requires API key"
        
        try:
            print(f"    🔗 Connecting to Azure Translator API...")
            headers = {
                'Ocp-Apim-Subscription-Key': api_key,
                'Content-Type': 'application/json'
            }
            
            params = {
                'api-version': '3.0',
                'to': target_lang
            }
            if source_lang != "auto":
                params['from'] = source_lang
            
            body = [{'text': text}]
            
            print(f"    📤 Sending request: {source_lang} -> {target_lang}")
            response = requests.post(self.base_url, params=params, headers=headers, json=body, timeout=10)
            print(f"    📥 Response status: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            if result and len(result) > 0 and 'translations' in result[0]:
                translated_text = result[0]['translations'][0]['text']
                print(f"    ✅ Azure Translator success: {len(translated_text)} characters")
                return True, translated_text
            print(f"    ❌ Azure Translator: Invalid response format")
            return False, "Translation failed"
            
        except Exception as e:
            print(f"    ❌ Azure Translator error: {str(e)}")
            return False, f"Azure Translator error: {str(e)}"


class TextTranslator_UTK:
    CATEGORY = "UniversalToolkit/Tools"
    
    def __init__(self):
        self.providers = {
            "GLM-4 Flash (Free)": GLM4FlashProvider(),
            "Silicon Flow (Free)": SiliconFlowProvider(),
            "Baidu Translate (Free)": BaiduTranslateProvider(),
            "Youdao Translate (Free)": YoudaoTranslateProvider(),
            "Google Translate (Free)": GoogleTranslateProvider(),
            "LibreTranslate (Free)": LibreTranslateProvider(),
            "MyMemory (Free)": MyMemoryProvider(),
            "DeepL (Paid)": DeepLProvider(),
            "Azure Translator (Paid)": AzureTranslatorProvider(),
        }
    
    @classmethod
    def INPUT_TYPES(cls):
        # Language codes for common languages
        languages = [
            "auto", "en", "zh", "zh-cn", "zh-tw", "ja", "ko", "fr", "de", "es", "it", 
            "pt", "ru", "ar", "hi", "th", "vi", "tr", "pl", "nl", "sv", "da", "no", 
            "fi", "cs", "hu", "ro", "bg", "hr", "sk", "sl", "et", "lv", "lt", "el", 
            "he", "fa", "ur", "bn", "ta", "te", "ml", "kn", "gu", "pa", "or", "as", 
            "ne", "si", "my", "km", "lo", "ka", "am", "sw", "zu", "af", "sq", "eu", 
            "be", "bs", "ca", "cy", "eo", "gl", "is", "mk", "mt", "sr", "uk", "uz"
        ]
        
        # Provider list with free/paid indicators
        provider_list = [
            "auto",
            "GLM-4 Flash (Free)",
            "Silicon Flow (Free)",
            "Baidu Translate (Free)",
            "Youdao Translate (Free)",
            "Google Translate (Free)",
            "LibreTranslate (Free)", 
            "MyMemory (Free)",
            "DeepL (Paid)",
            "Azure Translator (Paid)"
        ]
        
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "Hello, world!",
                    "placeholder": "Enter text to translate..."
                }),
                "target_language": (languages, {"default": "zh"}),
                "source_language": (languages, {"default": "auto"}),
                "provider": (provider_list, {"default": "auto"}),
            },
            "optional": {
                "api_key": ("STRING", {
                    "default": "",
                    "placeholder": "API key (required for paid services)"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("translated_text", "provider_used", "status_message")
    FUNCTION = "translate_text"
    
    def translate_text(self, text, target_language: str, source_language: str, provider: str, api_key: str = ""):
        """Main translation function"""
        
        print(f"🌐 Text Translator (UTK) - Starting translation process")
        print(f"📝 Input text length: {len(str(text))} characters")
        print(f"🎯 Target language: {target_language}")
        print(f"🔍 Source language: {source_language}")
        print(f"🔧 Provider: {provider}")
        
        # Handle both string and list inputs
        if isinstance(text, list):
            print(f"📋 Input is a list with {len(text)} items")
            if not text or len(text) == 0:
                print("❌ Error: Empty list provided")
                return ("", "", "Error: No text provided")
            # Use the first item if it's a list
            text = str(text[0])
            print(f"📄 Using first item from list: {text[:50]}...")
        else:
            text = str(text)
            print(f"📄 Input is a string: {text[:50]}...")
        
        if not text.strip():
            print("❌ Error: Empty text after processing")
            return ("", "", "Error: No text provided")
        
        # Clean API key
        api_key = api_key.strip() if api_key else ""
        if api_key:
            print(f"🔑 API key provided: {api_key[:8]}...")
        else:
            print("🔓 No API key provided")
        
        if provider == "auto":
            print("🔄 Auto mode: Trying providers in priority order")
            # Try providers in priority order
            sorted_providers = sorted(self.providers.values(), key=lambda x: x.priority)
            
            for i, provider_obj in enumerate(sorted_providers, 1):
                print(f"🔍 [{i}/{len(sorted_providers)}] Trying {provider_obj.name}...")
                
                # Check if API key is required but not provided
                if provider_obj.requires_key and not api_key:
                    print(f"⏭️  Skipping {provider_obj.name} - requires API key but none provided")
                    continue
                
                print(f"🌐 Sending request to {provider_obj.name}...")
                success, result = provider_obj.translate(text, target_language, source_language, api_key)
                
                if success:
                    print(f"✅ Success! Translation completed using {provider_obj.name}")
                    print(f"📤 Translated text: {result[:100]}...")
                    return (result, provider_obj.name, f"Successfully translated using {provider_obj.name}")
                else:
                    # Log the error but continue to next provider
                    print(f"❌ Translation failed with {provider_obj.name}: {result}")
                    continue
            
            print("💥 All translation providers failed!")
            return ("", "", "Error: All translation providers failed")
        
        else:
            # Use specific provider
            print(f"🎯 Using specific provider: {provider}")
            if provider not in self.providers:
                print(f"❌ Error: Unknown provider '{provider}'")
                return ("", "", f"Error: Unknown provider '{provider}'")
            
            provider_obj = self.providers[provider]
            print(f"📋 Provider details: {provider_obj.name} (Free: {provider_obj.is_free}, Requires Key: {provider_obj.requires_key})")
            
            # Check API key requirement
            if provider_obj.requires_key and not api_key:
                print(f"❌ Error: {provider} requires an API key but none provided")
                return ("", "", f"Error: {provider} requires an API key")
            
            print(f"🌐 Sending request to {provider_obj.name}...")
            success, result = provider_obj.translate(text, target_language, source_language, api_key)
            
            if success:
                print(f"✅ Success! Translation completed using {provider_obj.name}")
                print(f"📤 Translated text: {result[:100]}...")
                return (result, provider_obj.name, f"Successfully translated using {provider_obj.name}")
            else:
                print(f"❌ Translation failed with {provider_obj.name}: {result}")
                return ("", "", f"Error: {result}")


# Node mappings
NODE_CLASS_MAPPINGS = {
    "TextTranslator_UTK": TextTranslator_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextTranslator_UTK": "Text Translator (UTK)",
}
