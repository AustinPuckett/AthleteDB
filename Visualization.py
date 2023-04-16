import matplotlib
# from matplotlib import pyplot as plt
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from matplotlib.patches import Circle
import matplotlib.colors as mcolors
import imageio, PIL

def line_plot(frame, x, y, title=None):
    fig = Figure()
    
    # Figure settings
    fig.patch.set_facecolor(mcolors.CSS4_COLORS['mediumseagreen'])
    fig.patch.set_alpha(0.4)
    # matplotlib.rcParams.update({'font.size': 10, 'font.weight': 'bold', 'font.family': 'DejaVu Sans'})

    # Configure plot
    canvas = FigureCanvasTkAgg(fig, frame)
    ax = fig.add_subplot(111)
    ax.plot(x, y)
    
    
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ylim = [ax.get_ylim()[0]*.90, ax.get_ylim()[1]*1.11]
    xlim = [ax.get_xlim()[0], ax.get_xlim()[1]]
    ax.set_title(title, fontdict={'fontsize': 14, 'fontweight': 'bold'})
    ax.set_xticks(x)
    ax.set_xticklabels(x, fontdict={'fontsize': 8, 'fontweight': 'normal'}, rotation=30, ha='right')
    # plt.xticks(rotation=40, ha='right')
    ax.set_ylim([ylim[0], ylim[1]])
    ax.grid()
    # ax.legend()
    # ax.text(xlim[1] / 2 - 3.5, ylim[1] * 4 / 5 + .65, 'Schedule Wins (Expected Wins - Actual Wins)')

    return canvas

def create_visual2(frame, x=None, y=None):
    fig = Figure()
    x = [0, 1, 2, 3, 4]
    y = [i ** 2 for i in x]

    canvas = FigureCanvasTkAgg(fig, frame)
    ax = fig.add_subplot(111)
    ax.plot(x, y)

    return canvas




