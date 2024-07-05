# Knowledge Platform Comparison
## Comparative Study of Knowledge Platforms for Clinical Research

This comparative study analyses the databases and implementation methods of four knowledge platforms for clinical research:

*   **BIKG (Biological Insights Knowledge Graph):** Developed by AstraZeneca.
*   **TCRD (Target Central Resource Database) and Pharos:** Products of the Illuminating the Druggable Genome (IDG) project, an NIH initiative.
*   **Standigm ASK:** Developed by Standigm.
*   **AbbVie's Knowledge Graph ARCH:** Details are provided in a research paper from AbbVie. 

### Database Architectures

*   **BIKG:** Utilizes a hybrid database approach. The graph database technology is not specified in the source. It employs SOLR for text and BigQuery for structured data. This interconnected system links insights from subgraph analysis to source text and clinical trial data. 
*   **TCRD:** Sources do not explicitly state the database technology used. However, TCRD integrates data from 79 sources. It emphasizes data quality and documentation to ensure consistency and reliability across diverse datasets. 
*   **Standigm ASK:**  The specific database technology is not explicitly mentioned in the source.  Standigm ASK prioritizes data quality and documentation, drawing comparisons with other KGs like HetioNet, DRKG, BioKG, PharmKG, OpenBioLink, and Clinical Knowledge Graph in terms of information content and documentation quality. 
*   **AbbVie:** Leverages a hybrid database architecture combining graph databases, text format, and structured format data. This architecture allows for linking insights from subgraph analysis to source text (literature and patents) and comparisons with structured clinical trial data.

### Implementation Methods

*   **Data Sources and Integration:** 
    *   All four platforms rely on integrating data from multiple public and proprietary sources, including databases like ChEMBL, Ensembl, and Mondo; full-text publications; and internal experimental data.
    *   They employ entity recognition and resolution techniques to harmonize data from these diverse sources, mapping entities to standard ontologies like Uberon and Gene Ontology.
    *   **BIKG** uses ChEMBL identifiers as canonical for drug compounds, extending them with external (PubChem) and internal identifiers.
    *   **TCRD** harmonizes identifiers for targets, diseases, and ligands across its data sources.
    *   **AbbVie** harmonizes data from various public sources (both structured and unstructured) to common ontologies. 
*   **Knowledge Representation:** 
    *   All platforms employ a knowledge graph structure, representing biological entities and relationships as nodes and edges.
    *   **BIKG**'s schema utilizes an Upper-Level Ontology (ULO) designed to unify data from various sources and prioritize signal propagation for machine learning. 
    *   **Standigm ASK**  leverages heterogeneous KGs connecting multimodal data and employs metapaths to discover associations between nodes. 
    *   **AbbVie** focuses on specific subgraph patterns, particularly for representing drug-disease relationships.
*   **Data Analysis and Hypothesis Generation:**
    *   All platforms are designed to support machine learning applications for drug discovery tasks. They provide tools for data analysis, visualization, and hypothesis generation.
    *   **BIKG** is used for target identification and CRISPR recommendations, leveraging both internal and external data to train machine learning algorithms.
    *   **TCRD/Pharos** offers enrichment calculations, interactive heatmaps, and UpSet charts for analysing subsets of targets, diseases, or ligands.
    *   **Standigm ASK** prioritizes target genes using a five-criteria system considering biological relevance, disease causality, druggability, toxicity, and novelty. It uses QuatE as the Knowledge Graph Embedding (KGE) model. 
    *   **AbbVie** focuses on identifying drug-disease associations supported by genomic evidence. 

    

| Feature          | BIKG                                                                                      | AbbVie                                                                               | Standigm ASK                                                                      | TCRD                                                                                              |
|------------------|-------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| **Focus**        | Comprehensive drug discovery platform.                                                    | Drug repurposing and target prioritization using genomically-informed subgraphs.      | Identifying novel target genes for diseases.                                       | Aggregating information on protein targets, with an emphasis on understudied proteins.            |
| **Schema**       | Employs an Upper-Level Ontology (ULO) for data unification from diverse sources, prioritizing signal propagation for machine learning. | Focuses on subgraphs linking drugs to diseases via genes, with or without genetic evidence. | Leverages a heterogeneous KG connecting multimodal data and prioritizes targets using five criteria: biological relevance, disease causality, druggability, toxicity, and novelty. | Based on 'reviewed' (manually curated) human protein entries from UniProt. Data is organized using the Target Development Level (TDL) scheme, categorizing targets based on their level of development, and the Drug Target Ontology (DTO) for a formal classification and annotation of protein families. |
| **Database Structure** | Columnar data model using Parquet files, employing Spark for processing and Azure Blob storage for security. Offers BIKG, BROWSER, RDF, and Neo4j projections for varied user needs. | Hybrid approach combining a graph database with SOLR for text and BigQuery for structured data, interconnected for comprehensive analysis. | Specific database technology not mentioned, but emphasizes data quality and documentation, comparing itself to HetioNet, DRKG, BioKG, PharmKG, OpenBioLink, and Clinical Knowledge Graph. | Utilizes TCRD as the database and Pharos as the web interface for accessing and visualizing data. TCRD integrates data from various sources related to human genes and proteins. |
| **Implementation** | Focuses on a unified data model and flexibility, enabling user contributions and quick feedback incorporation. Employs a cloud-based pipeline for scalability. | Leverages NLP techniques like NER, BAR, SRQ, and CEC to extract information and build its knowledge graph. | Employs QuatE as the Knowledge Graph Embedding (KGE) model and utilizes metapaths to learn associations between nodes. | Provides a REST API for programmatic access and a web interface with features like free text search, sequence similarity search, batch search, data visualization, target ranking, target comparison, and target dossiers for a user-friendly experience. |

### Key Differences:
- **Scope and Purpose:** Each platform has a specific area of focus within drug discovery. BIKG aims for comprehensiveness, AbbVie emphasizes drug repurposing, Standigm ASK concentrates on target identification, and TCRD prioritizes understudied proteins.
- **Schema Design:** BIKG leverages a ULO for unified representation, AbbVie focuses on specific subgraph patterns, Standigm ASK uses a five-criteria system for target prioritization, and TCRD employs TDL and DTO for classification.
- **Database Specifics:** BIKG provides detailed information on its data model and technologies. AbbVie outlines a hybrid architecture. Standigm ASK focuses on data quality without specifying technology. TCRD's database specifics are not elaborated upon.


### Summary

While all four platforms share a common goal of leveraging knowledge graphs for drug discovery, they exhibit differences in their database architectures, data integration approaches, knowledge representation schemas, and specific areas of focus. 