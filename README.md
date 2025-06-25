# Computer Vision Research Powers Surveillance Technology

## Abstract

An increasing number of scholars, policymakers and grassroots communities argue that artificial intelligence (AI) research—and computer-vision research in particular has become the primary source for developing and powering mass surveillance. Yet, the pathways from computer vision to surveillance continue to be contentious. Here we present an empirical account of the nature and extent of the surveillance AI pipeline, showing extensive evidence of the close relationship between the field of computer vision and surveillance. Through an analysis of computer-vision research papers and citing patents, we found that most of these documents enable the targeting of human bodies and body parts. Comparing the 1990s to the 2010s, we observed a fivefold increase in the number of these computer-vision papers linked to downstream surveillance-enabling patents. Additionally, our findings challenge the notion that only a few rogue entities enable surveillance. Rather, we found that the normalization of targeting humans permeates the field. This normalization is especially striking given patterns of obfuscation. We reveal obfuscating language that allows documents to avoid direct mention of targeting humans, for example, by normalizing the referring to of humans as ‘objects’ to be studied without special consideration. Our results indicate the extensive ties between computer-vision research and surveillance.

## Overview of data & analysis

We use several datasets in this project:

1) [Microsoft Academic Graph (MAG)](https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/). Contains paper citations, paper authors, author affiliations, and lots of other info related to papers.

2) [Paper-patent citations](https://onlinelibrary.wiley.com/doi/10.1111/jems.12455). Contains linkages between MAG paper IDs and patent IDs.

3) Patents. Scrapped from Google Patents.

We use this corpus to conduct large-scale lexicon-based analysis and in-depth manual content analysis. The project data and code is described here.


## Setup

Prerequisites: [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) and [git](https://github.com/git-guides/install-git)

`git clone https://github.com/wagnew3/Computer-Vision-Research-Powers-Surveillance-Technology.git whatisai`

`cd whatisai`

`conda env create -f environment.yml`

`conda activate whatisai`

Installation may take 1-3 hours to download and compile required packages.



## Conducting the large-scale lexicon-based analysis
The code to conduct the data scraping, processing, and overall analysis is located in the `src` directory. The code to conduct the analysis stratified by institutions, fields, countries, and years is located in the `analysis-plots` directory.
Questions regarding MAG, scraping, and overall analysis can be directed to William Agnew (wagnew at andrew.cmu.edu).

### Data
Change to directory you want data in (found [here](https://s3.console.aws.amazon.com/s3/buckets/openalex-mag-format?region=us-east-1&tab=objects), will be about 100GB)


`wget https://zenodo.org/record/5803985/files/_pcs_mag_doi_pmid.tsv
https://openalex-mag-format.s3.amazonaws.com/data_dump_v1/2022-04-07/mag/Affiliations.txt
https://openalex-mag-format.s3.amazonaws.com/data_dump_v1/2022-04-07/mag/PaperAuthorAffiliations.txt
https://openalex-mag-format.s3.amazonaws.com/data_dump_v1/2022-04-07/mag/PaperReferences.txt
https://openalex-mag-format.s3.amazonaws.com/data_dump_v1/2022-04-07/mag/Papers.txt
https://openalex-mag-format.s3.amazonaws.com/data_dump_v1/2022-04-07/advanced/FieldsOfStudy.txt
https://openalex-mag-format.s3.amazonaws.com/data_dump_v1/2022-04-07/advanced/PaperFieldsOfStudy.txt`

### Code

These datasets are very large. As such the code has multiple stages to preprocess them, and saves/loads checkpoints to disk to enable restarting. Processing the data from scratch can take up to 24 hours of compute time. Different stages of preprocessed data are used to generate different graphs and numbers. The analysis-plots folder contains preprocessed datasets that can be loaded on a laptop and code to generate the plots in the paper.

#### ♦ MAG Data Processing Pipeline
To see this data processing pipeline in use, see _save_ml_graphs.py_.

1) Saved on disk: Raw MAG.
2) Save MAG in a compressed and faster to load format. *utils.load_mag* saves a pickled and compressed dict of pandas dataframes of a subset of MAG files as f"cached_{n_rows}.lz4", where n_rows is the number of rows to load for each MAG files.
3) Create dictionaries to allow deduplication of MAG IDs. Some papers have several versions (conference and arxiv, for example). To handle this, create dictionaries that map each MAG ID onto every other mag ID that shares the same paper title and MAG author IDs. We do this by running *utils.make_title_date_to_dup_mags*
4) Make citation graph. *utils.make_mag_graph*

Once the raw data is processed into pandas dataframes, the paper MAG deduplication dictionary is created, and the paper citation graph is created, we can start using the data to answer questions. For example, *utils.get_conferences_subgraph* returns a subgraph of the paper citation graph that is all papers beloning to a particular set of conferences, and all papers citing those papers to a certain citation depth.

#### ♦ Patent Scraping Pipeline

1) *save_ml_patents.py:* From raw MAG data and patent-paper linkages computes patents citing papers from a particular set of conferences and saves as 'patents_file_name+'_patents_metadata.tsv''
2) *scrape_patents.py*: scrapes data on a list of patents (*patents_file_name+'_patents_metadata.tsv'*)--abstracts, organizations, dates, authors, patent pdfs, etc--and saves as 'patents_file_name+'_patents_scraped_info.p''

#### ♦ Analysis

* *analysis-plots*: This directory contains code to perform all analysis of papers and patents and all plots presented in the paper. Specifically, *lexicon-based-analysis.ipynb* contains code to conduct analysis across years, decades, institutions, countries, and subfields.
* *analyze_ml_graphs.py*: This supplementary code analyzes preprocessed citation graphs.
* *make_patent_metadata_plots*: This supplementary code makes additional plots from scraped patent data. Includes plots showing additional analysis of institution patent counts, keyword frequency, and simple NLP keyword extraction.  



## Conducting the in-depth manual content analysis
The data and code to conduct this analysis are located in the `analysis-plots` directory. Questions can be directed to Pratyusha Ria Kalluri (pkalluri at stanford.edu) or Abeba Birhane (birhanea at tcd.ie).

### Data
The randomly sampled set of 100 papers and 100 patents is included, along with the corresponding manual annotations, in `data/manual_papers_coding.csv` and  `data/manual_patents_coding.csv`.

### Code
The code to generate statistics and plots from these annotations is included in `content-analysis.ipynb`.


## Corresponding authors

Correspondence and requests for materials can be addressed to Pratyusha Ria Kalluri (pkalluri at stanford.edu), William Agnew (wagnew at andrew.cmu.edu), or Abeba Birhane (birhanea at tcd.ie).
