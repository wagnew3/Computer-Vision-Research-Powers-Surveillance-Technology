# CVPR and the rise of Surveillance AI

## Overview

We use several datasets in this project:

1) [Microsoft Academic Graph (MAG)](https://docs.microsoft.com/en-us/academic-services/graph/reference-data-schema). Containts paper citations, paper authors, author affiliations, and lots of other info related to papers.

2) [Paper-patent citations](https://onlinelibrary.wiley.com/doi/10.1111/jems.12455). Contains linkages between MAG paper IDs and patent IDs.

3) Patents. Scrapped from Google Patents.

## Installation
Prerequisites: [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) and [git](https://github.com/git-guides/install-git)

`git clone git@github.com:wagnew3/whatisai.git`

`cd whatisai`

`conda env create -f environment.yml`

`conda activate whatisai`

Installation may take 1-3 hours to download and compile required packages.

### Data Download
Change to directory you want data in (will be about 100GB)

https://s3.console.aws.amazon.com/s3/buckets/openalex-mag-format?region=us-east-1&tab=objects

`wget https://zenodo.org/record/5803985/files/_pcs_mag_doi_pmid.tsv
https://openalex-mag-format.s3.amazonaws.com/data_dump_v1/2022-04-07/mag/Affiliations.txt
https://openalex-mag-format.s3.amazonaws.com/data_dump_v1/2022-04-07/mag/PaperAuthorAffiliations.txt
https://openalex-mag-format.s3.amazonaws.com/data_dump_v1/2022-04-07/mag/PaperReferences.txt
https://openalex-mag-format.s3.amazonaws.com/data_dump_v1/2022-04-07/mag/Papers.txt
https://openalex-mag-format.s3.amazonaws.com/data_dump_v1/2022-04-07/advanced/FieldsOfStudy.txt
https://openalex-mag-format.s3.amazonaws.com/data_dump_v1/2022-04-07/advanced/PaperFieldsOfStudy.txt'

## Code Overview

These datasets are very large. As such the code has multiple stages to preprocess them, and saves/loads checkpoints to disk to enable restarting. Processing the data from scratch can take up to 24 hours of compute time. Different stages of preprocessed data are used to generate different graphs and numbers. The analysis-plots folder contains preprocessed datasets that can be loaded on a laptop and code to generate many of the plots in the paper.

### MAG Data Processing Pipeline
To see this pipeline in use, look at save_ml_graphs.py.

Saved on disk: Raw MAG.
1) Save MAG in a compressed and faster to load format. *utils.load_mag*, saves a pickled and compressed dict of pandas dataframes of a subset of MAG files as f"cached_{n_rows}.lz4", where n_rows is the number of rows to load for each MAG files.
2) Create dictionaries to allow deduplication of MAG IDs. Some papers have several versions (conference and arxiv, for example). To handle this, create dictionaries that map each MAG ID onto every other mag ID that shares the same paper title and MAG author IDs. We do this by running *utils.make_title_date_to_dup_mags*
3) Make citation graph. *utils.make_mag_graph*
4) analyze_ml_graphs.py code to analyze preprocessed citation graphs, still incomplete.

Once the raw data is processed into pandas dataframes, the paper MAG deduplication dictionary is created, and the paper citation graph is created, we can start using the data to answer questions. For example, *utils.get_conferences_subgraph* returns a subgraph of the paper citation graph that is all papers beloning to a particular set of conferences, and all papers citing those papers to a certain citation depth.

### Patent Scraping Pipeline

1) *save_ml_patents.py* From raw MAG data and patent-paper linkages computes patents citing papers from a particular set of conferences and saves as 'patents_file_name+'_patents_metadata.tsv''
2) *scrape_patents.py*: scrapes data on a list of patents (*patents_file_name+'_patents_metadata.tsv'*)--abstracts, organizations, dates, authors, patent pdfs, etc--and saves as 'patents_file_name+'_patents_scraped_info.p''
3) *make_patent_metadata_plots.py*: produces plots from 'patents_file_name+'_patents_scraped_info.p''

### Code Outline

*analyze_ml_graphs.py* code to analyze preprocessed citation graphs.  
*analysis/* directory containing code to perform all analysis of papers and patents and generate all plots used in the paper. Includes analysis across years, decades, institutions, countries, and subfields.  
*make_patent_metadata_plots* code for making additional plots from scraped patent data. Includes plots showing additional analysis of institution patent counts, keyword frequency, and simple NLP keyword extraction.  
*save_ml_graphs.py* code for processing MAG data into conference citation subgraphs.  
*save_ml_patents.py* code for processing MAG data into csv of patents citing papers from particular set of conferences.  
*scrape_patents.py* code for scraping data on set of patents produced by running *save_ml_patents.py*  
*utils.py* most of code for various processing steps, will be split apart soon for clarity.  
*run_save_ml_graphs.sh* and *run_save_ml_patents.sh* scripts for running code on UW CSE servers.  
