import matplotlib.pyplot as plt
import numpy as np

def imshow(img,
           figsize=(5,5),
           cmap='gray',
           axis='on',
           ax=None,
           title=None,
           zoom=None):
    '''Generate an MPL figure and show an image
    '''
    
    if zoom is not None:
        img = zoom_img(img,zoom)
    
    if ax is None:
        fig, ax = plt.subplots(1,1,
                               figsize=figsize,
                               tight_layout=True)
    else:
        plt.sca(ax)
        
    plt.imshow(img, cmap=cmap)
    plt.axis(axis)
    if title is not None:
        plt.title(title)
    
    return ax


def n_imshow(img_list,
             figsize=(10,3),
             cmap='gray',
             axis='off',
             titles=None,
             zoom=None):
    
    '''Generate an MPL figure and show an image
    '''
    
    n = len(img_list)
    fig, axes = plt.subplots(1,n,
                             figsize=figsize,
                             tight_layout=True)
    
    for ii,ax in enumerate(axes.ravel()):
        ax = imshow(img_list[ii], ax=ax)
    
    return fig, axes


def zoom_img(img,zoom):
    '''naive "zoom", actually just crops
    '''
    
    (h,w) = img.shape
    mid_h = np.ceil(h/2)
    mid_w = np.ceil(w/2)
    top = int(np.ceil(zoom*mid_h))
    bot = int(np.ceil(h-zoom*mid_h))
    left = int(np.ceil(zoom*mid_w))
    right = int(np.ceil(w-zoom*mid_w))
    
    img_zoom = img[top:bot,left:right]
    return img_zoom