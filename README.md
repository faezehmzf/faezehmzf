<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img width="100%" alt="Faezeh Mozaffari — Social Network Analysis, Graph Neural Networks, Data Mining" src="assets/banner-light.svg">
</picture>

<p align="center">
  <a href="https://www.linkedin.com/in/faezeh-mozaffari-7816b6230/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:faezehxmozaffari@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>
  <!-- <a href="https://faezehmzf.github.io/"><img src="https://img.shields.io/badge/Portfolio-111827?style=flat-square&logo=githubpages&logoColor=white" alt="Portfolio"></a> -->
</p>

<sub><i>The banner is a small network: node size is PageRank, colours are communities, and the moving dot is a random surfer.</i></sub>

### Hi, I'm Faezeh

I hold an MSc in IT Engineering from the **University of Tehran** and am a research assistant in its **Social Networks Lab**. I study graphs and social networks: how communities form and change over time, which accounts drive the spread of information, and how graph neural networks can learn from network structure, text and time together.

My thesis models **the evolution of communities in dynamic, multi-relational social networks**. It is an unsupervised framework that combines GraphSAGE, masked attention, a GRU and transformer text embeddings to find communities in large networks and track them as they grow, split and merge.

- **Social network analysis** — community detection, centrality and influence, information diffusion
- **Graph learning** — graph neural networks, dynamic and multi-relational graphs, knowledge graphs
- **Data mining & machine learning** — classification, clustering, ranking, statistical analysis
- **Natural language processing** — text representations, transformers, LLM applications

---

### Selected work

<table>
<tr>
<td width="50%" valign="top">

**💬 [RAG chatbot over a textbook](https://github.com/faezehmzf/slp3-rag-chatbot-langgraph)**<br>
**Goal:** answer questions about an NLP textbook from the book itself, and know when to search the web or decline instead of guessing.<br>
An LLM router picks between hybrid FAISS + BM25 search over the book, web search and a fallback, built with LangGraph.<br>
<kbd>6 / 6 routed correctly</kbd> in a live run with Llama-3-70B<br>
<sub>`RAG` `LangGraph` `LLMs`</sub>

</td>
<td width="50%" valign="top">

**🔎 [Job–candidate ranking](https://github.com/faezehmzf/job-candidate-ranking)**<br>
**Goal:** rank each job's applicants so that the best-fitting candidates come first.<br>
Data cleaning, 51 job–candidate features, cross-validation grouped by job, and LightGBM and XGBoost ranking models.<br>
<kbd>NDCG@10 0.858</kbd> vs. 0.424 without feature engineering<br>
<sub>`data-mining` `learning-to-rank` `LightGBM`</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

**🏷️ [Semantic role labelling: tagging vs. generation](https://github.com/faezehmzf/srl-tagging-vs-generation)**<br>
**Goal:** find out whether "who did what to whom" is better extracted by tagging words or by generating answers to questions.<br>
BiLSTM-CRF and RoBERTa taggers against seq2seq and FLAN-T5 generators, compared with one metric.<br>
<kbd>span F1 0.880</kbd> with RoBERTa + CRF; FLAN-T5 is close behind<br>
<sub>`NLP` `PyTorch` `Transformers`</sub>

</td>
<td width="50%" valign="top">

**⚡ [Parameter-efficient fine-tuning](https://github.com/faezehmzf/roberta-peft-mnli)**<br>
**Goal:** test how close cheap fine-tuning methods get to full fine-tuning when only a small part of a large model is trained.<br>
Full fine-tuning, LoRA and soft prompts on RoBERTa-large for natural language inference (MultiNLI).<br>
<kbd>LoRA 81.6%</kbd> training only 1.3% of the weights<br>
<sub>`PEFT` `LoRA` `RoBERTa`</sub>

</td>
</tr>
</table>

<details>
<summary><b>More projects</b></summary>
<br>

| Area | Project | In one line |
|---|---|---|
| Social networks | [information-diffusion-network-analysis](https://github.com/faezehmzf/information-diffusion-network-analysis) | Influence (HITS, PageRank), k-cores and communities (Louvain, Infomap) in six retweet and forward networks |
| Graphs | [graph-ranking-and-text-weighting](https://github.com/faezehmzf/graph-ranking-and-text-weighting) | PageRank, HITS and SALSA on a voting network, checked against NetworkX; TF-IDF as a MapReduce job |
| Data mining | [bm25-vs-language-models](https://github.com/faezehmzf/bm25-vs-language-models) | Eleven text ranking models compared with cross-validation and significance tests |
| Machine learning | [spoken-language-identification](https://github.com/faezehmzf/spoken-language-identification) | Four-language identification from speech, evaluated on speakers the model has never heard |
| Machine learning | [life-expectancy-mlp](https://github.com/faezehmzf/life-expectancy-mlp) | Neural networks on WHO indicators, tested on countries the model has never seen |
| Statistics | [Pima-Diabetes-Stat-Inference](https://github.com/faezehmzf/Pima-Diabetes-Stat-Inference) | Estimation, hypothesis tests and regression on the Pima diabetes data |
| NLP | [tokenizers-and-ngram-lms](https://github.com/faezehmzf/tokenizers-and-ngram-lms) | Subword tokenizers and n-gram language models, tested against Hugging Face |
| NLP | [tfidf-ppmi-word2vec](https://github.com/faezehmzf/tfidf-ppmi-word2vec) | Count-based and skip-gram word vectors compared with GloVe |
| NLP | [english-persian-nmt-fairseq](https://github.com/faezehmzf/english-persian-nmt-fairseq) | English→Persian translation with fairseq: LSTM vs. Transformer |
| Optimisation | [Bio-CPG-Optimization](https://github.com/faezehmzf/Bio-CPG-Optimization) | A genetic algorithm that tunes a walking gait for a six-legged robot in Webots |

</details>

---

### Toolbox

<p>
  <img src="https://skillicons.dev/icons?i=py,cpp,c,matlab,mysql,pytorch,tensorflow,sklearn,django,git,github,latex&perline=12" alt="Python, C++, C, MATLAB, MySQL, PyTorch, TensorFlow, scikit-learn, Django, Git, GitHub, LaTeX">
</p>

**Graphs & networks** NetworkX · Gephi · Neo4j<br>
**Machine learning** PyTorch · TensorFlow · scikit-learn · Hugging Face<br>
**Data** pandas · NumPy · SQL · Tableau<br>
**LLM applications** LangChain · LangGraph<br>
**Software** Python · C++ · Django · Git

**Languages** English (fluent) · Korean (intermediate) · Persian (native)

---

<p align="center">
  <sub>Happy to talk about social networks, graph learning or data mining — <a href="https://www.linkedin.com/in/faezeh-mozaffari-7816b6230/">LinkedIn</a> · <a href="mailto:faezehxmozaffari@gmail.com">email</a></sub>
</p>
