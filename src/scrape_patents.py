import utils
import csv
import pandas as pd
import requests
import pickle
import os
import multiprocessing as mp
from tqdm import tqdm
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--save_loc", dest="save_loc", default='/media/ssd_1000/microsoft_academic_graph/CVPR_patents')
    parser.add_option("--patents_list", dest="patents_list", default='/media/ssd_1000/microsoft_academic_graph/cvpr_patents.csv')
    parser.add_option("--num_processes", type="int", dest="num_processes", default=12)
    (options, args) = parser.parse_args()
    print(options)
    
    patents_file_name=options.patents_list.split("/")[-1]
    
    patents_save_loc=os.path.join(options.save_loc, "patents_pdfs")
    patents_info_save_loc=os.path.join(options.save_loc, patents_file_name+'_patents_scraped_info.p')
    if not os.path.exists(patents_save_loc):
        os.mkdir(patents_save_loc)

    
    rows=[]
    with open(options.patents_list, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            rows.append(row)
    u=0
    patents_list=[rows[i][0] for i in range(len(rows))]#[:5] #
    
    # multithreaded
    all_parallel_runs=[]
    patents_scraped_info={}
    pool = mp.Pool(processes=options.num_processes, maxtasksperchild=1)
    for patent in patents_list:
        #patents_scraped_info.update(utils.scrape_patents([patent], patents_save_loc))
        run=pool.apply_async(utils.scrape_patents, args=([patent], patents_save_loc))
        all_parallel_runs.append(run)
    
    
    for run in tqdm(all_parallel_runs):
        patents_scraped_info.update(run.get())
    
    
    #patents_scraped_info=utils.scrape_patents(patents_list)
    
    
    patents_info_csv=[['patent_id',
                       'title',
                       'inventor_name',
                'assignee_name_orig',
                'assignee_name_current',
                'pub_date',
                'priority_date',
                'grant_date',
                'filing_date',
                'abstract_text',
                'patent_full_url']]

    
    scrapped_succesfully=0
    for patent_id in patents_scraped_info:
        patent_info=patents_scraped_info[patent_id]
        # patent_pdf=requests.get()
        
       
        
        # with open(, 'w') as f:
        #     f.write(patent_pdf)
        if 'title' in patent_info:
            scrapped_succesfully+=1
            patent_info_row=[patent_id, patent_info['title'], patent_info['inventor_name'], patent_info['assignee_name_orig'], patent_info['assignee_name_current'],
                             patent_info['pub_date'], patent_info['priority_date'], patent_info['grant_date'], patent_info['filing_date'],
                             patent_info['abstract_text'], patent_info['patent_full_url'], patent_info['classification_code_descss']] 
        patents_info_csv.append(patent_info_row )
        
        
    pickle.dump((patents_scraped_info, scrapped_succesfully/len(patents_scraped_info)), open(patents_info_save_loc, 'wb'))
    with open(os.path.join(options.save_loc, patents_file_name+'_patents_metadata.tsv'), 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_ALL)
        csvwriter.writerows(patents_info_csv)
            