import os
import json
import re
import matplotlib.pyplot as plt
import pandas as pd

# Root folder containing run folders
root_dir = './'  # adjust as needed

# Regex to match folders like run01-ic7-one-ec7-all, run02-ic7-one-ec7-all...
folder_pattern = re.compile(r'run\d+-.+')

metrics_list = []

for folder_name in os.listdir(root_dir):	
    if folder_pattern.match(folder_name) and os.path.isdir(os.path.join(root_dir, folder_name)):
        json_path = os.path.join(root_dir, folder_name, 'combined_decisions.json')
        if os.path.isfile(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                metrics = data.get('metrics', {})
                
                # Extract and clean metrics (accuracy and recall come as strings like '55.00%')
                accuracy_str = metrics.get('accuracy', '0%')
                recall_str = metrics.get('recall', '0%')
                try:
                    accuracy = float(accuracy_str.strip('%'))
                except:
                    accuracy = None
                try:
                    recall = float(recall_str.strip('%'))
                except:
                    recall = None
                
                TP = metrics.get('TP', None)
                TN = metrics.get('TN', None)
                FP = metrics.get('FP', None)
                FN = metrics.get('FN', None)
                
                metrics_list.append({
                    'folder': folder_name,
                    'accuracy': accuracy,
                    'recall': recall,
                    'TP': TP,
                    'TN': TN,
                    'FP': FP,
                    'FN': FN
                })

# Convert to DataFrame
df = pd.DataFrame(metrics_list)

# Drop rows with None values if any
df_clean = df.dropna(subset=['accuracy', 'recall', 'TP', 'TN', 'FP', 'FN'])

# --- Plot boxplots for accuracy and recall ---
plt.figure(figsize=(10,6))
plt.boxplot([df_clean['accuracy'], df_clean['recall']], labels=['Accuracy (%)', 'Recall (%)'])
plt.title('Boxplots of Accuracy and Recall Across Runs')
plt.grid(True)
plt.show()

# --- Show TP, FP, TN, FN with boxplots or barplots ---
plt.figure(figsize=(10,6))
plt.boxplot([df_clean['TP'], df_clean['FP'], df_clean['TN'], df_clean['FN']], 
            labels=['TP', 'FP', 'TN', 'FN'])
plt.title('Boxplots of Confusion Matrix Components Across Runs')
plt.grid(True)
plt.show()

# Optional: Also print a summary table
print(df_clean.describe())
