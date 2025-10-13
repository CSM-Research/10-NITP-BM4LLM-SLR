import os
import json
import re
import matplotlib.pyplot as plt
import pandas as pd

# Adjustable parameters for label sizes and border width
label_fontsize = 28
tick_fontsize = 22
border_linewidth = 2

# Root folder containing 'high' and 'low' folders
root_dir = './'  # adjust as needed

# Regex to match run folders inside 'high' or 'low' (like run01-ic7-one-ec7-all)
folder_pattern = re.compile(r'run\d+-.+')

metrics_list = []

for group in ['high', 'low']:
    group_path = os.path.join(root_dir, group)
    if os.path.isdir(group_path):
        for folder_name in os.listdir(group_path):
            if folder_pattern.match(folder_name):
                json_path = os.path.join(group_path, folder_name, 'combined_decisions.json')
                if os.path.isfile(json_path):
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        metrics = data.get('metrics', {})

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
                            'group': group,
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

# Helper function for boxplots with custom mean, border styling, and light grey fill
def boxplot_with_custom_mean(ax, data, labels, ymin=None, ymax=None):
    bp = ax.boxplot(data, labels=labels, patch_artist=True,
                    showmeans=True, meanline=True,
                    meanprops=dict(color='black', linewidth=2),
                    boxprops=dict(linewidth=border_linewidth, facecolor='#d3d3d3'),  # light grey fill
                    whiskerprops=dict(linewidth=border_linewidth),
                    capprops=dict(linewidth=border_linewidth),
                    medianprops=dict(linewidth=border_linewidth, color='black'))  # black median line
    if ymin is not None and ymax is not None:
        ax.set_ylim(ymin, ymax)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.tick_params(axis='both', which='major', labelsize=tick_fontsize)
    ax.xaxis.label.set_fontsize(label_fontsize)
    ax.yaxis.label.set_fontsize(label_fontsize)
    for spine in ax.spines.values():
        spine.set_linewidth(border_linewidth)

# --- Plot boxplots comparing accuracy and recall for 'high' and 'low' with same scale ---

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Data for accuracy and recall
data_acc = [df_clean.loc[df_clean['group'] == grp, 'accuracy'] for grp in ['high', 'low']]
data_recall = [df_clean.loc[df_clean['group'] == grp, 'recall'] for grp in ['high', 'low']]

# Determine y-axis limits for both accuracy and recall together
all_acc_recall = pd.concat([pd.concat(data_acc), pd.concat(data_recall)])
ymin = all_acc_recall.min()
ymax = all_acc_recall.max()

boxplot_with_custom_mean(axes[0], data_acc, ['High', 'Low'], ymin, ymax)
axes[0].set_ylabel('Accuracy (%)', fontsize=label_fontsize)

boxplot_with_custom_mean(axes[1], data_recall, ['High', 'Low'], ymin, ymax)
axes[1].set_ylabel('Recall (%)', fontsize=label_fontsize)

plt.tight_layout()
plt.show()

# --- Plot boxplots comparing TP, FP, TN, FN for 'high' and 'low' with same scale ---

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
confusion_metrics = ['TP', 'FP', 'TN', 'FN']
axes = axes.flatten()

for i, metric in enumerate(confusion_metrics):
    data_metric = [df_clean.loc[df_clean['group'] == grp, metric] for grp in ['high', 'low']]
    all_values = pd.concat(data_metric)
    ymin = all_values.min()
    ymax = all_values.max()
    
    boxplot_with_custom_mean(axes[i], data_metric, ['High', 'Low'], ymin, ymax)
    axes[i].set_ylabel(metric, fontsize=label_fontsize)

plt.tight_layout()
plt.show()

# Optional: summary statistics by group
print(df_clean.groupby('group').describe())
