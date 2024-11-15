import matplotlib.pyplot as plt
import numpy as np

import os
save_loc="/home/willie/Documents/queeria_data/plots/"

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n({:d})".format(pct, absolute)

def pie_chart(data, labels, title):
    norm_data=data/np.sum(data)
    fig, ax = plt.subplots()
    ax.pie(norm_data, labels=labels, autopct=lambda pct: func(pct, data))
    ax.axis('equal')
    
    
    ax.set_title(title)
    fig.tight_layout()
    plt.savefig(os.path.join(save_loc, title+".png"))