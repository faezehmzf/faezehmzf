<img width="100%" alt="Faezeh Mozaffari" src="assets/banner.webp">

<p align="center">
  <a href="https://www.linkedin.com/in/faezeh-mozaffari-7816b6230/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:faezehxmozaffari@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>
  <!-- <a href="https://faezehmzf.github.io/"><img src="https://img.shields.io/badge/Portfolio-111827?style=flat-square&logo=githubpages&logoColor=white" alt="Portfolio"></a> -->
</p>

### Hi, I'm Faezeh

🎓 I hold an MSc in Information Technology Engineering from the **University of Tehran**, where I am also a Research Assistant at the **Social Networks Lab**. Our lab investigates computational approaches to understanding social networks, integrating **Network Science**, **Machine Learning**, and **Natural Language Processing** to study online behavior and information dynamics.

🔬 My research lies at the intersection of **Network Science and Machine Learning**, with a particular focus on **Community Detection and Evolution**, **Influence Analysis**, and **Information Diffusion** in large-scale social networks.

🚀 My broader research interests encompass **Graph Machine Learning and Representation Learning**, with an emphasis on modeling complex relational structures, capturing structural and temporal dependencies, and learning generalizable representations. Building on my experience with **Graph Neural Networks**, I am particularly interested in developing robust and scalable learning approaches for complex, structured, and evolving data across diverse domains.

---

### Selected work

<table>
<tr>
<td width="50%" valign="top">

**💬 [RAG chatbot for *Speech and Language Processing*](https://github.com/faezehmzf/slp3-rag-chatbot-langgraph)**<br>
**Goal:** a chatbot that answers questions about Jurafsky and Martin's *Speech and Language Processing* textbook from the book itself, and turns to web search or politely declines when the book does not cover the question.<br>
**Approach:** a LangGraph workflow sends each question to hybrid FAISS + BM25 search over the 640-page book, to web search, or to a fallback.<br>
**Result:** tested with Llama-3-70B, every test question reached the right source, and the answers stayed within the retrieved passages.<br>
<sub>`RAG` `LangGraph` `LLMs`</sub>

</td>
<td width="50%" valign="top">

**🔎 [Job–candidate ranking](https://github.com/faezehmzf/job-candidate-ranking)**<br>
**Goal:** rank the applicants for each job so that the best-fitting candidates come first.<br>
**Approach:** data cleaning, 51 job–candidate features, cross-validation grouped by job, and LightGBM and XGBoost ranking models.<br>
**Result:** NDCG@10 of 0.858 on the test set, compared with 0.424 for the same model without the engineered features.<br>
<sub>`data-mining` `learning-to-rank` `LightGBM`</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

**🏷️ [Semantic role labelling: tagging vs. generation](https://github.com/faezehmzf/srl-tagging-vs-generation)**<br>
**Goal:** semantic role labelling finds *who did what to whom* in a sentence. The project asks whether this works better by labelling each word, or by generating the answer to a question such as *"who accepted the offer?"*<br>
**Approach:** two taggers (BiLSTM-CRF, RoBERTa) and two generators (an RNN encoder–decoder, FLAN-T5), all scored with the same metric.<br>
**Result:** RoBERTa with a CRF layer is the strongest model (span F1 0.880). FLAN-T5 comes close (token F1 0.894 vs. 0.902), while the generator trained without pre-training falls far behind.<br>
<sub>`NLP` `PyTorch` `Transformers`</sub>

</td>
<td width="50%" valign="top">

**⚡ [Parameter-efficient fine-tuning](https://github.com/faezehmzf/roberta-peft-mnli)**<br>
**Goal:** measure how much accuracy is lost when, instead of updating all 355M weights of RoBERTa-large, only a small set of added weights is trained.<br>
**Approach:** full fine-tuning, LoRA and soft prompts on natural language inference (MultiNLI), with 1% of the training data on a single GPU.<br>
**Result:** LoRA reaches 81.6% while training 1.3% of the weights, but needs three epochs to get there. After one epoch, full fine-tuning is well ahead (74.6% vs. 52.6%), and the soft prompts did not learn.<br>
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

---

<p align="center">
  <sub>Happy to talk about social networks, graph learning or data mining — <a href="https://www.linkedin.com/in/faezeh-mozaffari-7816b6230/">LinkedIn</a> · <a href="mailto:faezehxmozaffari@gmail.com">email</a></sub>
</p>
