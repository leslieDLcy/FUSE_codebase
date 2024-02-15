import numpy as np
import matplotlib.pyplot as plt

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


def save2Vis(figname):
    """ a shortcut function to save plot to visualization dir 

    Note
    ----
    We simply assume that every repo will have a 'visulizations' 
    dir under the root directory
    """

    axe = plt.gca()
    plt.savefig(f'visualizations/{figname}.pdf',
                format='pdf', dpi=300, bbox_inches='tight')