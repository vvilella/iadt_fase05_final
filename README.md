
# IADT Fase 05 — Hackathon
## Detecção de Componentes Arquiteturais + STRIDE

Este projeto apresenta um MVP que combina visão computacional com modelagem de ameaças baseada em STRIDE para automatizar a análise inicial de segurança de diagramas de arquitetura.

A ideia central é simples: receber um diagrama como imagem, identificar automaticamente os principais componentes arquiteturais e gerar um relatório com ameaças e recomendações de mitigação.

O objetivo não é substituir a análise de um especialista em segurança, mas acelerar a identificação inicial de riscos em arquiteturas de sistemas.

---

# Pipeline da Solução

O sistema segue o fluxo abaixo:

Diagrama de arquitetura (imagem)  
↓  
Detecção de componentes arquiteturais (YOLOv8)  
↓  
Classificação em macroclasses arquiteturais  
↓  
Consulta a catálogo de ameaças baseado em STRIDE  
↓  
Geração automática de relatório de segurança

Esse pipeline permite transformar um diagrama visual em uma análise inicial de ameaças de forma automatizada.

---

# Objetivo do Projeto

Dado um diagrama de arquitetura representado como imagem, o sistema é capaz de:

- Detectar automaticamente componentes arquiteturais
- Classificar os componentes identificados
- Gerar um inventário técnico da arquitetura
- Produzir um relatório de ameaças baseado em STRIDE
- Sugerir contramedidas associadas a cada tipo de ameaça

O relatório final apresenta:

- componentes detectados
- bounding boxes
- nível de confiança das detecções
- ameaças típicas associadas ao componente
- recomendações de mitigação

---
# Dataset

O dataset utilizado neste projeto foi obtido a partir de um dataset público contendo ícones de serviços cloud e componentes arquiteturais.

As anotações originais estão no formato VOC/XML e foram utilizadas como base para o treinamento supervisionado do modelo.

Referência do dataset:

https://www.kaggle.com/datasets/carlosrian/software-architecture-dataset

Neste projeto, as classes originais foram consolidadas em seis macroclasses arquiteturais para simplificar o problema de detecção e viabilizar o treinamento do modelo em um ambiente computacional limitado.

---
# Classes Utilizadas no MVP

Para simplificar o problema, diferentes serviços e ícones de arquitetura foram consolidados em seis macroclasses.

| ID | Classe |
|---|---|
| 0 | user |
| 1 | web_app |
| 2 | gateway |
| 3 | service |
| 4 | database |
| 5 | external_service |

Esse agrupamento permite tratar diferentes tecnologias como papéis arquiteturais equivalentes, simplificando o treinamento do modelo.

---

# Metodologia

O dataset original contém anotações em formato VOC/XML com ícones representando serviços cloud.

O processo utilizado foi:

1. Importação do dataset original
2. Mapeamento das classes para as seis macroclasses do projeto
3. Conversão das anotações para o formato YOLO
4. Geração de dataset de treino e validação
5. Treinamento de um detector YOLOv8n

O objetivo foi validar a viabilidade do pipeline completo utilizando um modelo leve.

---

# Estrutura do Projeto

```
data/
 ├── kaggle_raw/           dataset original (não versionado)
 ├── yolo/                 dataset convertido para YOLO
 ├── catalog/              catálogo STRIDE
 ├── class_mapping.yaml    regras de mapeamento das classes
 └── eval/images/          imagens de arquitetura utilizadas na avaliação

scripts/
 └── convert_voc_to_yolo.py

notebooks/
 ├── 01_dataset.ipynb
 ├── 02_train.ipynb
 └── 03_infer_and_report.ipynb

src/
 └── report.py

assets/
 └── outputs/
     └── report.md
```

---

# Setup

Criar ambiente virtual:

python3 -m venv .venv  
source .venv/bin/activate  

Instalar dependências:

pip install -r requirements.txt

---

# 1. Conversão do Dataset

Script responsável por converter as anotações VOC para YOLO:

python scripts/convert_voc_to_yolo.py

Esse passo realiza:

- aplicação do mapeamento de classes
- seleção de amostra do dataset
- criação do split train / validation
- geração do dataset no formato YOLO

---

# 2. Treinamento do Modelo

Abra o notebook:

notebooks/02_train.ipynb

O treinamento utiliza YOLOv8n, uma versão leve da arquitetura YOLO.

O modelo treinado é salvo em:

runs/detect_train_mvp3/weights/best.pt

---

# 3. Inferência

Coloque as imagens do desafio em:

data/eval/images/

Execute:

notebooks/03_infer_and_report.ipynb

Esse notebook realiza:

- carregamento do modelo treinado
- detecção de componentes na imagem
- extração de bounding boxes e confiança
- geração do relatório STRIDE

Saída:

assets/outputs/report.md

---

# Exemplo de Resultado

O relatório final inclui:

- inventário de componentes detectados
- bounding boxes
- confiança das detecções
- ameaças STRIDE associadas ao componente
- recomendações de mitigação

---

# Limitações Conhecidas

Algumas limitações importantes do MVP:

- dataset composto majoritariamente por ícones de serviços cloud
- classes abstratas como user e web_app possuem menor recall
- treinamento realizado com subset do dataset
- modelo utilizado é YOLOv8n (modelo leve)

Essas limitações são esperadas em um protótipo voltado à validação do pipeline.

---

# Possíveis Evoluções

Algumas melhorias possíveis para versões futuras:

- balanceamento das classes do dataset
- aumento do volume de dados de treino
- data augmentation direcionado
- análise de fluxos entre componentes
- geração automática de relatórios em PDF
- integração com ferramentas de documentação de arquitetura

---

# Conclusão

Este projeto demonstra que é possível integrar:

- visão computacional
- detecção de componentes arquiteturais
- modelagem de ameaças baseada em STRIDE

para automatizar uma primeira análise de segurança a partir de diagramas de arquitetura.

Pipeline final:

Diagrama → Detecção → Classificação → STRIDE → Relatório
