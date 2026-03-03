# IADT Fase 05 --- Hackathon

## Arquitetura + Detecção Automática + STRIDE

Este projeto implementa um pipeline end-to-end para:

1.  Converter dataset anotado (VOC/XML) em YOLO\
2.  Treinar um detector de objetos (YOLOv8)\
3.  Detectar componentes arquiteturais em diagramas\
4.  Gerar automaticamente um relatório de ameaças baseado em STRIDE

------------------------------------------------------------------------

# Objetivo

Dado um diagrama de arquitetura (imagem), o sistema:

-   Detecta componentes (gateway, service, database, etc.)
-   Classifica cada componente
-   Gera inventário técnico
-   Produz relatório STRIDE automático com:
    -   vulnerabilidades típicas
    -   recomendações de mitigação

------------------------------------------------------------------------

# Classes do MVP

  ID   Classe
  ---- ------------------
  0    user
  1    web_app
  2    gateway
  3    service
  4    database
  5    external_service

------------------------------------------------------------------------

# Estrutura do Projeto

    data/
     ├── kaggle_raw/           # Dataset bruto (ignorado no Git)
     ├── yolo/                 # Dataset convertido (YOLO format)
     ├── catalog/              # Catálogo STRIDE
     ├── class_mapping.yaml    # Regras de mapeamento
     └── eval/images/          # Imagens do challenge

    scripts/
     └── convert_voc_to_yolo.py

    notebooks/
     ├── 01_dataset.ipynb
     ├── 02_train.ipynb
     └── 03_infer_and_report.ipynb

    src/
     └── report.py

------------------------------------------------------------------------

# Setup

``` bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

------------------------------------------------------------------------

# 1. Converter Dataset

``` bash
python scripts/convert_voc_to_yolo.py
```

Esse passo:

-   Aplica o mapeamento das classes originais para as 6 classes do MVP
-   Seleciona amostra aleatória controlada
-   Gera split train/val
-   Cria dataset no formato YOLO

------------------------------------------------------------------------

# 2. Treinar Modelo

Abra o notebook:

    notebooks/02_train.ipynb

O modelo treinado será salvo em:

    runs/detect_train_mvp3/weights/best.pt

------------------------------------------------------------------------

# 3. Rodar Inferência

Coloque as imagens do challenge em:

    data/eval/images/

Execute:

    notebooks/03_infer_and_report.ipynb

Saída gerada:

    assets/outputs/report.md

------------------------------------------------------------------------

# Exemplo de Saída

O relatório inclui:

-   Inventário de componentes detectados
-   Bounding boxes
-   Confiança por detecção
-   Ameaças STRIDE por tipo de componente
-   Mitigações recomendadas

------------------------------------------------------------------------

# Limitações Conhecidas

-   Dataset base composto majoritariamente por ícones cloud
    (AWS/Azure/GCP)
-   Classes abstratas como user e web_app possuem menor recall
-   Modelo treinado com subset (MVP)
-   Detector YOLOv8n (modelo leve)

------------------------------------------------------------------------

# Evoluções Futuras

-   Balanceamento por classe
-   Fine-tuning adicional
-   Data augmentation direcionado
-   Pós-processamento para deduplicação
-   Exportação automática para PDF

------------------------------------------------------------------------

# Resultado

Pipeline funcional:

Diagrama → Detecção → Classificação → STRIDE → Relatório Markdown
