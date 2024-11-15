import utils
from optparse import OptionParser
import os
import compress_pickle as pickle
from tqdm import tqdm
import multiprocessing as mp
save_loc="/scratch/github/data"

patents_save_loc="/scratch/github/data"
data_dir="/scratch/github/data"
num_papers=-1

if not os.path.exists(os.path.join(save_loc, 'cvpr_patents_graph_crawl_list.lz4')):
    loaded_dict=utils.load_mag(data_dir, n_papers=num_papers)
    cvpr_graph=pickle.load(open(os.path.join(data_dir, f'cvpr_graph_-1.lz4'), 'rb'))

    ''' Save list of patents directly citing papers from conferences.

    args:
        loaded_dict: dict of MAG dataframes from load_mag
        subgraph: subgraph with MAGS to get patents for in keys
    returns:
        patents, dict MAG : citing patents and metadata
    '''



    subgraph=cvpr_graph
    all_mags=list(subgraph.keys())
    for patents in list(subgraph.values()):
        all_mags+=patents
    all_mags=set(all_mags)
    print(f'len(all_mags) {len(all_mags)}')
    papers_patents=loaded_dict['_pcs_mag_doi_pmid.tsv']
    print(f'{len(papers_patents)} paper patent linkages loaded')
    papers_patents_old=loaded_dict['_pcs.tsv']
    paper_to_patent={}
    patents=[]

    for row_ind in tqdm(range(len(papers_patents))):
        # https://onlinelibrary.wiley.com/doi/10.1111/jems.12455 Table 1, 0.63% error
        paper_mag=str(papers_patents['magid'][row_ind])
        if paper_mag in all_mags:
            patent_id=str(papers_patents['patent'][row_ind])
            if paper_mag not in paper_to_patent:
                paper_to_patent[paper_mag]=[patent_id]
            else:
                paper_to_patent[paper_mag].append(patent_id)
            patents.append(patent_id)

    for row_ind in tqdm(range(len(papers_patents_old))):
        paper_mag=str(papers_patents_old['magid'][row_ind])
        if paper_mag in all_mags:
            patent_id=str(papers_patents_old['patent'][row_ind])
            if paper_mag not in paper_to_patent:
                paper_to_patent[paper_mag]=[patent_id]
            else:
                paper_to_patent[paper_mag].append(patent_id)
            patents.append(patent_id)

    # Get list of unique patents
    patents_list=list(set(patents))

    pickle.dump(patents_list, open(os.path.join(save_loc, 'cvpr_patents_graph_crawl_list.lz4'), 'wb'))
else:
    patents_list=pickle.load(open(os.path.join(save_loc, 'cvpr_patents_graph_crawl_list.lz4'), 'rb'))
    
print(f'downloading {len(patents_list)} patents')

# Get metadata for all patents

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

patents_info_save_loc=os.path.join(save_loc, 'patents')
all_parallel_runs=[]
patents_scraped_info={}

scrape_args=[]
for patent in tqdm(patents_list):
    #patents_scraped_info.update(utils.scrape_patents([patent], patents_save_loc))
    scrape_args.append(([patent], patents_save_loc, False, True))

# # for i in range(10):
# #     utils.scrape_patents(scrape_args[i])
    
# with ThreadPoolExecutor(max_workers=80) as p:
#     results=p.map(utils.scrape_patents, scrape_args)
#     print(f'len(results {len(results)}')
#     for result in tqdm(results):
#         u=0
        
with Pool(processes=64) as pool, tqdm(total=len(scrape_args)) as pbar: # create Pool of processes (only 2 in this example) and tqdm Progress bar
    for data in pool.imap_unordered(utils.scrape_patents, scrape_args):                   # send urls from all_urls list to parse() function (it will be done concurently in process pool). The results returned will be unordered (returned when they are available, without waiting for other processes)
        pbar.update() 

        
#patents_scraped_info=utils.scrape_patents(patents_list)


# patents_info_csv=[['patent_id',
#                    'title',
#                    'inventor_name',
#             'assignee_name_orig',
#             'assignee_name_current',
#             'pub_date',
#             'priority_date',
#             'grant_date',
#             'filing_date',
#             'abstract_text',
#             'patent_full_url']]


# scrapped_succesfully=0
# for patent_id in patents_scraped_info:
#     patent_info=patents_scraped_info[patent_id]
#     # patent_pdf=requests.get()



#     # with open(, 'w') as f:
#     #     f.write(patent_pdf)
#     if 'title' in patent_info:
#         scrapped_succesfully+=1
#         patent_info_row=[patent_id, patent_info['title'], patent_info['inventor_name'], patent_info['assignee_name_orig'], patent_info['assignee_name_current'],
#                          patent_info['pub_date'], patent_info['priority_date'], patent_info['grant_date'], patent_info['filing_date'],
#                          patent_info['abstract_text'], patent_info['patent_full_url'], patent_info['classification_code_descss'], patent_info['patent_text']] 
#     patents_info_csv.append(patent_info_row )

print(f'saved {len(patents_info_csv)} patents')

# with open(os.path.join(save_loc, patents_file_name+'_patents_metadata.tsv'), 'w', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_ALL)
#     csvwriter.writerows(patents_info_csv)
