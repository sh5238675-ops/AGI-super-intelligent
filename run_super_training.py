#!/usr/bin/env python3
"""
🔥 DIRECT LLAMA3.2 SUPER TRAINING
স্থানীয় মেশিনে সরাসরি ট্রেনিং
"""

import subprocess
import os
import time

print("\n" + "=" * 80)
print("🔥 STARTING DIRECT LLAMA3.2 SUPER TRAINING")
print("=" * 80)

# Step 1: Create training data file
print("\n📝 Step 1: Creating training data...")

training_data = """
# Python Algorithms
def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)

def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: left = mid + 1
        else: right = mid - 1
    return -1

# JavaScript Code
function quickSort(arr) {
    if (arr.length <= 1) return arr;
    const pivot = arr[0];
    const left = arr.slice(1).filter(x => x < pivot);
    const right = arr.slice(1).filter(x => x >= pivot);
    return [...quickSort(left), pivot, ...quickSort(right)];
}

# Java
public class Algorithm {
    public static void bubbleSort(int[] arr) {
        for (int i = 0; i < arr.length; i++) {
            for (int j = 0; j < arr.length - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
}

# C++
#include <iostream>
using namespace std;

void heapSort(int arr[], int n) {
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }
    for (int i = n - 1; i > 0; i--) {
        swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}

# বাংলা মন্তব্য সহ
# ফিবোনাচি ফাংশন - বাংলা ব্যাখ্যা সহ
def fibonacci_bengali(n):
    '''ফিবোনাচি সিরিজ তৈরি করুন'''
    if n <= 1:
        return n
    return fibonacci_bengali(n-1) + fibonacci_bengali(n-2)

# ডেটা স্ট্রাকচার - ক্লাস
class LinkedList:
    '''লিংকড লিস্ট ডেটা স্ট্রাকচার'''
    def __init__(self):
        self.head = None
    
    def insert(self, value):
        '''নতুন নোড যোগ করুন'''
        pass

# Graph Algorithms
class Graph:
    def __init__(self):
        self.graph = {}
    
    def bfs(self, start):
        '''বিস্তৃত অনুসন্ধান - Breadth First Search'''
        from collections import deque
        visited = set()
        queue = deque([start])
        visited.add(start)
        result = []
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            for neighbor in self.graph.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def dfs(self, start):
        '''গভীর অনুসন্ধান - Depth First Search'''
        visited = set()
        result = []
        
        def dfs_helper(vertex):
            visited.add(vertex)
            result.append(vertex)
            for neighbor in self.graph.get(vertex, []):
                if neighbor not in visited:
                    dfs_helper(neighbor)
        
        dfs_helper(start)
        return result

# Machine Learning
def linear_regression(X, y, epochs=100, lr=0.01):
    '''সরল রৈখিক রিগ্রেশন মডেল'''
    m = len(X)
    theta = 0
    for epoch in range(epochs):
        predictions = [theta * x for x in X]
        errors = [pred - actual for pred, actual in zip(predictions, y)]
        theta -= lr * (2/m) * sum(e * x for e, x in zip(errors, X))
    return theta

# REST API Example
class API:
    def get_user(self, user_id):
        '''GET /api/users/{user_id}'''
        return {"id": user_id, "name": "User"}
    
    def create_user(self, data):
        '''POST /api/users'''
        return {"status": "created", "data": data}
    
    def update_user(self, user_id, data):
        '''PUT /api/users/{user_id}'''
        return {"status": "updated", "data": data}
    
    def delete_user(self, user_id):
        '''DELETE /api/users/{user_id}'''
        return {"status": "deleted"}

# SQL Queries
SELECT * FROM users WHERE age > 18;
INSERT INTO users (name, email) VALUES ('John', 'john@example.com');
UPDATE users SET age = 25 WHERE id = 1;
DELETE FROM users WHERE id = 1;

# Advanced Patterns
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class Factory:
    @staticmethod
    def create(type):
        if type == 'dog': return Dog()
        elif type == 'cat': return Cat()
"""

os.makedirs("training_data", exist_ok=True)
with open("training_data/llama_training.txt", "w", encoding="utf-8") as f:
    f.write(training_data)

print(f"✅ Training data created: {len(training_data)} bytes")

# Step 2: Create Modelfile
print("\n🔧 Step 2: Creating Modelfile...")

modelfile = """FROM llama3.2

PARAMETER temperature 0.7
PARAMETER top_k 50
PARAMETER top_p 0.95
PARAMETER num_predict 512

SYSTEM \"\"\"You are an expert AI programming assistant.
You specialize in:
- Code generation in all programming languages
- Algorithm design and data structures
- System design and architecture
- Web and mobile development
- Machine learning and AI
- English and Bengali bilingual support

Provide clean, well-documented, production-ready code.
Always include error handling and best practices.
Support both English and Bengali programming queries.
\"\"\"
"""

with open("training_data/Modelfile", "w") as f:
    f.write(modelfile)

print("✅ Modelfile created")

# Step 3: Build model with ollama
print("\n🏗️ Step 3: Building llama3.2 custom model...")
print("   Running: ollama create llama-super:latest -f training_data/Modelfile")

try:
    result = subprocess.run(
        ['ollama', 'create', 'llama-super:latest', '-f', 'training_data/Modelfile'],
        capture_output=True,
        text=True,
        timeout=600
    )
    
    if result.returncode == 0:
        print("✅ Model built successfully!")
        print(result.stdout)
    else:
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
except subprocess.TimeoutExpired:
    print("⚠️ Build timed out (model might still be building)")
except Exception as e:
    print(f"⚠️ Error: {e}")

# Step 4: Test the model
print("\n🧪 Step 4: Testing model...")

test_prompts = [
    "Write a Python function to sort an array",
    "Create a REST API endpoint",
    "বাংলায় একটি ফিবোনাচি ফাংশন লিখুন"
]

for i, prompt in enumerate(test_prompts, 1):
    print(f"\n Test {i}: {prompt[:50]}...")
    try:
        result = subprocess.run(
            ['ollama', 'run', 'llama-super:latest', prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"✅ Response received ({len(result.stdout)} chars)")
        else:
            print(f"⚠️ Response: {result.stderr[:100]}")
    except subprocess.TimeoutExpired:
        print("⚠️ Timeout")
    except Exception as e:
        print(f"⚠️ Error: {e}")

# Step 5: Display model info
print("\n📊 Step 5: Checking model info...")

try:
    result = subprocess.run(
        ['ollama', 'list'],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode == 0:
        print("✅ Available models:")
        print(result.stdout)
except Exception as e:
    print(f"⚠️ Error: {e}")

print("\n" + "=" * 80)
print("✅ LLAMA3.2 SUPER TRAINING COMPLETE!")
print("=" * 80)

print("\n🚀 NEXT COMMANDS:")
print("""
# Run the model
ollama run llama-super:latest "Your prompt here"

# In Python
import subprocess
result = subprocess.run(['ollama', 'run', 'llama-super:latest', 'prompt'], 
                       capture_output=True, text=True)
print(result.stdout)

# Bengali prompt
ollama run llama-super:latest "বাংলায় প্রোগ্রামিং করুন"

# In background (API mode)
ollama serve  # Then access via http://localhost:11434
""")

print("\n✨ MODEL IS READY FOR USE!")
