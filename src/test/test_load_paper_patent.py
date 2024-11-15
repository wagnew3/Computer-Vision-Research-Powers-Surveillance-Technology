import pandas as pd
import re

if __name__ == '__main__':
    paper_patents=pd.read_csv('/media/ssd_2000/Microsoft_Academic_Graph/04.ConferenceSeries.nt', sep="> <", lineterminator=".")
    for i in range(10):
        print(paper_patents.loc[i])
        print("------------------------------------------------------")
    u=0