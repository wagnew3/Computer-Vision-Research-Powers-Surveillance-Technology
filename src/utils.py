import pandas as pd
import os
import compress_pickle as pickle
from tqdm import tqdm
#import snap
import numpy as np
import json
from google_patent_scraper.main import scraper_class
import urllib.request
import math
import time
import csv

def load_mag(mag_path, n_papers=250000, load_refs=True):
    ''' Load microsoft academic graph tsvs into dict of pandas dfs.
    
    args:
        mag_path: path to folder containing MAG tsvs
        n_papers: int, max number papers to load, keep low unless you have lots of RAM
        
    returns:
        loaded: dict of dataframes for mag files
    '''
    
    # Names for columns in MAG csvs
    col_names={
        'Affiliations.txt':['AffiliationId', 'Rank','NormalizedName', 'DisplayName', 'GridId', 'OfficialPage', 'WikiPage', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'Iso3166Code', 'Latitude', 'Longitude', 'CreatedDate'],
        'Authors.txt': ['AuthorId', 'Rank', 'NormalizedName', 'DisplayName', 'LastKnownAffiliationId', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate'],
        #'ConferenceInstances.txt':['ConferenceInstanceId', 'NormalizedName', 'DisplayName', 'ConferenceSeriesId', 'Location', 'OfficialUrl', 'StartDate', 'EndDate', 'AbstractRegistrationDate', 'SubmissionDeadlineDate', 'NotificationDueDate', 'FinalVersionDueDate', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'Latitude', 'Longitude', 'CreatedDate' ],
        #'ConferenceSeries.txt': ['ConferenceSeriesId', 'Rank', 'NormalizedName', 'DisplayName', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate'],
        'FieldsOfStudy.txt': ['FieldOfStudyId', 'Rank', 'NormalizedName', 'DisplayName', 'MainType', 'Level', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate'],
        #'Journals.txt':['ConferenceSeriesId', 'Rank', 'DisplayName', 'Issn', 'Publisher', 'Webpage', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate'],
        'PaperAuthorAffiliations.txt': ['PaperId', 'AuthorId', 'AffiliationId'],#, 'AuthorSequenceNumber', 'OriginalAuthor', 'OriginalAffiliation'],
        'PaperFieldsOfStudy.txt': ['PaperId', 'FieldOfStudyId', 'Score'],
        #'PaperReferences.txt': {'PaperId': pd.Int64Dtype(), 'PaperReferenceId': pd.Int64Dtype()},
        #'PaperResources.txt':['PaperId', 'ResourceType', 'ResourceUrl', 'SourceUrl', 'RelationshipType'],
        'Papers.txt': {'PaperId': pd.Int64Dtype(), 
                       #'Rank': pd.Int64Dtype(), 
                       #'Doi': str, 
                       #'DocType': str, 
                       #'Genre': str, 
                       #'IsParatext': str,
                       'PaperTitle': str, 
                       #'OriginalTitle': str, 
                       #'BookTitle': str, 
                       'Year': pd.Int64Dtype(), 
                       #'Date': str,
                       #'OnlineDate': str, 
                       #'Publisher': str, 
                       'JournalId':pd.Int64Dtype(), 
                       'ConferenceSeriesId':pd.Int64Dtype(),
                       'ConferenceInstanceId':pd.Int64Dtype(), 
                       #'Volume': str, 
                       #'Issue': str, 
                       #'FirstPage': str, 
                       #'LastPage': str,
                       #'ReferenceCount': pd.Int64Dtype(), 
                       'CitationCount': pd.Int64Dtype(), 
                       #'EstimatedCitation': pd.Int64Dtype(), 
                       #'OriginalVenue': pd.Int64Dtype(),
                       #'FamilyId':pd.Int64Dtype(), 
                       #'FamilyRank':pd.Int64Dtype(), 
                       #'DocSubTypes': str, 'OaStatus': str, 
                       #'BestUrl': str,
                       #'BestFreeUrl': str, 
                       #'BestFreeVersion': str, 
                       #'DoiLower': str, 
                       #'CreatedDate': str,
                       #'UpdatedDate': str
                       },
        '_pcs_mag_doi_pmid.tsv': {'reftype':pd.Int64Dtype(), 'confscore':pd.Int64Dtype(), 'magid':pd.Int64Dtype(), 'patent':str, 'uspto':str, 'wherefound':str, 'doi':str, 'pmid':str},
        '_pcs.tsv':{'reftype':str, 'confscore':pd.Int64Dtype(), 'magid':pd.Int64Dtype(), 'patent':str}
        }
    
    # # Names for columns in reliance on science mag data
    # col_names={
    #     '_pcs_mag_doi_pmid.tsv': ['reftype', 'confscore', 'magid', 'patent', 'uspto', 'wherefound', 'doi', 'pmid', 'Name'],
    #     'paperauthoridaffiliationname.tsv': ['paperid', 'authorid', 'affiliationame'],
    #     'paperauthororder.tsv': ['paperid', 'authorid', 'authororder'],
    #     'papercitations.tsv': ['citingpaperid', 'citedpaperid'],
    #     'paperconferenceid.tsv': ['paperid', 'ConferenceSeriesId'],
    #     'paperjournalid.tsv': ['paperid', 'JournalId'],
    #     'PaperTitle.tsv': ['paperid', 'PaperTitle'],
    #     'Year.tsv': ['paperid', 'Year']
    #     }

    loaded={}
    mag_files=os.listdir(mag_path)
    mag_files.remove('Authors.txt')
    mag_files=['Authors.txt']+mag_files
    for file in tqdm(mag_files):
        if file[-3:] in ["txt", "tsv"] and file in col_names:
            print(f"loading {file}")
            cached_file=os.path.join(mag_path, f"cached_{file[:-4]}_{n_papers}.lz4")
            if os.path.isfile(cached_file):
                print(f'loading from cached file {cached_file}')
                loaded[file]=pickle.load(open(cached_file, "rb"))
            else:
            
                file_path=os.path.join(mag_path, file)
                # Only read some cols, too large for memory otherwise
                if file=='Papers.txt':
                    df=pd.read_csv(file_path, usecols=[0,6,9,13,14,15], sep='\t', on_bad_lines='skip', nrows=(n_papers if n_papers>-1 else None), dtype=str)
                elif file=='PaperAuthorAffiliations.txt':
                    df=pd.read_csv(file_path, usecols=[0,1,2], sep='\t', on_bad_lines='skip', nrows=(n_papers if n_papers>-1 else None), dtype=str)
                elif file=='Authors.txt':
                    df=pd.read_csv(file_path, sep='\t', on_bad_lines='skip', nrows=(n_papers if n_papers>-1 else None), dtype=str, quoting=csv.QUOTE_NONE)
                else:
                    df=pd.read_csv(file_path, sep='\t', on_bad_lines='skip', nrows=(n_papers if n_papers>-1 else None), dtype=str)
                loaded[file]=df
                print(f"loaded {file}")
                print(f"saving as {cached_file}")
                pickle.dump(df, open(cached_file, 'wb'), compression="lz4")
    print("loaded mag")
    return loaded

def list_to_str(list):
    string=""
    for l in list:
        string+=str(l)+"\t"
    return string

def str_to_list(string):
    parts=string.split("\t")
    return parts

def cache_graph_progress(mag_path, mag_graph, verts_row, edges_row, num_papers, paper_id_to_v_ind, edges):
    cached_file=os.path.join(mag_path, f"cached_graph_progress_{num_papers}.p")
    pickle.dump((mag_graph, verts_row, edges_row, paper_id_to_v_ind, edges), open(cached_file, 'wb'), compression=None)
    print(f"Saved graph creation progress {verts_row} nodes {edges_row} edges")
    
def restore_cache_graph_progress(mag_path, num_papers):
    if os.path.exists(os.path.join(mag_path, f"cached_graph_progress_{num_papers}.p")):
        cached_file=os.path.join(mag_path, f"cached_graph_progress_{num_papers}.p")
        mag_graph, verts_row, edges_row, paper_id_to_v_ind, edges=pickle.load(open(cached_file, 'rb'), compression=None)
        print(f"Restored graph creation progress {verts_row} nodes {edges_row} edges")
        return mag_graph, verts_row, edges_row, paper_id_to_v_ind, edges
    else:
        return {}, 0, 0, {}, []

# def get_paper_id(papers, ind):
#     return 

def get_dedup_key(mag_id, title, papers, new_paper_authors_dict):
    if mag_id in new_paper_authors_dict:
        authors_ids=new_paper_authors_dict[mag_id]
        key=title+"|"+authors_ids
        return key
    else:
        #print(f"{mag_id} not in new_paper_authors_dict!")
        return mag_id

def make_title_date_to_dup_mags(loaded_dict, mag_path):
    ''' Make a dict to match duplicated MAG entities matching titles and years.
    
    args:
        loaded_dict: dict of MAG dataframes from load_mag
    returns:
        title_date_to_dup_mags: dict of title.lower() and year strings to lists of MAG IDs
        mag_to_dup_mags: mag to list of duplicat MAG IDs
    '''
    
    print('making title year disambiguation dict')
    
    
    
    papers=loaded_dict["Papers.txt"]
    paper_authors=loaded_dict['PaperAuthorAffiliations.txt']
    cached_file=os.path.join(mag_path, f"cached_title_date_to_dup_mags_{len(papers)}.lz4")
    if os.path.isfile(cached_file):
        print(f"found cached file {cached_file}")
        title_date_to_dup_mags, mag_to_dup_mags, new_paper_authors_dict=pickle.load(open(cached_file, "rb"))
    else:
        print(f"cannot find cached file {cached_file}")
        paper_authors_dict={}
        for paper_ind in tqdm(range(len(paper_authors))):
            mag_id=str(paper_authors['PaperId'][paper_ind])
            author_id=str(paper_authors['AuthorId'][paper_ind])
            if mag_id not in paper_authors_dict:
                paper_authors_dict[mag_id]=[author_id]
            else:
                paper_authors_dict[mag_id].append(author_id)
        new_paper_authors_dict={}
        for mag_id in tqdm(paper_authors_dict):
            authors=paper_authors_dict[mag_id]
            authors.sort()
            new_paper_authors_dict[mag_id]=' '.join(authors)
        title_date_to_dup_mags={}
        mag_to_dup_mags={}
        for paper_ind in tqdm(range(len(papers))):
            title=str(papers['PaperTitle'][paper_ind]).lower()
            mag_id=str(papers['PaperId'][paper_ind])
            key=get_dedup_key(mag_id, title, papers, new_paper_authors_dict)
            if title=='normalizing flows an introduction and review of current methods':
                print(f'normalizing flows an introduction and review of current methods key {key}')
            if key in title_date_to_dup_mags:
                title_date_to_dup_mags[key].append(mag_id)
            else:
                title_date_to_dup_mags[key]=[mag_id]
                
        for paper_ind in tqdm(range(len(papers))):
            title=str(papers['PaperTitle'][paper_ind]).lower()
            mag_id=str(papers['PaperId'][paper_ind])
            key=get_dedup_key(mag_id, title, papers, new_paper_authors_dict)
            mag_to_dup_mags[mag_id]=title_date_to_dup_mags[key]
        
        pickle.dump((title_date_to_dup_mags, mag_to_dup_mags, new_paper_authors_dict), open(cached_file, 'wb'), compression="lz4")
    print('end title year disambiguation dict')
    return title_date_to_dup_mags, mag_to_dup_mags, new_paper_authors_dict

def make_mag_graph(loaded_dict, mag_path):
    ''' Make a graph from loaded mag data. 
    
    args:
        loaded_dict: dict of MAG dataframes from load_mag
    returns:
        mag_graph: graph_tool graph of papers and citations
        paper_id_to_v_ind: dict of MAG id: graph vertex number
    '''
    
    
    
    papers_patents=loaded_dict['_pcs_mag_doi_pmid.tsv']
    paper_to_patent={}
    
    
    for row_ind in range(len(papers_patents)):
        conf=int(papers_patents['confscore'][row_ind])
        # https://onlinelibrary.wiley.com/doi/10.1111/jems.12455 Table 1, 0.63% error
        if conf>=4:
            paper_mag=papers_patents['magid'][row_ind]
            patent_id=papers_patents['patent'][row_ind]
            if paper_mag not in paper_to_patent:
                paper_to_patent[paper_mag]=[patent_id]
            else:
                paper_to_patent[paper_mag].append(patent_id)
    
    # Add paper vertices
    print("Adding vertices to graph")
    papers=loaded_dict["Papers.txt"]
    
    #make dict of papers to dates
    paper_to_date={}
    for paper_ind in range(len(papers)):
        if isinstance(papers['Year'][paper_ind], str) and papers['Year'][paper_ind].isnumeric():
            paper_to_date[str(papers['PaperId'][paper_ind])]=int(papers['Year'][paper_ind])
    
    mag_graph, start_paper_ind, start_ref_ind, paper_id_to_v_ind, edges=restore_cache_graph_progress(mag_path, len(papers))
    matched_patents=0
    vertex_ind=len(paper_id_to_v_ind)

    print(f"Matched {matched_patents} patents to papers")      
    print(f"len paper_id_to_v_ind {len(paper_id_to_v_ind)}")
    # Add edges
    print("Adding edges to graph")
    cites=loaded_dict["PaperReferences.txt"]
    num_edges=0
    for ref_ind in tqdm(range(start_ref_ind, len(cites))):
        if ref_ind%(1800*100000)==0:
            cache_graph_progress(mag_path, mag_graph, paper_ind, ref_ind, len(papers), paper_id_to_v_ind, edges)
        v1=str(cites['PaperId'][ref_ind])
        v2=str(cites['PaperReferenceId'][ref_ind])
        if v1 in paper_to_date and v2 in paper_to_date:
            if paper_to_date[v1]>=paper_to_date[v2]-1:
                if v2 not in mag_graph:
                    mag_graph[v2]=[]
                mag_graph[v2].append(v1)
                num_edges+=1
            else:
                print(f'citation back in time {paper_to_date[v1]} {paper_to_date[v2]}')
        if paper_ind%60*100000==0:
            print(f"edge {ref_ind} of {len(cites)} total edges: {num_edges}", flush=True)
    print("Saving finished graph")
    cache_graph_progress(mag_path, mag_graph, paper_ind, ref_ind, len(papers), paper_id_to_v_ind, edges)
    print(f"Added {num_edges} edges")
    
    # Add random edges (for testing only)
    # for rnd_edge_ind in range(15000):
    #     v1=mag_graph.GetRndNId()
    #     v2=mag_graph.GetRndNId()
    #     mag_graph.AddEdge(v1, v2)
    
    return mag_graph, paper_id_to_v_ind

def cache_subgraph_progress(conf_paper_ids, in_verts, vert_depth, name, num_papers, save_loc, max_depth):
    cached_file=os.path.join(save_loc, f"{name}_{num_papers}_{max_depth}.p")
    pickle.dump((conf_paper_ids, in_verts, vert_depth), open(cached_file, 'wb'), compression=None)
    print(f"Saved subgraph progress")
    
def restore_subgraph_progress(name, num_papers, save_loc, max_depth):
    cached_file=os.path.join(save_loc, f"{name}_{num_papers}_{max_depth}.p")
    if os.path.exists(cached_file):
        conf_paper_ids, in_verts, vert_depth=pickle.load(open(cached_file, 'rb'), compression=None)
        print(f"Restored subgraph progress")
        return conf_paper_ids, in_verts, vert_depth
    else:
        return None, None, {}

def debug_get_conferences_subgraph(graph, loaded_dict, conference_series_ids, title_date_to_dup_mags, paper_id_to_v_ind, new_paper_authors_dict, save_loc, name, num_papers, test=False, max_depth=5):
    ''' debug and tests for get_conferences_subgraph
        
    args:
        graph: citation graph from make_mag_graph
        conference_series_ids: list of MAG conference series ids
        mag_path: path to folder containing MAG tsvs
        
    returns:
        subgraph: dict, paper MAG : list of cited paper MAGS for papers in conference and papers citing/cited by them to max_depth
    '''
    
    print("Starting components labeling")
    raw_papers=0
    in_verts=None
    if in_verts==None:
        # Get papers in conferences and journals
        papers=loaded_dict["Papers.txt"]
        conf_paper_ids=[]
        mag_title={}
        for paper_ind in tqdm(range(0, len(papers))):
            title=str(papers['PaperTitle'][paper_ind]).lower()
            mag_id=str(int(papers['PaperId'][paper_ind]))
            mag_title[mag_id]=title
            # if title=='ultra technological refugees identity construction through consumer culture among african refugees in israel':
            #     v_ind=paper_id_to_v_ind[mag_id]
            #     vert=graph.vs[v_ind]
            #     print(f'removing ultra technological refugees identity construction through consumer culture among african refugees in israel vertex degree {vert.degree()} vid {v_ind} magid {mag_id}')
            #     graph.delete_vertices([v_ind])
            if (str(papers['ConferenceSeriesId'][paper_ind]) in conference_series_ids
                or str(papers['JournalId'][paper_ind]) in conference_series_ids):
                key=get_dedup_key(mag_id, title, papers, new_paper_authors_dict)
                mag_ids=title_date_to_dup_mags[key]
                conf_paper_ids+=mag_ids
                raw_papers+=1
                #print(str(papers['ConferenceSeriesId'][paper_ind])+" "+str(papers['JournalId'][paper_ind]))
            # if paper_ind%10000==0:
                #print(f"Founds {len(conf_paper_ids)} papers in target conferences")
        print('conf_paper_ids.shape', len(conf_paper_ids), 'raw papers', raw_papers)
        
        conf_paper_ids=[str(conf_paper_ids[i]) for i in range(len(conf_paper_ids))]
        for mag_id in conf_paper_ids:
            vert_depths[mag_id]=0
        in_verts=set()
        search_verts=set(conf_paper_ids)
        print('len(search_verts)', len(search_verts))
    
def get_conferences_subgraph(graph, loaded_dict, conference_series_ids, title_date_to_dup_mags, paper_id_to_v_ind, new_paper_authors_dict, save_loc, name, num_papers, test=False, max_depth=5):
    ''' Get a graph of only papers in particular conferences, and 
        papers citing and cited by them.
        
    args:
        graph: citation graph from make_mag_graph
        conference_series_ids: list of MAG conference series ids
        mag_path: path to folder containing MAG tsvs
        
    returns:
        subgraph: dict, paper MAG : list of cited paper MAGS for papers in conference and papers citing/cited by them to max_depth
    '''
    
    print("Starting components labeling")
    search_verts, in_verts, vert_depths=restore_subgraph_progress(name, num_papers, save_loc, max_depth)
    raw_papers=0
    vert_depths={}
    if in_verts==None:
        # Get papers in conferences and journals
        papers=loaded_dict["Papers.txt"]
        conf_paper_ids=[]
        mag_title={}
        for paper_ind in range(0, len(papers)):
            if (str(papers['ConferenceSeriesId'][paper_ind]) in conference_series_ids
                or str(papers['JournalId'][paper_ind]) in conference_series_ids):
                title=str(papers['PaperTitle'][paper_ind]).lower()
                mag_id=str(int(papers['PaperId'][paper_ind]))
                mag_title[mag_id]=title
                
                key=get_dedup_key(mag_id, title, papers, new_paper_authors_dict)
                mag_ids=title_date_to_dup_mags[key]
                conf_paper_ids+=mag_ids

        print('conf_paper_ids.shape', len(conf_paper_ids)) 
        print("Start tree search")
        
        conf_paper_ids=[str(conf_paper_ids[i]) for i in range(len(conf_paper_ids))]
        for mag_id in conf_paper_ids:
            vert_depths[mag_id]=0
        
        
        in_verts=set()
        search_verts=set(conf_paper_ids)
    
    times=np.zeros(8)
    add_search_verts=[]
    add_in_verts=[]
    step=0
    while len(search_verts)>0:
        if step%1000==0:
            print(f'len(search_verts) {len(search_verts)} len(in_verts) {len(in_verts)}')
        search_vert=search_verts.pop()
        cur_depth=vert_depths[search_vert]
        add_in_verts.append(search_vert)
        if len(add_in_verts)>10000:
            in_verts=in_verts.union(set(add_in_verts))
            add_in_verts=[]
        if search_vert in graph:
            if cur_depth<max_depth:
                cited_by=set(graph[search_vert])
                cited_by=cited_by.difference(in_verts)
                add_search_verts+=cited_by
                if len(search_verts)==0 or step%50000==0:
                    search_verts=search_verts.union(set(add_search_verts))
                    add_search_verts=[]
                for cited in graph[search_vert]:
                    if cited not in vert_depths:
                        vert_depths[cited]=1000000
                    vert_depths[cited]=min(vert_depths[cited], cur_depth+1)
            else:
                print(f"depth exceeded {search_vert} {cur_depth}")
        else:
            print(f'{search_vert} not in graph {type(search_vert)}')
        # if len(in_verts)%100==0:
        #     print('time', times/len(in_verts))
        step+=1
        
        if step%1000000==0:
            in_verts=in_verts.union(set(add_in_verts))
            add_in_verts=[]
            
            search_verts=search_verts.union(set(add_search_verts))
            add_search_verts=[]
            
            cache_subgraph_progress(search_verts, in_verts, vert_depths, name, num_papers, save_loc, max_depth)
        
    in_verts=in_verts.union(set(add_in_verts))

    subgraph={}
    for vert in tqdm(in_verts):
        if vert in graph:
            subgraph[vert]=graph[vert]
        else:
            print(f'sub {vert} not in graph {type(vert)}')

    print(f"Conference subgraph has {len(subgraph)}")
    return subgraph

def test_conferences_subgraph():
    g=Graph(directed=True)
    g.add_vertices(10)
    edges=[]
    for i in range(9):
        edges.append((i,i+1))
    g.add_edges(edges)
    g.delete_vertices([5])
    # igraph.plot(g)
    
    # conf_paper_id=paper_id_to_v_ind[str(conf_paper_ids[0])]
    # print('conf_paper_id', conf_paper_id, int(conf_paper_id))
    bfs_verts, layers, parents = g.bfs(0, mode='out')
    bfs_nodes=[]
    graph_bfs_nodes=[]
    for node in bfs_verts:
        graph_bfs_nodes.append(node)
    graph_bfs_nodes=np.array(graph_bfs_nodes, dtype=np.int)
    conf_paper_ids=np.setdiff1d(conf_paper_ids, graph_bfs_nodes)
    if all_nodes is None:
        all_nodes=graph_bfs_nodes
    else:
        all_nodes=np.union1d(all_nodes, graph_bfs_nodes)
    print(f"{len(conf_paper_ids)} remaining in tree search")
    print(f"{len(all_nodes)} nodes in subgraph")

def get_patents_from_conferences(loaded_dict, title_date_to_dup_mags, conference_series_ids, new_paper_authors_dict):
    ''' Save list of patents directly citing papers from conferences.
    
    args:
        loaded_dict: dict of MAG dataframes from load_mag
        conference_series_ids: list of MAG conference series ids
    returns:
        mag_graph: graph_tool graph of papers and citations
    
    
    '''
    
    papers_patents=loaded_dict['_pcs_mag_doi_pmid.tsv']
    papers_patents_old=loaded_dict['_pcs.tsv']
    paper_to_patent={}
    
    for row_ind in tqdm(range(len(papers_patents))):
        # https://onlinelibrary.wiley.com/doi/10.1111/jems.12455 Table 1, 0.63% error
        conf=int(papers_patents['confscore'][row_ind])
        if conf>=4:
            paper_mag=str(papers_patents['magid'][row_ind])
            patent_id=str(papers_patents['patent'][row_ind])
            if paper_mag not in paper_to_patent:
                paper_to_patent[paper_mag]=[patent_id]
            else:
                paper_to_patent[paper_mag].append(patent_id)
    
    for row_ind in tqdm(range(len(papers_patents_old))):
        conf=int(papers_patents_old['confscore'][row_ind])
        if conf>=4:
            paper_mag=str(papers_patents_old['magid'][row_ind])
            patent_id=str(papers_patents_old['patent'][row_ind])
            if paper_mag not in paper_to_patent:
                paper_to_patent[paper_mag]=[patent_id]
            else:
                paper_to_patent[paper_mag].append(patent_id)
                
    print("Adding vertices to graph")
    papers=loaded_dict["Papers.txt"]
    paper_id_to_v_ind={}
    conf_patents=[]
    num_conf_papers=0
    conf_papers=[]
    for paper_ind in range(0, len(papers)):
        if (str(papers['ConferenceSeriesId'][paper_ind]) in conference_series_ids
            or str(papers['JournalId'][paper_ind]) in conference_series_ids):
            title=str(papers['PaperTitle'][paper_ind]).lower()
            paper_mag=str(papers['PaperId'][paper_ind])
            key=get_dedup_key(paper_mag, title, papers, new_paper_authors_dict)
            mag_ids=title_date_to_dup_mags[key]
            conf_papers.append([mag_ids, papers['PaperTitle'][paper_ind]])
            # print(f'len mag_ids {len(mag_ids)} key {key}')
            for mag_id in mag_ids:
                if mag_id in paper_to_patent:
                    patents=paper_to_patent[mag_id]
                    for patent in patents:
                        conf_patents.append([patent, mag_id, papers['PaperTitle'][paper_ind], papers['Year'][paper_ind]])
            num_conf_papers+=1
        if paper_ind%10000==0:
            print(f"Matched {len(conf_patents)} patents to {num_conf_papers} papers {paper_ind} of {len(papers)}")
            
    unique_conf_patents={}
    for patent_info in conf_patents:
        if patent_info[0] not in unique_conf_patents:
            unique_conf_patents[patent_info[0]]=patent_info
        else:
            unique_conf_patents[patent_info[0]]+=[patent_info[2], patent_info[3]]
            
    patents_data=[]
    for patent_id in unique_conf_patents:
        patents_data.append(unique_conf_patents[patent_id])
    return patents_data, conf_papers
    
def plot_graph(graph):
    labels={}
    for NI in graph.Nodes():
        labels[NI.GetId()] = str(NI.GetId())
    graph.DrawGViz(snap.gvlDot, "output.png", " ", labels)
    
def scrape_patents(args):
    '''
    Scrape patents from Google Patents.
    Taken from https://github.com/ryanlstevens/google_patent_scraper
    
    args:
        patents_list: list of strings of patent IDs
        
    returns
        patent_parsed: dict of dicts of patent information
    
    '''
    
    
    patents_list, patents_save_loc, save_pdf, save_info=args
    # print(patents_list, patents_save_loc, save_pdf, save_info)
    scraper=scraper_class(return_abstract=True)
    # ~ Add patents to list ~ #
    for patent in patents_list:
        patent=patent.replace("-", "").upper()
        if patent[0].isdigit():
            patent="US"+patent
        scraper.add_patents(patent)
    
    save_path=os.path.join(patents_save_loc, f'{patent}.lz4')
    # if os.path.exists(save_path):
    #     return None
    
    # ~ Scrape all patents ~ #
    scraper.scrape_all_patents()
    # ~ Get results of scrape ~ #
    patent_parsed = scraper.parsed_patents
    if 'patent_full_url' in patent_parsed[patent]:
        # print('patent found')
        if save_pdf:
            if not os.path.exists(os.path.join(patents_save_loc, f'{patent}.pdf')):
                try:
                    urllib.request.urlretrieve(patent_parsed[patent]['patent_full_url'], os.path.join(patents_save_loc, f'{patent}.pdf'))
                except:
                    print(f"Error No patent {patents_list}")
            else:
                print('Already downloaded patent')
        if save_info:
            patent_parsed=patent_parsed[patent]
            if 'title' in patent_parsed:
                
                # print(f'save in {save_path}')
                patent_info_row=[patent, patent_parsed['title'], patent_parsed['inventor_name'], patent_parsed['assignee_name_orig'], patent_parsed['assignee_name_current'],
                                 patent_parsed['pub_date'], patent_parsed['priority_date'], patent_parsed['grant_date'], patent_parsed['filing_date'],
                                 patent_parsed['abstract_text'], patent_parsed['patent_full_url'], patent_parsed['classification_code_descss'], patent_parsed['patent_text']] 

                pickle.dump(patent_info_row, open(os.path.join(patents_save_loc, f'{patent}.lz4'), 'wb'))
                # print('saved info')
    else:
        print(f"No patent {patents_list}")
    return patent_parsed
    
    #graph_draw(mag_graph, output="100k refs.pdf")

if __name__ == '__main__':
    test_conferences_subgraph()

#df=pd.read_csv("/media/willie/e0435106-b9f4-4e00-b6c7-33e1892fb212/Microsoft_Academic_Graph/Papers.txt", sep='\t', header=None,usecols=[0,5,6,7,8,9,10])#,12,13,14,19,20,21
#u=0

            
            
            

   
