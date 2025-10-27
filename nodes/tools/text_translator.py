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


class GoogleTranslateProvider(TranslationProvider):
    """Google Translate (Free) - Using web interface"""
    
    def __init__(self):
        super().__init__("Google Translate (Free)", True, False)
        self.priority = 1
        self.base_url = "https://translate.googleapis.com/translate_a/single"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        try:
            params = {
                'client': 'gtx',
                'sl': source_lang,
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result and len(result) > 0 and result[0]:
                translated_text = ''.join([item[0] for item in result[0] if item[0]])
                return True, translated_text
            return False, "Translation failed"
            
        except Exception as e:
            return False, f"Google Translate error: {str(e)}"


class LibreTranslateProvider(TranslationProvider):
    """LibreTranslate (Free) - Open source translation"""
    
    def __init__(self):
        super().__init__("LibreTranslate (Free)", True, False)
        self.priority = 2
        self.base_url = "https://libretranslate.de/translate"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        try:
            data = {
                'q': text,
                'source': source_lang if source_lang != "auto" else "en",
                'target': target_lang,
                'format': 'text'
            }
            
            response = requests.post(self.base_url, data=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if 'translatedText' in result:
                return True, result['translatedText']
            return False, "Translation failed"
            
        except Exception as e:
            return False, f"LibreTranslate error: {str(e)}"


class MyMemoryProvider(TranslationProvider):
    """MyMemory (Free) - Community translation"""
    
    def __init__(self):
        super().__init__("MyMemory (Free)", True, False)
        self.priority = 3
        self.base_url = "https://api.mymemory.translated.net/get"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        try:
            params = {
                'q': text,
                'langpair': f"{source_lang}|{target_lang}" if source_lang != "auto" else f"auto|{target_lang}"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('responseStatus') == 200 and 'responseData' in result:
                return True, result['responseData']['translatedText']
            return False, "Translation failed"
            
        except Exception as e:
            return False, f"MyMemory error: {str(e)}"


class DeepLProvider(TranslationProvider):
    """DeepL (Paid) - High quality translation"""
    
    def __init__(self):
        super().__init__("DeepL (Paid)", False, True)
        self.priority = 4
        self.base_url = "https://api-free.deepl.com/v2/translate"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        if not api_key:
            return False, "DeepL requires API key"
        
        try:
            data = {
                'auth_key': api_key,
                'text': text,
                'target_lang': target_lang.upper()
            }
            if source_lang != "auto":
                data['source_lang'] = source_lang.upper()
            
            response = requests.post(self.base_url, data=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if 'translations' in result and len(result['translations']) > 0:
                return True, result['translations'][0]['text']
            return False, "Translation failed"
            
        except Exception as e:
            return False, f"DeepL error: {str(e)}"


class AzureTranslatorProvider(TranslationProvider):
    """Azure Translator (Paid) - Microsoft translation service"""
    
    def __init__(self):
        super().__init__("Azure Translator (Paid)", False, True)
        self.priority = 5
        self.base_url = "https://api.cognitive.microsofttranslator.com/translate"
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto", api_key: str = None) -> Tuple[bool, str]:
        if not api_key:
            return False, "Azure Translator requires API key"
        
        try:
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
            
            response = requests.post(self.base_url, params=params, headers=headers, json=body, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result and len(result) > 0 and 'translations' in result[0]:
                return True, result[0]['translations'][0]['text']
            return False, "Translation failed"
            
        except Exception as e:
            return False, f"Azure Translator error: {str(e)}"


class TextTranslator_UTK:
    CATEGORY = "UniversalToolkit/Tools"
    
    def __init__(self):
        self.providers = {
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
        
        # Handle both string and list inputs
        if isinstance(text, list):
            if not text or len(text) == 0:
                return ("", "", "Error: No text provided")
            # Use the first item if it's a list
            text = str(text[0])
        else:
            text = str(text)
        
        if not text.strip():
            return ("", "", "Error: No text provided")
        
        # Clean API key
        api_key = api_key.strip() if api_key else ""
        
        if provider == "auto":
            # Try providers in priority order
            sorted_providers = sorted(self.providers.values(), key=lambda x: x.priority)
            
            for provider_obj in sorted_providers:
                # Check if API key is required but not provided
                if provider_obj.requires_key and not api_key:
                    continue
                
                success, result = provider_obj.translate(text, target_language, source_language, api_key)
                
                if success:
                    return (result, provider_obj.name, f"Successfully translated using {provider_obj.name}")
                else:
                    # Log the error but continue to next provider
                    print(f"Translation failed with {provider_obj.name}: {result}")
                    continue
            
            return ("", "", "Error: All translation providers failed")
        
        else:
            # Use specific provider
            if provider not in self.providers:
                return ("", "", f"Error: Unknown provider '{provider}'")
            
            provider_obj = self.providers[provider]
            
            # Check API key requirement
            if provider_obj.requires_key and not api_key:
                return ("", "", f"Error: {provider} requires an API key")
            
            success, result = provider_obj.translate(text, target_language, source_language, api_key)
            
            if success:
                return (result, provider_obj.name, f"Successfully translated using {provider_obj.name}")
            else:
                return ("", "", f"Error: {result}")


# Node mappings
NODE_CLASS_MAPPINGS = {
    "TextTranslator_UTK": TextTranslator_UTK,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextTranslator_UTK": "Text Translator (UTK)",
}
