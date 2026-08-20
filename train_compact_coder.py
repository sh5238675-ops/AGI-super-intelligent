#!/usr/bin/env python3
"""
Compact Coder Model - 2GB Programming AI
Bilingual support (English + Bengali)
"""

import torch
import json
import os
from transformers import (
    GPT2Tokenizer, 
    GPT2LMHeadModel,
    TextDataset,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments
)
from peft import get_peft_model, LoraConfig, TaskType
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompactCoderTrainer:
    def __init__(self, config_path="config.json"):
        """Initialize the compact coder trainer"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
    def load_model(self):
        """Load GPT2 model with configuration"""
        logger.info("Loading model...")
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        
        # Add special tokens for Bengali
        special_tokens = {
            "additional_special_tokens": [
                "[BENGALI_CODE]", "[ENGLISH_CODE]", 
                "[FUNCTION]", "[CLASS]", "[LOOP]"
            ]
        }
        self.tokenizer.add_special_tokens(special_tokens)
        self.model.resize_token_embeddings(len(self.tokenizer))
        
        return self.model
    
    def apply_lora(self):
        """Apply LoRA for efficient training"""
        logger.info("Applying LoRA adaptation...")
        
        peft_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=8,
            lora_alpha=32,
            lora_dropout=0.1,
            target_modules=["c_attn", "c_proj"]
        )
        
        self.model = get_peft_model(self.model, peft_config)
        self.model.print_trainable_parameters()
        
        return self.model
    
    def create_training_data(self):
        """Create sample training data for demonstration"""
        logger.info("Creating training data...")
        
        training_data = """
        # Python Function
        def fibonacci(n):
            '''বাংলা: ফিবোনাচি সিরিজ তৈরি করুন'''
            if n <= 1:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
        
        # JavaScript Code
        function checkPalindrome(str) {
            // ইংরেজি: Check if string is palindrome
            return str === str.split('').reverse().join('');
        }
        
        # C++ Algorithm
        #include <iostream>
        int binarySearch(int arr[], int n, int x) {
            int left = 0, right = n - 1;
            while (left <= right) {
                int mid = left + (right - left) / 2;
                if (arr[mid] == x) return mid;
                if (arr[mid] < x) left = mid + 1;
                else right = mid - 1;
            }
            return -1;
        }
        
        # Java Class
        class DataStructure {
            private int[] array;
            
            public DataStructure(int size) {
                this.array = new int[size];
            }
            
            public void insert(int value) {
                // ইনসার্ট অপারেশন
            }
        }
        """
        
        # Save training data
        os.makedirs("training_data", exist_ok=True)
        with open("training_data/code_samples.txt", "w", encoding="utf-8") as f:
            f.write(training_data)
        
        return "training_data/code_samples.txt"
    
    def train(self):
        """Train the model"""
        logger.info("Starting training...")
        
        # Load model
        self.load_model()
        self.model.to(self.device)
        
        # Apply LoRA
        self.apply_lora()
        
        # Create training data
        train_file = self.create_training_data()
        
        # Dataset
        train_dataset = TextDataset(
            tokenizer=self.tokenizer,
            file_path=train_file,
            block_size=512
        )
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir="./model_output",
            overwrite_output_dir=True,
            num_train_epochs=self.config["training"]["epochs"],
            per_device_train_batch_size=self.config["training"]["batch_size"],
            save_steps=100,
            save_total_limit=2,
            logging_steps=10,
            learning_rate=self.config["training"]["learning_rate"],
            weight_decay=self.config["training"]["weight_decay"],
            warmup_steps=self.config["training"]["warmup_steps"],
        )
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
        )
        
        # Train
        trainer.train()
        
        logger.info("Training completed!")
        
        # Save model
        self.save_model()
    
    def save_model(self):
        """Save the trained model"""
        logger.info("Saving model...")
        
        os.makedirs("./compact_coder_model", exist_ok=True)
        
        self.model.save_pretrained("./compact_coder_model")
        self.tokenizer.save_pretrained("./compact_coder_model")
        
        # Save config
        with open("./compact_coder_model/config_info.json", "w") as f:
            json.dump(self.config, f, indent=2)
        
        logger.info("Model saved to ./compact_coder_model")

def main():
    """Main training function"""
    trainer = CompactCoderTrainer()
    trainer.train()

if __name__ == "__main__":
    main()
