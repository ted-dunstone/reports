import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import DBSCAN, OPTICS
from collections import Counter
import pandas as pd

import seaborn as sns
import pytablewriter
from IPython.display import display, Markdown
from IPython.display import Image as IpyImg

# Classes for displaying tables and figures.


class Tables():
    table_count = 0

    def render(self, df, name):
        self.table_count += 1
        writer = pytablewriter.MarkdownTableWriter()
        #writer.table_name = "example_table"
        writer.header_list = list(df.columns.values)
        writer.value_matrix = df.values.tolist()
        display(Markdown("%s \n\n**Table %d**: *%s*\n\n" %
                         (writer.dumps(), self.table_count, name)))

    def markdown(self, df, name):
        self.table_count += 1
        print(df.to_markdown())
        print(f'table {self.table_count}: {name}')


class Figures():
    figure_count = 0

    def render(self, img_fn, name):
        self.figure_count += 1
        if img_fn != None:
            display(IpyImg(filename=img_fn))
        display(Markdown("**Figure %d**: *%s*\n\n" %
                         (self.figure_count, name)))


def plot_Zoo_mpl(zoo_results, eps):
    zoo_results = zoo_results.dropna()
    plt.figure(figsize=(12, 7))
    y_name = "match_score"
    x_name = "false_match_score"
    x = zoo_results[x_name]
    y = zoo_results[y_name]
    data = [r for r in zip(x.values, y.values)]
    model = DBSCAN(eps=eps, min_samples=10).fit(data)
    colors = model.labels_
    xmean = x.mean()
    ymean = y.mean()

    def mapv(c, xy):
        if c == -1:
            x1, y1 = xy[0], xy[1]
            if x1 <= xmean and y1 <= ymean:
                return "phantom", 10
            elif x1 >= xmean and y1 <= ymean:
                return "dove", 10
            elif x1 >= xmean and y1 >= ymean:
                return "chameleon", 10
            elif x1 <= xmean and y1 >= ymean:
                return "worm", 10
            print(x1, y1, c)
        else:
            return "sheep", 5

    zoo_map = [mapv(c, data[i]) for (i, c) in enumerate(colors)]

    data = zoo_results.copy()
    data['zoo_class'] = [v[0] for v in zoo_map]

    data['zoo_size'] = [v[1] for v in zoo_map]

    ax = sns.scatterplot(x=x_name, y=y_name, hue='zoo_class', style='zoo_class', size='zoo_size',
                         data=data, legend='brief')
    plt.axhline(y.mean(), linestyle=':')
    plt.axvline(x.mean(), linestyle=':')

    # fix legend
    h, l = ax.get_legend_handles_labels()
    col_lgd = plt.legend(h[:6], l[:6], loc='upper left',
                         bbox_to_anchor=(0.05, -.09), fancybox=True, shadow=True, ncol=6)
    plt.gca().add_artist(col_lgd)

    return data[data['zoo_class'] != 'sheep']

# Matplotlib plotting functions.


def plot_match_dist_mpl(match_scores, non_match_scores, threshold=None, match_color='green', non_match_color='red', kde_on=True, labels_on=True):
    """
    Plot a match / non-match distribution

    match_scores : pandas series or list
    non_match_scores : pandas series or list
    threshold : float
    kde_on = flag to use kde
    """

    plt.figure(figsize=(12, 7))
    m_label = "matches" if labels_on else None
    mn_label = "non matches" if labels_on else None
    def thrs_label(thresh): return f"threshold {threshold}"
    sns.distplot(match_scores, kde=kde_on, norm_hist=True, hist=not kde_on,
                 color="green", rug=True, label=m_label, rug_kws={"height": 0.06})
    sns.distplot(non_match_scores, kde=kde_on, norm_hist=True, hist=not kde_on,
                 color="red", rug=True, label=mn_label, rug_kws={"height": 0.04})
    if threshold is not None:
        if type(threshold) == tuple:
            plt.axvline(threshold[0], ls='--', c='grey',
                        alpha=0.8, label=thrs_label(threshold[0]))
            plt.axvline(threshold[1], ls='--', c='grey',
                        alpha=0.8, label=thrs_label(threshold[1]))
        else:
            plt.axvline(threshold, ls='--', c='grey',
                        alpha=0.8, label=thrs_label(threshold))
    # plt.title('histogram')
    plt.xlabel('score')
    plt.ylabel('distrubtion')
    if labels_on:
        plt.legend(loc='upper left', fontsize=15)
    fig = plt.gcf()
    # plt.close()
    return fig  # return the axis

# Accuracy Plot Support Functions


def plot_roc_line(roc_res, axes, label):
    """
    Plots a single roc curve on an already existing axes.
    roc_results : ROC results dictionary object which contains a pandas dataframe, threshold, fpr_thresh and tpr_thresh.
    axes : matplotlib axes object (plot to draw the roc graph on)
    label : label for this line
    """
    roc_df = roc_res.get("roc_df")

    fpr_thresh = roc_res.get("fpr_thresh")
    tpr_thresh = roc_res.get("tpr_thresh")

    axes.semilogx(roc_df['fpr'], roc_df['tpr'], label=label)
    if (fpr_thresh is not None) and (tpr_thresh is not None):
        axes.plot(fpr_thresh, tpr_thresh, marker='x')
    return axes


def roc_plot(roc_results, axes=None, is_verification=True, rankone=False):
    """
    Plots one or more roc curves on a single axes
    roc_results : A dictionary of a ROC Results object which includes a Pandas DataFrame with fpr, tpr, and threshold column, the threshold and fpr/tpr at the threshold.
    axes : An empty axes to draw the roc_plot on, alternatively creates a new axes if none is provided.
    fpr_thresh : fpr at the threshold
    tpr_thresh : tpr at the threshold
    """
    if axes is None:
        fig, ax = plt.subplots()
        axes = ax

    for label in roc_results:
        plot_roc_line(roc_results[label], axes, label)

    if rankone:
        axes.set_title('Alarm Curve (%s)' % label)
        axes.set_ylabel('Alarm Rate')
    else:
        axes.set_title('ROC (%s)' % label)
        if is_verification:
            axes.set_ylabel('Verification Rate')
        else:
            axes.set_ylabel('Idenitifcation Rate')
    axes.set_xlabel('False Accept Rate')

    #  axes.hline(threshold,label='threshold')
    #axes = plt.gca()
    axes.set_ylim([0.6, 1])
    axes.grid(True, linestyle=':', linewidth=0.5)
    axes.legend()
    return axes


def error_plot(roc_res, axes=None, label=''):
    """
    Plots the error curves
    roc_results : ROC results dictionary object which contains a pandas dataframe, threshold, fpr_thresh and tpr_thresh.
    """
    if axes is None:
        fig, ax = plt.subplots()
        axes = ax
    roc_df = roc_res.get("roc_df")
    threshold = roc_res.get("threshold")
    fpr_thresh = roc_res.get("fpr_thresh")
    tpr_thresh = roc_res.get("tpr_thresh")

    axes.semilogy(roc_df['threshold'], roc_df['fpr'], label='FMR')
    axes.semilogy(roc_df['threshold'], 1-roc_df['tpr'], label='FNMR')
    if threshold is not None:
        axes.axvline(threshold, label='threshold', linestyle=":")
        fnmr_t = 1-tpr_thresh
        fmr_t = fpr_thresh
        axes.annotate('FNMR %0.6f' % fnmr_t,
                      ha='center', va='center', textcoords='offset pixels',
                      xytext=(60, -20), xy=(threshold, fnmr_t), arrowprops={'facecolor': 'black', 'width': 0.25, 'headwidth': 6})
        axes.annotate('FMR %0.6f' % fmr_t,
                      ha='center', va='center', textcoords='offset pixels',
                      xytext=(60, 20), xy=(threshold, fmr_t), arrowprops={'facecolor': 'black', 'width': 0.25, 'headwidth': 6})

    axes.set_title('Error versus Threshold '+label)
    axes.set_xlabel('Score')
    axes.set_ylabel('Error Rate')
    axes.grid(True, linestyle=':', linewidth=0.5)
    axes.legend()
    return axes

# Main accuracy plot figure


def plot_acc_res(roc_results, roc_res_adjust=None, label='', is_verification=True, rankone=False):
    """
    Plots the main figure for accuracy graphs. Includes a ROC curve and Error versus threshold curve, can be set to plot alarm curves.
    roc_results : A dictionary with result values
    roc_res_adjust : A dictionary with result values, for a gallery adjusted results.
    is_verification : flag to graph verification data.
    rankone : flag to graph an alarm curve.
    """

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), dpi=80)
    # plt.close()

    roc_res = {f"{label}": roc_results}
    if roc_res_adjust is not None:
        roc_res[f"{label} gallery adjusted"] = roc_res_adjust

    roc_plot(roc_res, ax1, is_verification=is_verification, rankone=rankone)

    if roc_res_adjust is not None:
        error_plot(roc_res_adjust, axes=ax2, label=f'({label} adjusted)')
    else:
        error_plot(roc_results, axes=ax2, label=f'({label})')

    return fig


def plot_CMC_mpl(data, xvals, cdf, rank_col='rank', score_col='score', truth_col='truth'):
    """
    Returns a figure with CMC plot 
    data : columns=['rank','scores',truth]
    xvals : x values of CMC
    cdf : cdf values matching the xvals
    """
    plt.figure(figsize=(12, 7))
    plt.subplot(211)
    plt.plot(xvals, cdf)
    plt.title('CMC')
    plt.xlabel('Rank')
    plt.ylabel('Identification Rate')
    plt.xticks(xvals)
    # plt.set_xlim([0,10])
    plt.grid(True, linestyle=':', linewidth=0.5)
    plt.subplot(212)
    sns.lineplot(x=rank_col, y=score_col, hue=truth_col,
                 data=data)
    plt.xticks(xvals)
    plt.grid(True, linestyle=':', linewidth=0.5)
    fig = plt.gcf()
    # plt.close()
    return fig


def plot_score_box(data, threshold=None, max_rank=20):
    """
    Plot a Score vs Rank box plot (with optional threshold)
    """
    sns.set(style="ticks", palette="pastel")

    sns.boxplot(x="rank", y="scores",
                hue="truth", palette=["m", "g"],  # split=True,inner="box",
                data=data[data['rank'] < max_rank])
    if threshold:
        plt.axhline(threshold, ls='--', c='grey', alpha=0.8)

    sns.despine(offset=10, trim=True)

    plt.title('Rank vs Score')
    plt.xlabel('rank')
    plt.ylabel('score')
    return plt.gca()  # return the axis
