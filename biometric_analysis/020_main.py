import matplotlib.pyplot as plt
from textwrap import dedent
from px_display import plot_match_dist_mpl, plot_acc_res, plot_CMC_mpl, plot_Zoo_mpl,  plot_score_box
from px_build_doc.util import FigureManager, TableManager, fetch_var, display
import data

from px_build_doc.util import set_temp_dir
set_temp_dir()

plt.rcParams['font.family'] = 'serif'

_, results, _ = data.get()

col = fetch_var("column_names")
c_pid = col['pid']
c_gid = col['gid']
c_rank = col['rank']
c_score = col['score']
c_truth = col['truth']
c_ppos = col['ppos']
c_gpos = col['gpos']

figs = FigureManager()
tables = TableManager()

# Display functions


def print_test_info(test_size, label, instance):
    display(f"""
        This section desacribes the performance parameters for {label} {instance}. There are {test_size} probes in this test set.
    """)


def print_performance(roc_results, ft, errors):
    # try:
    threshold = roc_results.threshold
    if threshold is not None:
        fpr_t = roc_results.fpr_thresh
        tpr_t = roc_results.tpr_thresh
        fnr_t = roc_results.fnr_thresh
        display(dedent("""
                ## Performance at the threshold of *%.1f*

                * False Positive Rate: *%2.2f* %%
                * False Negative Rate: *%2.2f* %%
                * True Positive Rate: *%2.2f* %%
            """ % (threshold, fpr_t*100, fnr_t*100, tpr_t*100)))
    # except Exception as ex:
    #    errors.append(f"For {ft} type, unable to print performance analysis due to exception: {ex}")


def print_match_dist(matches, non_matches, threshold, label, errors):

    # try:
    display("""      
            * Count of Matches: **%s**
            * Count of Non-Matches: **%s**
        """ % (
        len(matches),
        len(non_matches)
    ))

    plot_match_dist_mpl(matches, non_matches, threshold=threshold)
    plt.show()
    figs.save_plot("Match Distribution " + f"({label})", height=9).display()
    # except Exception as ex:
    #    errors.append(f"Unable to output Distribution Plot due to exception {label} : {ex}")


def print_acc_plot(roc_results, roc_res_adjust=None, label='', is_verification=True, rankone=False, errors=[]):
    # try:
    if roc_results is not None:
        roc_res_adj_dict = roc_res_adjust.to_dict() if roc_res_adjust is not None else None
        plot_acc_res(roc_results.to_dict(), roc_res_adj_dict,
                     label, is_verification, rankone)

        title = "Reciever Operating Curve"
        if rankone:
            title = "Alarm Curve"
        plt.show()
        figs.save_plot(title + f" ({label})", height=7).display()
    # except Exception as ex:
    #    errors.append(f"For {label} type, unable to output ROC plot due to exception: {ex}")


def print_cmc_curve(data, table, label, errors):
    # try:
    plot_CMC_mpl(data[[c_rank, c_score, c_truth]], table[c_rank],
                 table['identification rate'], c_rank, c_score, c_truth)
    plt.show()
    figs.save_plot("Cumulative Matching Curve" +
                   f"({label})", height=9).display()

    #tables.read_df(table).display("Identification Results by Rank")
    # except Exception as ex:
    #    errors.append(f"For {label} type, unable to output CMC plot due to exception: {ex}")


def proportion_to_description(value, total, label, less_than=[
    (1.0, "As some outliers are expected this is not concerning, however it may be worth investigating."),
    (2.0, "This is worth examining more closely to see if these represent individuals with similar attributes.")
]):
    proportion = 100.0*(value/total)
    analysis = f"The proportion of {label} in the results is less than {'%2.2f'%proportion} %."
    for t in less_than:
        if (proportion < t[0]):
            analysis += t[1]
            break
    return analysis


def print_zoo_plot(zoo_results, label='', theshold=2000):
    outliers = plot_Zoo_mpl(zoo_results, 100)
    display("""
The zoo plot displays how different people perform based on their average match score and their average non-match score. 
Each point represents a single individual and a good system will have few outliers. 
It can be used to investigate which people or groups of people are causing more system errors when additional metadata is available.
In the tables below scores are shown in bold when they are above the threshold if a non-match and below the threshold for a match.
    """)
    figs.save_plot("Zoo Plot" + f"({label})", height=9).display()
    out = outliers[["id", "zoo_class", "false_match_score",
                    "match_score", "false_match_score_max"]]
    classes = {
        "dove": "Individuals classified as doves work the best with this algorithm  as they verify easily and are more difficult to impost",
        "chameleon": "Indviduals classified as chameleons may have very generic features weighted heavily by the algorithm",
        "worm": "Indviduals classified as worms work the worst with the algorithm as they have difficulty verifying and are easily imposted",
        "phantom": "Indviduals classified as phantoms may have very unique features and match poorly in all cases"
    }
    for zoo_class in classes.keys():
        filtered = out[out["zoo_class"] == zoo_class]

        def fm_score(s, greater=True):
            if greater:
                return "**%r**" % s if s >= theshold else str(s)
            else:
                return "**%r**" % s if s <= theshold else str(s)

        def highlight(col_name, greater):
            return [fm_score(s, greater) for s in filtered[col_name]]

        if len(filtered) > 0:
            # filtered["match_score"]=highlight("match_score",False)
            # filtered["false_match_score"]=highlight("false_match_score",True)
            # filtered["false_match_score_max"]=highlight("false_match_score_max",True)
            title = zoo_class+'s'
            display(f"""
* **{title.title()}**

{classes[zoo_class]}. {proportion_to_description(len(filtered),len(zoo_results),title)}.

""")
            tables.read_df(filtered).display(f"Zoo analysis {title} ({label})")

# def print_score_box(df, threshold, ft, errors):
#     try:
#         df_renamed = df.rename(columns={c_rank:'rank', c_truth:'truth', c_score:'scores'})
#         plot = plot_score_box(df_renamed,threshold=threshold)
#         display(figs.fig_latex(bp_img_fn,"Rank vs Score"))
#     except Exception as ex:
#         errors.append(f"For {ft} type, unable to output score boxplot (may be incomplete rank information) due to exception: {ex}")
#        errors.append(f"For {ft} type, unable to output CMC plot due to exception: {ex}")


def print_score_box(df, threshold, ft, errors):
    # try:
    df_renamed = df.rename(
        columns={c_rank: 'rank', c_truth: 'truth', c_score: 'scores'})
    plot = plot_score_box(df_renamed, threshold=threshold)
    bp_img_fn = "boxplot.png"
    plt.tight_layout()
    # plt.savefig(bp_img_fn)
    # plt.close()
    figs.save_plot("Rank vs Score", height=9).display()
    # except Exception as ex:
    #    errors.append(f"For {ft} type, unable to output score boxplot (may be incomplete rank information) due to exception: {ex}")


finger_types = fetch_var("finger_types")
is_identification = True  # TODO implement way to identify identification
is_verification = not is_identification
errors = []

# Main Analysis.
for ft in finger_types:
    dres = results[ft]

    plot_label = f'{dres.label} {dres.dtype}'

    display(f"# {fetch_var('label')} type {ft}")

    print_test_info(dres.nr_probes, fetch_var('label'), ft)

    print_performance(dres.accuracy_results, ft, errors)

    display("## Analysis")

    display("### Match distribution")
    display(dedent("""
        The match distribution shows the frequency of matches and non matches versus the threshold.
    """))
    print_match_dist(dres.match_scores, dres.non_match_scores,
                     dres.threshold, ft, errors)

    display("### Accuracy")
    if dres.accuracy_results.auc == 1:
        display(
            "Non-Match and match results have no overlap. There are hence no errors at an optimal threshold.")
    else:
        # ROC curve
        display(dedent("""
            The ROC Curve below shows the change in accuracy (verification rate vs false accept) as the threshold is changed. The graph on the right shows the changes to the individual error rates with respect to the score.
            Note the accuracy is calculated using the available data provided which does not account for the full gallery size. As a consequence the evaluated accuracy rate here is likely to be worse than the true accuracy rate.
        """))
        if dres.gallery_size is not None:
            display(dedent("""
                The graphs below show an accuracy adjusted curve using the gallery size provided.
            """))
        print_acc_plot(dres.accuracy_results, dres.ac_res_gallery_adjusted,
                       label=plot_label, rankone=False, is_verification=is_verification)
        display(dedent("""
            The following table shows false non-match rates and gallery adjusted values (if calculated) as evaluated at specific false match rates using the ROC curve.
        """))
        tables.read_df(dres.accuracy_table).display(
            f"False Match vs False Non-Match ({plot_label})")

        # Alarm curve
        if is_identification and (dres.alarm_results is not None):
            display(dedent("""
                The Alarm Curve shows accuracy rate for the rank 1 results. This corresponds to how often the system would falsely alarm with the highest matching result for different thresholds.
            """))
            print_acc_plot(dres.alarm_results, dres.alarm_gallery_adjusted,
                           label=plot_label, rankone=True, is_verification=is_verification)
            display(dedent("""
                The following table shows false non-match rates and gallery adjusted values (if calculated) as evaluated at specific false match rates using the Alarm curve.
            """))
            tables.read_df(dres.alarm_table).display(
                f"False Match vs False Non-Match ({plot_label})")

    if is_identification:
        display("### Cumulative Match Curve")
        display(dedent("""
            The Cumulative Match Curve shows the identification as a function of the rank (or candidate list size). The plot below displays the match and non-match scores versus the rank (shaded area shows the distribution range).
        """))
        print_cmc_curve(dres.data, dres.cmc_table,
                        label=plot_label, errors=errors)

        display('### Zoo Analysis')

        print_zoo_plot(dres.zoo_result, plot_label)

        #tables.read_df(dres.zoo_result).display(f"Zoo Analysis ({plot_label})")

        display("### Rank versus Score Box Plot")
        display(dedent("""
            The Rank versus Score Box Plot shows a box plot of the match (truth=1) and non-match (truth=0) score ranges versus rank. The dotted line represents the set threshold.
        """))
        print_score_box(dres.data, dres.threshold, ft, errors)
