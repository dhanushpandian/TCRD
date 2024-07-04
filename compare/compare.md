# Comparative Study of Knowledge Platforms for Biomedical NLP

## Introduction

Natural Language Processing (NLP) in biomedical literature is crucial for identifying biological entities and extracting relations from structured and unstructured text. This comparative study analyzes three knowledge platforms: Abbvie ARCH, BIKG, and Standigm ASK, focusing on their implementation and working mechanisms.

## Abbvie ARCH

### Overview
Abbvie ARCH uses NLP to extract associations between chemicals/drugs, target genes, proteins, and disease states from biomedical text, aiding drug discovery and repurposing.

### Methodology
1. **Subgraph Pattern Matching**:
   - Utilizes a multimodal knowledge graph built from structured and unstructured data harmonized to common ontologies.
   - Enriches drug-disease associations with direct or indirect genomic evidence.
   - Identifies genomically-informed subgraphs associating known drugs with novel diseases.

2. **Data Curation**:
   - Uses proprietary machine learning algorithms for:
     - Named Entity Recognition (NER)
     - Biomedical Ambiguity Resolution (BAR)
     - Semantic Relationship Quantification (SRQ)
     - Causal Context Expression Curation (CEC)

3. **SRQ Model**:
   - Transformer-style model pre-trained on a large multi-domain corpus of scientific text.
   - Fine-tuned on annotated data, providing confidence scores for semantic relationships.

4. **CEC**:
   - Processes directionality of entities in cause-and-effect relationships using syntactic dependency graphs.

### Database Architecture
- **Graph Database**: Stores graph data.
- **SOLR Database**: Manages text format data.
- **BigQuery**: Handles structured data.
- **Metadata Links**: Interconnect data across different formats for comprehensive analysis.

### Data Sources
- **Unstructured Text**: PubMed, PMC, bioRxiv, medRxiv, arXiv, Google Patents, NIH grants.
- **Structured Data**: HGNC, GWAS, dbSNP, CPDB.

### Applications
- **Drug-Repurposing**:
  - Identifies potential drug-repurposing candidates for rare diseases like Carney Complex.
- **Subgraph Utilization**:
  - DD3, DD4, DD5 subgraphs complement target validation by connecting genes to diseases and clinical activity of drug candidates.

### Conclusion
Abbvie ARCH demonstrates the potential of using a 911M edge knowledge graph for drug repurposing, emphasizing the role of NLP in enriching the knowledge graph with insights from unstructured biomedical text.

## BIKG

### Overview
BIKG focuses on a different approach, leveraging deep learning models for entity recognition and relation extraction from biomedical literature.

### Methodology
1. **Deep Learning Models**:
   - Utilizes BERT-based models fine-tuned on biomedical corpora for entity recognition.
   - Relation extraction using attention mechanisms to identify meaningful connections between entities.

2. **Data Integration**:
   - Merges structured data from databases like KEGG and Reactome with unstructured text from scientific publications.

3. **Model Training**:
   - Trains models on large annotated datasets to improve accuracy and reliability.

### Database Architecture
- **Relational Database**: Stores structured data.
- **NoSQL Database**: Manages unstructured text data.
- **Integration Layer**: Connects data sources for unified access and analysis.

### Data Sources
- **Unstructured Text**: Scientific publications, patents.
- **Structured Data**: KEGG, Reactome, UniProt.

### Applications
- **Target Identification**:
  - Identifies new drug targets by analyzing connections between genes, proteins, and diseases.
- **Drug Interaction Analysis**:
  - Examines potential drug interactions and side effects by correlating data from multiple sources.

### Conclusion
BIKG showcases the effectiveness of deep learning models in biomedical NLP, enhancing the integration of structured and unstructured data for comprehensive analysis.

## Standigm ASK

### Overview
Standigm ASK employs a hybrid approach, combining rule-based systems with machine learning for text mining and knowledge extraction.

### Methodology
1. **Rule-Based Systems**:
   - Applies predefined rules for initial entity recognition and relation extraction.
   - Utilizes machine learning models for refining and validating extracted data.

2. **Hybrid Model**:
   - Combines rule-based methods with supervised learning to improve accuracy and reduce false positives.

3. **Data Processing**:
   - Processes data through multiple stages, including normalization, validation, and integration.

### Database Architecture
- **Graph Database**: Stores relationships and entities.
- **Document Database**: Manages unstructured text data.
- **Data Warehouse**: Aggregates structured data for analysis.

### Data Sources
- **Unstructured Text**: Medical literature, clinical trial reports.
- **Structured Data**: DrugBank, OMIM, ClinicalTrials.gov.

### Applications
- **Clinical Decision Support**:
  - Provides insights for clinical decision-making by correlating patient data with biomedical knowledge.
- **Disease Ontology Mapping**:
  - Maps diseases to genetic and molecular pathways for better understanding of disease mechanisms.

### Conclusion
Standigm ASK demonstrates the utility of a hybrid approach in biomedical NLP, leveraging both rule-based systems and machine learning for robust knowledge extraction.

## Comparative Analysis

| Feature/Aspect              | Abbvie ARCH                      | BIKG                                    | Standigm ASK                         |
|-----------------------------|----------------------------------|-----------------------------------------|--------------------------------------|
| **Approach**                | NLP with subgraph pattern matching | Deep learning models                     | Hybrid rule-based and machine learning|
| **Entity Recognition**      | NER, BAR, SRQ, CEC               | BERT-based models                        | Rule-based initial recognition       |
| **Data Integration**        | Multimodal knowledge graph       | Structured and unstructured integration  | Multiple-stage processing            |
| **Database Architecture**   | Graph DB, SOLR, BigQuery         | Relational DB, NoSQL                     | Graph DB, Document DB, Data Warehouse|
| **Applications**            | Drug-repurposing, Target validation | Target identification, Drug interaction | Clinical decision support, Disease mapping|
| **Data Sources**            | PubMed, PMC, HGNC, GWAS, etc.    | KEGG, Reactome, UniProt                  | DrugBank, OMIM, ClinicalTrials.gov   |
| **Strengths**               | Enriched drug-disease associations | Effective deep learning for NLP          | Robust knowledge extraction          |
| **Challenges**              | Complex database management      | Requires large annotated datasets        | Balancing rule-based and ML approaches|

## Conclusion

Each platform presents unique strengths and challenges in the realm of biomedical NLP. Abbvie ARCH excels in enriching drug-disease associations through subgraph pattern matching, BIKG leverages deep learning for precise entity recognition, and Standigm ASK employs a hybrid approach for robust knowledge extraction. Together, these platforms showcase the diverse methodologies driving advancements in biomedical research and drug discovery.
