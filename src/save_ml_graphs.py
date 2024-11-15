import utils
from optparse import OptionParser
import os
import compress_pickle as pickle

if __name__ == '__main__':
    '''
    Computer Vision
    1. CVPR: 1158167855
    2. ECCV: 1124077590
    3. ICCV: 1164975091
    4. IEEE Transactions on Pattern Analysis and Machine Intelligence: 199944782 1979
    5. IEEE Transactions on Image Processing: 115304631
    6. WACV
    
    Artificial Intelligence
    1. ICLR: 2584161585
    2. NeurIPS: 1127325140
    3. ICML: 1180662882
    4. AAAI: 1184914352 (listed as National Conference on Artificial Intelligence?)
    5. IEEE Transactions On Systems, Man And Cybernetics Part B, Cybernetics: 76152103
    
    Computational Linguistics
    1. ACL: 1188739475
    2. EMNLP: 1192655580
    3. NAACL: 1173951661
    4. COLING: 1169674987
    5. Transactions of the Association for Computational Linguistics: 2729999759
    
    Robotics
    1. ICRA: 1163902177
    2. IEEE Robotics and Automation Letters: 116420536 (listed as ieee transactions on robotics and automation?)
    3. IROS: 1143279144
    4. Transactions on Mechatronics: 13961689
    5. Science Robotics: not listed
    '''
    
    all_confs=['1158167855', '1124077590', '1164975091', '199944782', '115304631',
                                                  '2584161585', '1127325140', '1180662882', '1184914352', '76152103',
                                                  '1188739475', '1192655580', '1173951661', '1169674987', '2729999759',
                                                  '1163902177', '116420536', '1143279144', '13961689']
    cvpr=['1158167855']
    
    ijssc=['83637746'] #ieee journal of solid state circuits
    ccs=['1198471430'] #Computer and Communications Security
    chi=['89276529'] #chi
    icse=['1174403976'] #International Conference on Software Engineering
    osdi=['1185109434'] #Operating Systems Design and Implementation
    pldi=['1127352206'] #Programming Language Design and Implementation
    mia=['116571295'] #Medical Image Analysis
    
    
    
    parser = OptionParser()
    parser.add_option("--data_dir", dest="data_dir", default="/media/ssd_2000/Microsoft_Academic_Graph/")
    (options, args) = parser.parse_args()
    print(options)
    
    num_papers=-1
    
    mag=utils.load_mag(options.data_dir, n_papers=num_papers)
    title_date_to_dup_mags, mag_to_dup_mags, new_paper_authors_dict=utils.make_title_date_to_dup_mags(mag, options.data_dir)
    
    #mag_graph, paper_id_to_v_ind=utils.make_mag_graph(mag, options.data_dir)
    #pickle.dump((mag_graph, paper_id_to_v_ind), os.path.join(options.data_dir, f'mag_graph_{num_papers}.lz4'))
    mag_graph, paper_id_to_v_ind=pickle.load(os.path.join(options.data_dir, f'mag_graph_{num_papers}.lz4'))
    print(f'graph has {len(mag_graph)} vertices')
    #mag_graph.Save(snap.TFOut(os.path.join(options.data_dir, f'mag_graph_{num_papers}.b')))
    
    # Make CVPR graph
    # cvpr_graph=utils.get_conferences_subgraph(mag_graph, mag, all_confs, title_date_to_dup_mags, paper_id_to_v_ind, new_paper_authors_dict, options.data_dir, "cvpr", num_papers, max_depth=3)
    # pickle.dump(cvpr_graph, open(os.path.join(options.data_dir, f'cvpr_graph_{num_papers}.lz4'), 'wb'))
    
    cvpr_graph=utils.debug_get_conferences_subgraph(mag_graph, mag, all_confs, title_date_to_dup_mags, paper_id_to_v_ind, new_paper_authors_dict, options.data_dir, "cvpr", num_papers, max_depth=3)
    
    # # Make AI graph
    # ml_graph=utils.get_conferences_subgraph(mag_graph, mag, cvpr, title_date_to_dup_mags, paper_id_to_v_ind, new_paper_authors_dict, options.data_dir, "all_ml", num_papers, max_depth=3)
    # pickle.dump(ml_graph, open(os.path.join(options.data_dir, f'ml_graph_{num_papers}.lz4'), 'wb'))
    
    
    