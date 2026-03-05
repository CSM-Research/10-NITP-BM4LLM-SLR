import os
import json
import re
import pandas as pd

# Caminho raiz onde ficam as pastas (pode ajustar)
root_dir = './'

# Regex para identificar pastas de "run" (ex: run01-ic7-one-ec7-all)
folder_pattern = re.compile(r'run\d+-.+')

# Lista onde vamos acumular as linhas
rows = []

# Percorrer todas as subpastas recursivamente
for dirpath, dirnames, filenames in os.walk(root_dir):
    if 'combined_decisions.json' in filenames:
        json_path = os.path.join(dirpath, 'combined_decisions.json')

        # Pasta imediatamente acima do JSON
        folder_name = os.path.basename(dirpath)

        # Grupo pode ser o nome da pasta "pai" (ex: high / low)
        parent_folder = os.path.basename(os.path.dirname(dirpath))

        # Ler o JSON
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Erro ao ler {json_path}: {e}")
            continue

        metrics = data.get('metrics', {})

        # Extrair métricas
        def parse_percent(value):
            try:
                return float(str(value).strip('%'))
            except:
                return None

        row = {
            'group': parent_folder,
            'folder': folder_name,
            'accuracy': parse_percent(metrics.get('accuracy')),
            'recall': parse_percent(metrics.get('recall')),
            'TP': metrics.get('TP'),
            'TN': metrics.get('TN'),
            'FP': metrics.get('FP'),
            'FN': metrics.get('FN')
        }

        rows.append(row)

# Criar DataFrame
df = pd.DataFrame(rows)

# Mostrar
print(df)

# Salvar em CSV
df.to_csv('metrics_summary.csv', index=False)
print("Resumo salvo em metrics_summary.csv")
