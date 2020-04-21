from textwrap import dedent
from PxS_display import plot_match_dist_mpl, plot_acc_res, plot_CMC_mpl
#from pxlib.util.display import plot_score_box
from px_build_doc.util import FigureManager, TableManager
import data

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'serif'

data_df, col, results, outliers, metrics, params = data.get()

c_pid = col['pid']
c_gid = col['gid']
c_rank = col['rank']
c_score = col['score']
c_truth = col['truth']
c_ppos = col['ppos']
c_gpos = col['gpos']

figs = FigureManager()
tables = TableManager()

#Display functions
def print_test_info(test_size):
    print(dedent("""
        Test Size: *%d* probes
    """%(test_size)))

def print_performance(roc_results, ft, errors):
    try:
        threshold = roc_results.threshold
        if threshold is not None:
            fpr_t = roc_results.fpr_thresh
            tpr_t = roc_results.tpr_thresh
            fnr_t = roc_results.fnr_thresh
            print(dedent("""
                ## Performance at the threshold of *%.1f*

                * False Positive Rate: *%2.2f* %%
                * False Negative Rate: *%2.2f* %%
                * True Positive Rate: *%2.2f* %%
            """%(threshold,fpr_t*100,fnr_t*100,tpr_t*100)))
    except Exception as ex:
        errors.append(f"For {ft} type, unable to print performance analysis due to exception: {ex}")

def print_match_dist(matches, non_matches, threshold, ft, errors):
    display_text = ""
    match_img_fn = 'match.png'

    try:
        print(dedent("""      
            * Count of Matches: **%s**
            * Count of Non-Matches: **%s**
        """%(
            len(matches),
            len(non_matches)
            )))

        fig = plot_match_dist_mpl(matches, non_matches, threshold=threshold)
        fig.savefig(match_img_fn,dpi=250)
        print(figs.fig_latex(match_img_fn, "Match Distribution"))
    except Exception as ex:
        errors.append(f"Unable to output Distribution Plot due to exception: {ex}")

def print_acc_plot(roc_results, roc_res_adjust=None, label='', is_verification=True, rankone=False, errors=[]):
    roc_img_fn = 'roc_new.png'
    try:
        roc_res_adj_dict = roc_res_adjust.to_dict() if roc_res_adjust is not None else None
        fig = plot_acc_res(roc_results.to_dict(), roc_res_adj_dict, label, is_verification, rankone)
        fig.savefig(roc_img_fn,dpi=250)
        title = "Reciever Operating Curve"
        if rankone:
            title = "Alarm Curve"
        print(figs.fig_latex(roc_img_fn, title))
    except Exception as ex:
        errors.append(f"For {label} type, unable to output ROC plot due to exception: {ex}")

def print_cmc_curve(data, table, ft, errors):
    try:
        fig = plot_CMC_mpl(data[[c_rank, c_score, c_truth]], table[c_rank], table['identification rate'], c_rank, c_score, c_truth)
        cmc_img_fn = "cmc.png"
        fig.savefig(cmc_img_fn,dpi=250)
        print(figs.fig_latex(cmc_img_fn,"Cumulative Matching Curve"))
        tables.read_df(table).display("Identification Results by Rank")
    except Exception as ex:
        errors.append(f"For {ft} type, unable to output CMC plot due to exception: {ex}")


# def print_score_box(df, threshold, ft, errors):
#     try:
#         df_renamed = df.rename(columns={c_rank:'rank', c_truth:'truth', c_score:'scores'})
#         plot = plot_score_box(df_renamed,threshold=threshold)
#         bp_img_fn = "boxplot.png"
#         plt.tight_layout()
#         plt.savefig(bp_img_fn)
#         plt.close()
#         print(figs.fig_latex(bp_img_fn,"Rank vs Score"))
#     except Exception as ex:
#         errors.append(f"For {ft} type, unable to output score boxplot (may be incomplete rank information) due to exception: {ex}")



finger_types = data.get_finger_types(data_df, col, params.show_types)
is_identification = True #TODO implement way to identify identification
is_verification = not is_identification
errors = []

#Main Analysis.
for ft in finger_types:
    dres = results[ft]
    
    print(f"# {params.label} type {ft}")
    
    print_test_info(dres.nr_probes)
    
    print_performance(dres.accuracy_results, ft, errors)
    
    print("## Analysis")
    
    print("### Match distribution")
    print(dedent("""
        The match distribution shows the frequency of matches and non matches versus the threshold.
    """))
    print_match_dist(dres.match_scores, dres.non_match_scores, dres.threshold, ft, errors)
    
    print("### Accuracy")
    if dres.accuracy_results.auc == 1:
        print("Non-Match and match results have no overlap. There are hence no errors at an optimal threshold.")
    else:
        #ROC curve
        print(dedent("""
            The ROC Curve below shows the change in accuracy (verification rate vs false accept) as the threshold is changed. The graph on the right shows the changes to the individual error rates with respect to the score.
            Note the accuracy is calculated using the available data provided which does not account for the full gallery size. As a consequence the evaluated accuracy rate here is likely to be worse than the true accuracy rate.
        """))
        if dres.gallery_size is not None:
            print(dedent("""
                The graphs below show an accuracy adjusted curve using the gallery size provided.
            """))
        print_acc_plot(dres.accuracy_results, dres.ac_res_gallery_adjusted, label=f'{dres.label} {dres.dtype}', rankone=False, is_verification=is_verification)
        print(dedent("""
            The following table shows false non-match rates and gallery adjusted values (if calculated) as evaluated at specific false match rates using the ROC curve.
        """))
        tables.read_df(dres.accuracy_table).display("False Match vs False Non-Match")
        
        #Alarm curve
        if is_identification:
            print(dedent("""
                The Alarm Curve shows accuracy rate for the rank 1 results. This corresponds to how often the system would falsely alarm with the highest matching result for different thresholds.
            """))
            print_acc_plot(dres.alarm_results, dres.alarm_gallery_adjusted, label=f'{dres.label} {dres.dtype}', rankone=True, is_verification=is_verification)
            print(dedent("""
                The following table shows false non-match rates and gallery adjusted values (if calculated) as evaluated at specific false match rates using the Alarm curve.
            """))
            tables.read_df(dres.alarm_table).display("False Match vs False Non-Match")

    if is_identification:
        print("### Cumulative Match Curve")
        print(dedent("""
            The Cumulative Match Curve shows the identification as a function of the rank (or candidate list size). The plot below displays the match and non-match scores versus the rank (shaded area shows the distribution range).
        """))
        print_cmc_curve(dres.data, dres.cmc_table, ft, errors)
    
        # print("### Rank versus Score Box Plot")
        # print(dedent("""
        #     The Rank versus Score Box Plot shows a box plot of the match (truth=1) and non-match (truth=0) score ranges versus rank. The dotted line represents the set threshold.
        # """))
        # print_score_box(dres.data, dres.threshold, ft, errors)