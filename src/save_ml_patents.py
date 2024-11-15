import utils
from optparse import OptionParser
import os
import snap
import pickle
import csv
import random
import multiprocessing as mp


if __name__ == '__main__':
    '''
    Computer Vision
    1. CVPR: 1158167855
    2. ECCV: 1124077590
    3. ICCV: 1164975091
    4. IEEE Transactions on Pattern Analysis and Machine Intelligence: 199944782
    5. IEEE Transactions on Image Processing: 115304631
    
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
    cv=['1158167855', '1124077590', '1164975091', '199944782', '115304631']
    nlp=['1188739475', '1192655580', '1173951661', '1169674987', '2729999759']
    robotics=['1163902177', '116420536', '1143279144', '13961689']
    
    parser = OptionParser()
    parser.add_option("--data_dir", dest="data_dir", default="/media/ssd_2000/Microsoft_Academic_Graph/")
    (options, args) = parser.parse_args()
    print(options)
    
    mag=utils.load_mag(options.data_dir, n_papers=-1)
    
    title_date_to_dup_mags, paper_id_to_v_ind, new_paper_authors_dict=utils.make_title_date_to_dup_mags(mag, options.data_dir)
    
    # # all ml confs
    # patents, conf_papers=utils.get_patents_from_conferences(mag, title_date_to_dup_mags, all_confs, new_paper_authors_dict)
    # random.shuffle(patents)
    # with open('all_ml_patents.csv', 'w', newline='') as csvfile:
    #     csvwriter = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     csvwriter.writerows(patents)
    # CVPR
    patents, conf_papers=utils.get_patents_from_conferences(mag, title_date_to_dup_mags, cvpr, new_paper_authors_dict)
    random.shuffle(patents)
    with open('cvpr_patents.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerows(patents)
    # # NLP
    # patents, conf_papers=utils.get_patents_from_conferences(mag, title_date_to_dup_mags, nlp, new_paper_authors_dict)
    # random.shuffle(patents)
    # with open('nlp_patents.csv', 'w', newline='') as csvfile:
    #     csvwriter = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     csvwriter.writerows(patents)
    # CV
    # patents, conf_papers=utils.get_patents_from_conferences(mag, title_date_to_dup_mags, cv, new_paper_authors_dict)
    # random.shuffle(patents)
    # with open('cv_patents.csv', 'w', newline='') as csvfile:
    #     csvwriter = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     csvwriter.writerows(patents)
    # # Robotics
    # patents, conf_papers=utils.get_patents_from_conferences(mag, title_date_to_dup_mags, robotics, new_paper_authors_dict)
    # random.shuffle(patents)
    # with open('robotics_patents.csv', 'w', newline='') as csvfile:
    #     csvwriter = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     csvwriter.writerows(patents)
    
    
    