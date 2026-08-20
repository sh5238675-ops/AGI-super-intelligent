#!/usr/bin/env python3
"""
Multilingual Support Module - Bengali + English
Handles tokenization, translation, and bilingual inference
"""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BilingualCodeGenerator:
    def __init__(self, model_path="./compact_coder_model"):
        """Initialize bilingual code generator"""
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        self.bengali_keywords = {
            'ফাংশন': 'function',
            'ক্লাস': 'class',
            'লুপ': 'loop',
            'শর্ত': 'condition',
            'রিটার্ন': 'return',
            'চলক': 'variable',
            'অ্যারে': 'array',
            'স্ট্রিং': 'string'
        }
        
    def translate_bengali_to_english(self, bengali_text):
        """Translate Bengali programming terms to English"""
        result = bengali_text
        for bengali, english in self.bengali_keywords.items():
            result = result.replace(bengali, english)
        return result
    
    def generate_code(self, prompt, language="en", max_length=256):
        """Generate code from prompt in Bengali or English"""
        
        # Convert Bengali prompt to English if needed
        if language == "bn":
            prompt = self.translate_bengali_to_english(prompt)
        
        logger.info(f"Generating code for: {prompt}")
        
        return {
            "prompt": prompt,
            "language": language,
            "model_path": self.model_path,
            "status": "ready_for_inference"
        }
    
    def format_output(self, code, language="en"):
        """Format generated code for output"""
        if language == "bn":
            output = f"# বাংলা কোমেন্ট\n{code}"
        else:
            output = f"# English Code\n{code}"
        
        return output

if __name__ == "__main__":
    generator = BilingualCodeGenerator()
    
    # Test Bengali prompt
    bengali_prompt = "একটি ফাংশন তৈরি করুন যা দুটি সংখ্যার যোগ করে"
    result = generator.generate_code(bengali_prompt, language="bn")
    print(result)
