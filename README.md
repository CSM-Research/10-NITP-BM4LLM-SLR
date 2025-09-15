# BM4LLM-SLR  
**Bias Mitigation for LLM-Assisted Systematic Literature Reviews**  

BM4LLM-SLR is a model designed to support researchers during the **study selection phase** of **Systematic Literature Reviews (SLRs)**. Its primary objective is to enhance the use of **Large Language Models (LLMs)** by making them more **reliable, transparent, and less prone to bias**.  

---

## 🚀 Why BM4LLM-SLR?  

Systematic Literature Reviews are critical for consolidating scientific evidence but require **substantial manual effort** and are susceptible to **human error**. While **LLMs** can assist in this process, they may also introduce **bias or inconsistencies** if applied in isolation.  

BM4LLM-SLR introduces a **bias mitigation layer**, offering:  
- ✅ **Configurable confidence thresholds**  
- ✅ **Rigorous control mechanisms for study selection**  
- ✅ **Active engagement of the human reviewer**  

These features increase the **robustness** of results while reducing the likelihood of bias.  

---

## 🛠️ Installation and Usage  

**To set up and run the tool**:  

1. Clone the repository and navigate to the `support-system` folder.  
2. Run `npm install` in the terminal.  
3. Open `localhost:3000` in your browser and explore the available options in the sidebar.  

---

### 1. Running BM4LLM-SLR with Local **Ollama**  

You can use [Ollama](https://ollama.com/) to run models locally.  

With **Docker**:  
```bash
docker run -d --name ollama \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  -e OLLAMA_ORIGINS=* \
  ollama/ollama
```
## 📂 Repository Contents  

This repository provides a tool designed to create a controlled environment for appraising the **BM4LLM-SLR** model. Below is an overview of the key pages and their functionalities.  

### **Introduction**  
Provides an overview of the tool’s purpose. If human participants are involved, this section displays a notification that collected data will be used for research purposes, along with the author’s details. Researchers reusing this tool are encouraged to adapt the disclaimer to their own studies.  

### **Instructions**  
Contains experiment guidelines. These include general information about BM4LLM-SLR and task-specific instructions. Researchers can adapt this section according to their experiment design, clarifying permitted and restricted actions.  

### **Questionnaire**  
Collects demographic and background information about participants, including prior experience with SLRs and related tasks. This data supports subsequent analyses by enabling contextual interpretation of results.  

### **Run Setup**  
Allows participants to configure the experiment. Key inputs include:  
- The **topic** (title of a peer-reviewed literature review) relevant to the participant’s expertise.  
- The **prompt template** (three options available).  
- The **LLMs** to be tested.  

Upon confirmation, a new **run** is initiated, representing a cycle of 20 randomly selected articles. Multiple runs can be registered by modifying these settings.  

### **Automatic Selection**  
Initiates prompt submission to the chosen LLMs. Selected studies are displayed with prompts ready for evaluation. Results are exported in CSV format and stored for subsequent review.  

### **Automated Review**  
Enables configuration of a **confidence threshold** (1–7 Likert scale). Articles are automatically included or excluded based on this threshold, with a recommendation of ≥6 for reliable decisions. Preliminary results can be exported in `.zip` format.  

### **Consensus Building**  
Validates automatic selections. If accepted, the process continues; if rejected, it returns to the setup stage for revision of prompts, templates, or criteria.  
- **Low-confidence mode:** Aggregates outputs from two additional LLMs to build an artificial consensus.  
- **High-confidence mode:** Combines one LLM’s output with human judgment.  

### **Final Report**  
Summarizes experiment outcomes by calculating performance metrics, including:  
- True Positives (TP)  
- False Positives (FP)  
- True Negatives (TN)  
- False Negatives (FN)  
- Accuracy and recall  

---

## 📊 Dataset  

This tool leverages the **[SESLR-Eval](https://arxiv.org/html/2507.19027v1)** dataset, which includes data from 14 peer-reviewed systematic reviews. This dataset provides a reliable foundation for controlled experimentation.  

---

🔗 [Access the online version of the system](https://csm-research.github.io/10-BM4LLM-SLR/support-system/public/)  

