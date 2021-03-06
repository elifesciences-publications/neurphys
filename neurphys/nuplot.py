"""
Plotting helper functions for publication quality figures.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
from itertools import cycle
# using my style not necessary, but GREATLY encouraged
# mpl.style.use('estep_style')

# like pandas-profiling - also check the way Seaborn does it
# matplotlib.style.use(resource_filename(__name__, "estep_style.mplstyle"))

# try/except block with 'estep_style' and except warning to install it


def simple_axis(ax):
    """
    Removes the top and right axis lines and tick marks for a single
    matplotlib.axes object.

    Parameters
    ----------
    ax:
        Matplotlib axes object.
    """
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()


def simple_figure(f):
    """
    Removes the top and right axis lines and tick marks for all axes in a matplolib figure.

    Parameters
    ----------
    f:
        Matplotlib figure object.
    """
    num_ax = len(f.axes)
    if num_ax == 1:
        simple_axis(f.axes[0])
    else:
        for i in range(num_ax):
            f.axes[i].spines['top'].set_visible(False)
            f.axes[i].spines['right'].set_visible(False)
            f.axes[i].get_xaxis().tick_bottom()
            f.axes[i].get_yaxis().tick_left()


def clean_axis(ax, y_units, **y_hline):
    """
    Removes all axis lines and tick marks for a single matplotlib.axes object.

    Parameters
    ----------
    ax:
        Matplotlib axes object.
    y_units: str
        The units you want listed in your legend for the y_hline(s).
    y_hline: key-value pair or None (default)
        Draws an arbitrary number of dotted horizontal lines at a user
        specified y-values that spans the entire length of the figure.
        ex: string = <int or float>
            baseline = -50.0
    """
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    for key, val in y_hline.items():
        ax.axhline(y=val,color='grey',linestyle='dotted',
                   label='{0}: {1} {2}'.format(key,val,y_units))


def clean_figure(f, y_units, **y_hline):
    """
    Removes all axis lines and tick marks for all axes in a matplolib figure.

    Parameters
    ----------
    f:
        Matplotlib figure object.
    y_units: str
        The units you want listed in your legend for the y_hline(s).
    y_hline: key-value pair or None (default)
        Draws an arbitrary number of dotted horizontal lines at a user
        specified y-values that spans the entire length of the figure.
        ex: string = <int or float>
            baseline = -50.0
    """
    num_ax = len(f.axes)
    if num_ax == 1:
        clean_axis(f.axes[0], y_units, **y_hline)
    else:
        for i in range(num_ax):
            f.axes[i].spines['top'].set_visible(False)
            f.axes[i].spines['right'].set_visible(False)
            f.axes[i].spines['bottom'].set_visible(False)
            f.axes[i].spines['left'].set_visible(False)
            f.axes[i].get_xaxis().set_visible(False)
            f.axes[i].get_yaxis().set_visible(False)
            for key, val in y_hline.items():
                f.axes[i].axhline(y=val,color='grey',
                                  linestyle='dotted',label=
                                  '{0}: {1} {2}'.format(key,val,y_units))


def nu_legend(f, x_scale, x_units, y_scale, y_units):
    """
    Add x and y scale bars to the bottom right of the only/last subplot of a
    figure and a legend outside of the figure.

    Parameters
    ----------
    f:
        Matplotlib figure object.
    x_scale: int or float
        User specified length of the scale bar.
    x_units: str
        X-axis units used in the figure legend.
    y_scale: int or float
        User specified length of the scale bar.
    y_units: str
        Y-axis units used in the figure legend.

    TODO:
    - modify this function to work on specific axes?
    """

    ax = f.axes[-1]
    x_min,x_max = ax.get_xlim()[0],ax.get_xlim()[1]
    y_min,y_max = ax.get_ylim()[0],ax.get_ylim()[1]
    x_range = abs(x_min-x_max)
    y_range = abs(y_min-y_max)
    hline_min = (x_scale/x_range)
    vline_max = (y_scale/y_range)
    ax.axhline(y=y_min,xmin=(1-hline_min),xmax=1,color='black',lw=2,
               label='x: {0} {1}'.format(x_scale,x_units))
    ax.axvline(x=x_max,ymin=0,ymax=vline_max,color='black',lw=2,
               label='y: {0} {1}'.format(y_scale,y_units))
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0,
               frameon=False)


def nu_boxplot(ax, df, cmap=False, color_list=False,
               medians_only=False, no_x=False, show_outliers=True, **y_hline):
    """
    Makes a much improved boxplot. Whiskers set at 10/90 percentiles.

    Parameters
    ----------
    ax:
        Matplotlib axes object.
    df: pandas DataFrame
        Pandas Dataframe where each column makes a separate boxplot. Column
        names will be used as x-axis labels.
    cmap: string (or direct call)
        Any valid matplotlib colormap (ex: 'afmhot' or 'viridis'). Can also
        call through direct mpl.cm.<colormap_name>.
    color_list: list
        List of valid matplotlib colors. Colors will be repeated if not enough
        are supplied.
    medians_only: bool (default=False)
        Default changes the entire boxplot the new color,
        but if True only changes the color of the median bar.
    no_x: bool (default=False)
        Change to 'True' if you want to get rid of the bottom x-axis and
        ticks.
    showfliers: bool (default=True)
        Turns outliers on or off.
    y_hline: key-value pair or None (default=None)
        Draws an arbitrary number of dotted horizontal lines at user specified
        y-value that spans the entire length of the figure.
        ex: string = <int or float> (baseline = -50.0)

    Returns
    -------
    bp: dict of matplolib objects
        Contains all the necessary boxplot parameters, and when properly
        assigned to a matplotlib axes object will render your boxplot.

    TODO:
    - move xaxis labels to left an option
    - CHANGE OUTLIERS TO SOMETHING MORE COMPATIBLE WITH ILLUSTRATOR. MAYBE
     DECREASE SIZE WHILE INCREASING LINEWIDTH TO MAKE ILLUSION OF FILLED
     CIRCLE, BUT WON'T RUN INTO PROBLEM WHEN CHANGING COLOR IN THE PROGRAM?
    - also need to make work with pd.Series since it apparently doesn't like
    to (easy fix. if Series, then pd.Dataframe(Series). should work just fine)
    """

    # remake data into list of lists. compensates for differing column sizes.
    columns = df.columns
    series_array = []
    for column in columns:
        series_array.append(df[column].dropna())
    column_num = len(series_array)
    # set up basic plotting values and parameters
    if df.ndim == 1:
        column_num = 1
        labels = [df.name]
    else:
        column_num = df.shape[1]
        labels = df.columns.values
    # make the basic figure with better default properties.
    # first line are pd.df.boxplot specific params, then general mpl params
    bp = ax.boxplot(series_array,
                    boxprops=dict(color='000000',linestyle='-',linewidth=2),
                    capprops=dict(color='000000',linestyle='-',linewidth=2),
                    flierprops=dict(linestyle='none',marker='.',
                                    markeredgecolor='000000',
                                    markerfacecolor='000000',markersize=5),
                    medianprops=dict(color='000000',linestyle='-',
                                     linewidth=4),
                    showfliers=show_outliers,
                    widths=0.5,
                    whis=[10,90],
                    whiskerprops=dict(color='000000',linestyle='-',linewidth=1
                    ))
    # make color cycler
    if cmap:
        color_idx = np.linspace(0,1,column_num)
        color_cycler = cycler('color',[mpl.cm.get_cmap(cmap)(color_idx[i])
                              for i in range(column_num)])
    elif color_list:
        color_cycler = cycler('color',color_list)
    else:
        color_cycler = cycler('color',[i['color']
                              for i in mpl.rcParams['axes.prop_cycle']])
    # change the color parameters
    for i, color_dict in zip(range(column_num), cycle(color_cycler)):
        if medians_only:
            mpl.artist.setp(bp['boxes'][i],color='000000')
            mpl.artist.setp(bp['medians'][i],**color_dict)
            mpl.artist.setp(bp['whiskers'][i*2],color='000000')
            mpl.artist.setp(bp['whiskers'][i*2+1],color='000000')
        else:
            # need to set color at beginning so it doesn't cycle with every
            # line
            color = color_dict['color']
            mpl.artist.setp(bp['boxes'][i],color=color)
            mpl.artist.setp(bp['caps'][i*2],color=color)
            mpl.artist.setp(bp['caps'][i*2+1],color=color)
            mpl.artist.setp(bp['medians'][i],color=color)
            mpl.artist.setp(bp['whiskers'][i*2],color=color)
            mpl.artist.setp(bp['whiskers'][i*2+1],color=color)
            if show_outliers:
                mpl.artist.setp(bp['fliers'][i],markerfacecolor=color,
                                markeredgecolor=color)

    # add in an optional line
    for key, val in y_hline.items():
        ax.axhline(y=val,color='grey',linestyle='dotted')
    # make final changes to plot to clean it up and make it pretty
    ax.xaxis.set_ticklabels(columns, rotation=45, horizontalalignment='right')
    simple_axis(ax)
    if no_x:
        ax.spines['bottom'].set_visible(False)
        ax.get_xaxis().set_visible(False)
    return bp


def nu_scatter(ax, df, alpha=0.35, cmap=False, color_list=False, jitter=0.05,
               markersize=8, monocolor=False, no_x=False, paired=False,
               seed=0):
    """
    Creates a scatter column plot.

    Parameters
    ----------
    ax:
        Matplotlib axes object.
    df: pandas DataFrame
        Pandas Dataframe where each column makes a separate scatter column
        plot. Column names will be used as x-axis labels.
    alpha: float (0.0 through 1.0)
        Sets marker opacity. 0.0 = transparent through 1.0 = opaque.
    cmap: string (or direct call)
        Any valid matplotlib colormap (ex: 'afmhot' or 'viridis'). Can also
        call through direct mpl.cm.<colormap_name>.
    color_list: list
        List of valid matplotlib colors. Colors will be repeated if not enough
        are supplied.
    jitter: float (0.0 through 1.0, default=0.35)
        Sets the amount of jitter in the column data. The default value keeps
        the scatter to roughly between the whiskers. 0.0 = no jitter through
        1.0 = jitter the width of the plot. Can technically go past 1.0, but
        at that point you lose data from the figure, so do not do that.
    markersize: float
        Sets the size of the scatter plot marker.
    monocolor: any matplotlib color (default=False)
        Set all scatter plot objects to the specificed color.
    no_x: bool (default=False)
        Change to 'True' if you want to get rid of the bottom x-axis and
        ticks.
    paired: bool (default=False)
        Will draw grey lines to data points with the same row index. If jitter
        set to 0 lines will connect datapoints. If not, it will look stupid.
        (may add features later to keep people from mucking it up, but we'll
        see...)
    seed:
        Sets the numpy.random.seed value that controls the jitter of the
        resulting plots. Same data + same seed = same figure.

    Returns
    -------
    sc: list of matplolib objects
        Contains all the necessary scatterplot parameters, and when properly
        assigned to a matplotlib axes object will render your scatterplot.

    TODO:
    - Should I just remove the markeredge entirely? may make things easier in
    the long run... (Update: did removed it, but could easily add it back.
    Need input from the lab since I don't want an overabundance of optional
    parameters to pass to the function that won't be used 99.9% of the time).
    """

    # set up basic plotting values and parameters
    np.random.seed(seed)
    data = df.values
    if df.ndim == 1:
        column_num = 1
        labels = [df.name]
    else:
        column_num = df.shape[1]
        labels = df.columns.values
    # make color cycler
    if cmap:
        color_idx = np.linspace(0,1,column_num)
        color_cycler = cycler('color',[mpl.cm.get_cmap(cmap)(color_idx[i])
                              for i in range(column_num)])
    elif color_list:
        color_cycler = cycler('color',color_list)
    else:
        color_cycler = cycler('color',[i['color']
                              for i in mpl.rcParams['axes.prop_cycle']])
    # need to draw paired lines first for stacking purposes
    if paired:
        for i in range(len(df)):
            ax.plot(np.arange(1,column_num+1),df.iloc[i],
                    color='000000',alpha=0.5)
    # create the scatter plot
    for i, color_dict in zip(range(column_num), cycle(color_cycler)):
        if column_num == 1:
            y = data
        else:
            y = data[:,i]
        if jitter == 0:
            x = [i+1]*len(y)
        else:
            x = np.random.normal(i+1, jitter, size=len(y))
        # need to set color at beginning so it doesn't cycle with every line
        color = color_dict['color']
        sc = ax.plot(x,y,
                     alpha=alpha,
                     color=color,
                     linestyle='None',
                     label=labels[i],
                     marker='.',
                     markersize=markersize,
                     markeredgewidth=0)
        if monocolor:
            mpl.artist.setp(sc[0],\
            markeredgecolor='none',markerfacecolor=monocolor)
    # make final changes to plot to clean it up and make it pretty
    ax.set_xlim(0.5, column_num+0.5)
    ax.xaxis.set_ticks(np.arange(1, column_num+1))
    ax.xaxis.set_ticklabels(labels, rotation=45, horizontalalignment='right')
    simple_axis(ax)
    if no_x:
        ax.spines['bottom'].set_visible(False)
        ax.get_xaxis().set_visible(False)
    return sc


def nu_raster(ax, df, color='00000', **x_vline):
    """
    Creates a raster plot that reads top-down and left-right.

    Parameters
    ----------
    ax:
        Matplotlib ax object.
    df: pandas DataFrame
        Pandas Dataframe where each column makes a separate raster plot. THE
        PLOT WILL READ IN THE EXACT SAME MANNER AS 'df.T' LOOKS.
    color: any valid matplotlib color (default: black)
        Color of your raster lines.
    x_vline: key-value pair or None (default=None)
        Draws an arbitrary number of dotted horizontal lines at user specified
        y-value that spans the entire length of the figure.

    Returns
    -------
    ras: matplotlib.collections.LineCollection
        Contains all the necessary raster parameters, and when properly
        assigned to a matplotlib axes object will render your raster plot.

    Heavily adapted from:
    [1] https://scimusing.wordpress.com/2013/05/06/
    making-raster-plots-in-python-with-matplotlib/

    TODO:
    - y label?
    - bottom up option?
    - line weight?
    - dotted line color/weight?
    """

    data = df.T.values
    if df.ndim == 1:
        ras = ax.vlines(data,0.5,1.5,color=color)
        ax.set_ylim(0.5, 1.5)
        ax.set_xlim(df.dropna().min(), df.dropna().max())
    else:
        for i, sweep in enumerate(data):
            ras = ax.vlines(sweep, i+0.5, i+1.5, color=color)
        ax.set_ylim(0.5, len(data)+0.5)
        ax.set_yticks(np.arange(1, data.shape[0]+1, 1))
    # add in an optional line
    for key, val in x_vline.items():
        ax.axvline(x=val, color='grey', linestyle='dotted')
    ax.invert_yaxis()
    simple_axis(ax)
    return ras


def nu_violin(ax, df, cmap=False, color_list=False, no_x=False,
              outline_only=False, rug=False, **y_hline):
    """
    Makes a much improved boxplot.

    Parameters
    ----------
    ax:
        Matplotlib axes object.
    df: pandas DataFrame
        Pandas Dataframe where each column makes a separate boxplot. Column
        names will be used as x-axis labels.
    cmap: str (or direct call)
        Any valid matplotlib colormap (ex: 'afmhot' or 'viridis'). Can also
        call through direct mpl.cm.<colormap_name>.
    color_list: list
        List of valid matplotlib colors. Colors will be repeated if not enough
        are supplied.
    no_x: bool (default=False)
        Change to 'True' if you want to get rid of the bottom x-axis and
        ticks.
    outline_only: bool (default=False)
        Remove the fill from each of the violin plots.
    rug: bool (default=False)
        Add a short horizontal line where each datapoint would be. Try it.
        It's cool.
    y_hline: key-value pair or None (default=None)
        Draws an arbitrary number of dotted horizontal lines at user specified
        y-value that spans the entire length of the figure.
        ex: string = <int or float>
            baseline = -50.0

    Returns
    -------
    vio: dict of matplolib objects
        Contains all the necessary boxplot parameters, and when properly
        assigned to a matplotlib axes object will render your boxplot.

    Notes
    - 'medians_only' parameter does not currently work like it did in
    nu_boxplot. It will though, goddamnit!
    -----
    """

    # remake data into list of lists. compensates for differing column sizes.
    columns = df.columns
    series_array = []
    for column in columns:
        series_array.append(df[column].dropna())
    column_num = len(series_array)
    # make the basic figure with better default properties.
    vio = ax.violinplot(series_array,
                        showmedians=True)
    # make color cycler
    if cmap:
        color_idx = np.linspace(0,1,column_num)
        color_cycler = cycler('color',[mpl.cm.get_cmap(cmap)(color_idx[i]) \
        for i in range(column_num)])
    elif color_list:
        color_cycler = cycler('color',color_list)
    else:
        color_cycler = cycler('color',[i['color'] \
        for i in mpl.rcParams['axes.prop_cycle']])
    # change the color parameters
    for i, color_dict in zip(range(column_num), cycle(color_cycler)):
        if outline_only:
            # need to set color at beginning so it doesn't cycle with every
            # line
            color = color_dict['color']
            mpl.artist.setp(vio['bodies'][i],color='111111')
            mpl.artist.setp(vio['bodies'][i],linewidth=2,edgecolor=color,\
            alpha=1)
            mpl.artist.setp(vio['cbars'],lw=0)
            mpl.artist.setp(vio['cmaxes'],lw=0)
            mpl.artist.setp(vio['cmedians'],lw=3,color='000000')
            mpl.artist.setp(vio['cmins'],lw=0)
        else:
            # need to set color at beginning so it doesn't cycle with every
            # line
            color = color_dict['color']
            mpl.artist.setp(vio['bodies'][i],linewidth=2,color=color,\
            alpha=0.35)
            mpl.artist.setp(vio['cbars'],lw=0.5,color='000000')
            mpl.artist.setp(vio['cmaxes'],lw=0)
            mpl.artist.setp(vio['cmedians'],lw=3,color='000000')
            mpl.artist.setp(vio['cmins'],lw=0)
    # add rug plot if selected
    if rug:
        if df.ndim == 1:
            ras = ax.hlines(df.T.values,0.95,1.05,color='000000',\
            alpha=0.35,linewidth=0.75)
        else:
            data = df.T.values
            for i, sweep in enumerate(data):
                ras = ax.hlines(sweep,i+0.95,i+1.05,color='000000',\
                alpha=0.35,linewidth=0.75)
    # add in an optional line
    for key, val in y_hline.items():
        ax.axhline(y=val,color='grey',linestyle='dotted')
    # make final changes to plot to clean it up and make it pretty
    ax.set_xticks(np.arange(1,column_num+1))
    ax.set_xlim(0.5,column_num+0.5)
    ax.xaxis.set_ticklabels(columns, rotation=45, horizontalalignment='right')
    simple_axis(ax)
    if no_x:
        ax.spines['bottom'].set_visible(False)
        ax.get_xaxis().set_visible(False)
    return vio


def nu_specheatmap(ax, df, sweep='sweep001', align='left', cmap='gray'):
    """
    Produce heatmap from spectrogram function.

    Parameters
    ----------
    ax:
        Matplotlib axes object.
    df: pandas DataFrame
        Pandas Dataframe generated from oscillation.nu_spectrogram function.
    sweep: str (default: 'sweep001')
        Sweep to be plotted.
    align: str (default: 'left')
        If plotting spectrogram alongside original signal, time values for
        the spectrogram windows can be aligned with time values of the
        signal. 'Left' aligns the left side of each spectrogram window to the
        left side of each signal window. With that explained, I'm pretty sure
        you can figure out what 'center' and 'right' do. If not, please pick
        a new line of work.
    cmap: any valid matplotlib cmap (default: 'gray')
        I picked one because the standard default is awful.

    Returns
    -------
    hm: matplotlib QuadMesh object
        QuadMesh plot.
    """

    # pull necessary variables for plotting from dataframe
    t = df.xs(sweep).columns
    f = df.xs(sweep).index
    data = df.xs(sweep).values

    # modify time values to customize the plot
    if align == 'center':
        t += ((nperseg/fs)/2) - 0.5
    elif align == 'right':
        t += ((nperseg/fs)) - 1
    elif align not in ('left','center','right'):
        raise ValueError('Not a recognized variable. Check the docs.')

    hm = plt.pcolormesh(t, f, data, cmap=cmap)
    simple_axis(ax)
    return hm


def nu_genheatmap(ax, df, xlim=None, ylim=None, cmap='gray'):
    """
    Create a heatmap from a unlabeled dataframe. x and y limits
    are determined by standard pandas integer-based indexing.

    Think of the dataframe as xy coordinates. This function plots
    the data as df[::-1].

    Parameters
    ----------
    ax:
        matplotlib axes object
    df: pandas DataFrame
        Unlabeled pandas dataframe.
    xlim: tuple (min, max) (default: None)
        X-limits for the plot. Best to use in this manner over setting
        the 'set_xlim' attribute on the axes.
    ylim: tuple (min, max) (default: None)
        Y-limits for the plot. Best to use in this manner over setting
        the 'set_ylim' attribute on the axes.
    cmap: any valid matplotlib cmap (default: 'gray')
        I picked one because the standard default is awful.

    Returns
    -------
    hm: matplotlib QuadMesh object
        QuadMesh plot.
    """

    # truncate dataframe
    if xlim is not None:
        df = df.iloc[:,xlim[0]:xlim[1]]
    if ylim is not None:
        df = df.iloc[ylim[0]:ylim[1],:]

    # pull necessary values from dataframe
    vals = df.values
    rows = np.arange(vals.shape[0])
    cols = np.arange(vals.shape[1])
    i, j = np.meshgrid(rows, cols, indexing='ij')

    hm = plt.pcolormesh(j, i, vals, cmap=cmap)
    simple_axis(ax)
    return hm
