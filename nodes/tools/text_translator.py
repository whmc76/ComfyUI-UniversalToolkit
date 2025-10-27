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
        super().__init__("GLM-4 Flash (Free)", True, True)
        self.priority = 6
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

            # Skip if no API key provided for AI services
            if not api_key or api_key == "your-api-key-here":
                print(f"    ⏭️  Skipping GLM-4 Flash - requires API key")
                return False, "GLM-4 Flash requires API key"
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
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
        super().__init__("Silicon Flow (Free)", True, True)
        self.priority = 7
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

            # Skip if no API key provided for AI services
            if not api_key or api_key == "your-api-key-here":
                print(f"    ⏭️  Skipping Silicon Flow - requires API key")
                return False, "Silicon Flow requires API key"
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
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
        super().__init__("Baidu Translate (Free)", True, True)
        self.priority = 8
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
            
            # Skip if no API key provided for Baidu
            if not api_key or api_key == "your_app_id":
                print(f"    ⏭️  Skipping Baidu Translate - requires API key")
                return False, "Baidu Translate requires API key"
            
            # Generate salt and sign for Baidu API
            import time
            import hashlib
            import random
            
            # For demo purposes, use a simple approach
            # In real usage, user should provide both appid and secret_key
            appid = api_key
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
        super().__init__("Youdao Translate (Free)", True, True)
        self.priority = 9
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
            
            # Skip if no API key provided for Youdao
            if not api_key or api_key == "your_app_key":
                print(f"    ⏭️  Skipping Youdao Translate - requires API key")
                return False, "Youdao Translate requires API key"
            
            # Generate salt and sign for Youdao API
            import time
            import hashlib
            import random
            
            # For demo purposes, use a simple approach
            # In real usage, user should provide both app_key and app_secret
            app_key = api_key
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


class MicrosoftTranslateProvider(TranslationProvider):
    """Microsoft Translator (Free) - Microsoft translation service"""
    
    def __init__(self):
        super().__init__("Microsoft Translator (Free)", True, True)
        self.priority = 4
        self.base_url = "https://api.cognitive.microsofttranslator.com/translate"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        try:
            print(f"    🔗 Connecting to Microsoft Translator API...")
            
            # Skip if no API key provided for Microsoft Translator
            if not api_key or api_key == "your_api_key":
                print(f"    ⏭️  Skipping Microsoft Translator - requires API key")
                return False, "Microsoft Translator requires API key"
            
            # Microsoft Translator language code mapping
            lang_map = {
                "auto": "auto", "en": "en", "zh": "zh-Hans", "ja": "ja", "ko": "ko",
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
            
            ms_source = lang_map.get(source_lang, "auto")
            ms_target = lang_map.get(target_lang, "en")
            
            headers = {
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': api_key
            }
            
            params = {
                'api-version': '3.0',
                'to': ms_target
            }
            if ms_source != "auto":
                params['from'] = ms_source
            
            body = [{'text': text}]
            
            print(f"    📤 Sending request: {source_lang} -> {target_lang}")
            response = requests.post(self.base_url, params=params, headers=headers, json=body, timeout=10)
            print(f"    📥 Response status: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            if result and len(result) > 0 and 'translations' in result[0]:
                translated_text = result[0]['translations'][0]['text']
                print(f"    ✅ Microsoft Translator success: {len(translated_text)} characters")
                return True, translated_text
            print(f"    ❌ Microsoft Translator: Invalid response format")
            return False, "Translation failed"
            
        except Exception as e:
            print(f"    ❌ Microsoft Translator error: {str(e)}")
            return False, f"Microsoft Translator error: {str(e)}"


class GoogleTranslateProvider(TranslationProvider):
    """Google Translate (Free) - Using web interface"""
    
    def __init__(self):
        super().__init__("Google Translate (Free)", True, False)
        self.priority = 1
        self.base_url = "https://translate.googleapis.com/translate_a/single"
        self.backup_url = "https://clients5.google.com/translate_a/single"
    
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
            
            # Try primary URL first
            try:
                response = requests.get(self.base_url, params=params, timeout=10)
                print(f"    📥 Response status: {response.status_code}")
                
                if response.status_code == 200:
                    response.raise_for_status()
                    result = response.json()
                    if result and len(result) > 0 and result[0]:
                        translated_text = ''.join([item[0] for item in result[0] if item[0]])
                        print(f"    ✅ Google Translate success: {len(translated_text)} characters")
                        return True, translated_text
                
            except Exception as e:
                print(f"    ⚠️  Primary URL failed: {str(e)}")
            
            # Try backup URL
            try:
                print(f"    🔄 Trying backup URL...")
                response = requests.get(self.backup_url, params=params, timeout=10)
                print(f"    📥 Backup response status: {response.status_code}")
                
                if response.status_code == 200:
                    response.raise_for_status()
                    result = response.json()
                    if result and len(result) > 0 and result[0]:
                        translated_text = ''.join([item[0] for item in result[0] if item[0]])
                        print(f"    ✅ Google Translate (backup) success: {len(translated_text)} characters")
                        return True, translated_text
                
            except Exception as e:
                print(f"    ❌ Backup URL also failed: {str(e)}")
            
            print(f"    ❌ Google Translate: All URLs failed")
            return False, "Translation failed"
            
        except Exception as e:
            print(f"    ❌ Google Translate error: {str(e)}")
            return False, f"Google Translate error: {str(e)}"


class BingTranslateProvider(TranslationProvider):
    """Bing Translator (Free) - Microsoft's free translation service"""
    
    def __init__(self):
        super().__init__("Bing Translator (Free)", True, True)  # Requires API key
        self.priority = 2
        self.base_url = "https://api.cognitive.microsofttranslator.com/translate"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        try:
            print(f"    🔗 Connecting to Bing Translator API...")
            
            # Check if API key is provided
            if not api_key or api_key == "your_api_key":
                print(f"    ⏭️  Skipping Bing Translator - requires API key")
                return False, "Bing Translator requires API key"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': api_key
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
            
            if response.status_code == 200:
                result = response.json()
                if result and len(result) > 0 and 'translations' in result[0]:
                    translated_text = result[0]['translations'][0]['text']
                    print(f"    ✅ Bing Translator success: {len(translated_text)} characters")
                    return True, translated_text
                print(f"    ❌ Bing Translator: Invalid response format")
                return False, "Invalid response format"
            elif response.status_code == 401:
                print(f"    ❌ Bing Translator: Unauthorized (401) - Invalid API key")
                return False, "Invalid API key"
            else:
                print(f"    ❌ Bing Translator: HTTP {response.status_code}")
                return False, f"HTTP error {response.status_code}"
                
        except Exception as e:
            print(f"    ❌ Bing Translator error: {str(e)}")
            return False, f"Bing Translator error: {str(e)}"




class DeepLProvider(TranslationProvider):
    """DeepL (Paid) - High quality translation"""
    
    def __init__(self):
        super().__init__("DeepL (Paid)", False, True)
        self.priority = 10
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
        self.priority = 11
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


class TextTranslatorAPI_UTK:
    CATEGORY = "UniversalToolkit/Tools"
    
    def __init__(self):
        self.providers = {
            "Google Translate (Free)": GoogleTranslateProvider(),
            "Bing Translator (Free)": BingTranslateProvider(),
            "GLM-4 Flash (Free)": GLM4FlashProvider(),
            "Silicon Flow (Free)": SiliconFlowProvider(),
            "Baidu Translate (Free)": BaiduTranslateProvider(),
            "Youdao Translate (Free)": YoudaoTranslateProvider(),
            "Microsoft Translator (Free)": MicrosoftTranslateProvider(),
            "DeepL (Paid)": DeepLProvider(),
            "Azure Translator (Paid)": AzureTranslatorProvider(),
        }
        
        # Language name to code mapping
        self.lang_name_to_code = {
            "auto": "auto", "English": "en", "中文": "zh", "日本語": "ja", "한국어": "ko",
            "Français": "fr", "Deutsch": "de", "Español": "es", "Italiano": "it", 
            "Português": "pt", "Русский": "ru", "العربية": "ar", "हिन्दी": "hi", 
            "ไทย": "th", "Tiếng Việt": "vi", "Türkçe": "tr", "Polski": "pl", 
            "Nederlands": "nl", "Svenska": "sv", "Dansk": "da", "Norsk": "no", 
            "Suomi": "fi", "Čeština": "cs", "Magyar": "hu", "Română": "ro", 
            "Български": "bg", "Hrvatski": "hr", "Slovenčina": "sk", "Slovenščina": "sl", 
            "Eesti": "et", "Latviešu": "lv", "Lietuvių": "lt", "Ελληνικά": "el", 
            "עברית": "he", "فارسی": "fa", "اردو": "ur", "বাংলা": "bn", 
            "தமிழ்": "ta", "తెలుగు": "te", "മലയാളം": "ml", "ಕನ್ನಡ": "kn", 
            "ગુજરાતી": "gu", "ਪੰਜਾਬੀ": "pa", "ଓଡ଼ିଆ": "or", "অসমীয়া": "as", 
            "नेपाली": "ne", "සිංහල": "si", "မြန်မာ": "my", "ខ្មែរ": "km", 
            "ລາວ": "lo", "ქართული": "ka", "አማርኛ": "am", "Kiswahili": "sw", 
            "IsiZulu": "zu", "Afrikaans": "af", "Shqip": "sq", "Euskera": "eu", 
            "Беларуская": "be", "Bosanski": "bs", "Català": "ca", "Cymraeg": "cy", 
            "Esperanto": "eo", "Galego": "gl", "Íslenska": "is", "Македонски": "mk", 
            "Malti": "mt", "Српски": "sr", "Українська": "uk", "O'zbek": "uz"
        }
    
    @classmethod
    def INPUT_TYPES(cls):
        # Language names in their native languages
        languages = [
            "auto", "English", "中文", "日本語", "한국어", "Français", "Deutsch", "Español", "Italiano", 
            "Português", "Русский", "العربية", "हिन्दी", "ไทย", "Tiếng Việt", "Türkçe", "Polski", 
            "Nederlands", "Svenska", "Dansk", "Norsk", "Suomi", "Čeština", "Magyar", "Română", 
            "Български", "Hrvatski", "Slovenčina", "Slovenščina", "Eesti", "Latviešu", "Lietuvių", 
            "Ελληνικά", "עברית", "فارسی", "اردو", "বাংলা", "தமிழ்", "తెలుగు", "മലയാളം", 
            "ಕನ್ನಡ", "ગુજરાતી", "ਪੰਜਾਬੀ", "ଓଡ଼ିଆ", "অসমীয়া", "नेपाली", "සිංහල", "မြန်မာ", 
            "ខ្មែរ", "ລາວ", "ქართული", "አማርኛ", "Kiswahili", "IsiZulu", "Afrikaans", "Shqip", 
            "Euskera", "Беларуская", "Bosanski", "Català", "Cymraeg", "Esperanto", "Galego", 
            "Íslenska", "Македонски", "Malti", "Српски", "Українська", "O'zbek"
        ]
        
        # Provider list with free/paid indicators (ordered by priority)
        provider_list = [
            "auto",
            "--- Free Services ---",
            "Google Translate (Free)",
            "--- Require API Key ---",
            "Bing Translator (Free)",
            "GLM-4 Flash (Free)",
            "Silicon Flow (Free)",
            "Baidu Translate (Free)",
            "Youdao Translate (Free)",
            "Microsoft Translator (Free)",
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
                "target_language": (languages, {"default": "中文"}),
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
        
        # Convert language names to codes
        target_lang_code = self.lang_name_to_code.get(target_language, target_language)
        source_lang_code = self.lang_name_to_code.get(source_language, source_language)
        
        print(f"🌐 Text Translator (UTK) - Starting translation process")
        print(f"📝 Input text length: {len(str(text))} characters")
        print(f"🎯 Target language: {target_language} ({target_lang_code})")
        print(f"🔍 Source language: {source_language} ({source_lang_code})")
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
                success, result = provider_obj.translate(text, target_lang_code, source_lang_code, api_key)
                
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
            
            # Skip separator items
            if provider.startswith("---"):
                print(f"❌ Error: '{provider}' is a separator, not a provider")
                return ("", "", f"Error: '{provider}' is a separator, not a provider")
            
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
            success, result = provider_obj.translate(text, target_lang_code, source_lang_code, api_key)
            
            if success:
                print(f"✅ Success! Translation completed using {provider_obj.name}")
                print(f"📤 Translated text: {result[:100]}...")
                return (result, provider_obj.name, f"Successfully translated using {provider_obj.name}")
            else:
                print(f"❌ Translation failed with {provider_obj.name}: {result}")
                return ("", "", f"Error: {result}")


# Node mappings
NODE_CLASS_MAPPINGS = {
    "TextTranslatorAPI_UTK": TextTranslatorAPI_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextTranslatorAPI_UTK": "Text Translator API (UTK)",
}
