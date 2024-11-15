import matplotlib.pyplot as plt
import numpy as np

import os
save_loc="/home/willie/Documents/queeria_data/plots/"

# https://www.nature.com/articles/nmeth.1618
colorblind_colors=np.array([[204, 121, 167],
                   [213, 94, 0],
                   [0,114,178],
                   [240,228,66],
                   [0,158,115],
                   [86,180,233],
                   [230,159,0]])/255.0

obscured_data_color=np.array([0,0,0])

def fix_labels(labels):
    if "Gender Non-Conforming" in labels:
        labels[labels.index("Gender Non-Conforming")]="Gender\nNon-Conforming"
    return labels

def bar_chart(datas, labels, group_labels, y_axis, title):
    group_labels=fix_labels(group_labels)
    total_width=0.9
    
    num_groups=len(datas)
    x = np.arange(len(group_labels))  # the label locations
    width = total_width/num_groups  # the width of the bars
    
    fig, ax = plt.subplots()
    rectss=[]
    obsc=[]
    for group_num in range(num_groups):
        labelled=False
        offset=width/2+-total_width/2+total_width*(group_num/num_groups)
        
        for x_ind in range(x.shape[0]):
            height=datas[group_num][x_ind]
            if height>0 and height<=3:
                height=3
                hatch=''
                obsc.append(True)
            else:
                hatch=""
                obsc.append(False)
            
            color=colorblind_colors[group_num % len(colorblind_colors)]
                
            if labels is not None and not labelled:
                rects = ax.bar(x[x_ind]+offset, height, width, label=(labels[group_num]), color=color, hatch=hatch)
                labelled=True
            else:
                rects = ax.bar(x[x_ind]+offset, height, width, color=color, hatch=hatch)
            rectss.append(rects)
    
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_ylim(0, 1.1*np.amax(datas[group_num]))
    ax.set_xticklabels(group_labels, rotation = 90)
    if labels is not None:
        ax.legend()
    
    for rectind in range(len(rectss)):
        if obsc[rectind]:
            ax.bar_label(rectss[rectind], labels=["*"], padding=3, fontsize=8)
    
    fig.tight_layout()
    
    plt.savefig(os.path.join(save_loc, title+".png"))
    
    