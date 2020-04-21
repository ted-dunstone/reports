from scipy import stats
import pandas as pd
import numpy as np
from sklearn import metrics
from scipy import interpolate


# Accuracy Results Calculations


class Ac_Results:
    def __init__(self):
        self.roc_df = pd.DataFrame()
        self.threshold = None
        self.fpr_thresh = None
        self.tpr_thresh = None
        self.fnr_thresh = None
        self.auc = None

    def calc_roc_df(self, truth, scores):
        """
        truth : series or list of truth values
        scores : series or list of scores values
        """
        fpr, tpr, thresholds = metrics.roc_curve(truth, scores)
        self.set_roc_df(pd.DataFrame(
            {'fpr': fpr, 'tpr': tpr, 'threshold': thresholds}))

    def set_roc_df(self, roc_df):
        if roc_df.shape[0] > 0:
            self.roc_df = roc_df
            self.set_auc()

    def set_auc(self):
        self.auc = metrics.auc(self.roc_df['fpr'], self.roc_df['tpr'])

    def roc_create_func(self, x_col='fpr', y_col='tpr'):
        return interpolate.interp1d(self.roc_df[x_col], self.roc_df[y_col], kind='nearest', bounds_error=False)

    def calc_metrics(self, threshold):
        if (threshold <= self.roc_df['threshold'].max()) or (threshold >= self.roc_df['threshold'].min()):
            tpr_func = self.roc_create_func('threshold', 'tpr')
            fpr_func = self.roc_create_func('threshold', 'fpr')
            self.threshold = threshold
            self.fpr_thresh = fpr_func(threshold)
            self.tpr_thresh = tpr_func(threshold)
            self.fnr_thresh = 1-self.tpr_thresh
            return True
        return False

    def get_metrics(self):
        if self.threshold is not None:
            return {'threshold': self.threshold, 'fpr': '%2.2f' % (self.fpr_thresh*100), 'fnr': '%2.2f' % (self.fnr_thresh*100), 'tpr': '%2.2f' % (self.tpr_thresh*100), 'auc': self.auc}
        else:
            return {'auc': self.auc}

    def roc_table(self, fpr_arry=[0.1, 0.05, 0.01, 0.001, 0.00001], col_name='FMNR'):
        """Given the roc function return a table evaluated at the fpr_arry"""
        r_array = []

        roc_func = self.roc_create_func()

        for fpr_v in fpr_arry:
            r_array.append([fpr_v, 1-roc_func(fpr_v).round(4)])
        rtable = pd.DataFrame(r_array, columns=['FMR', col_name])
        rtable = rtable.set_index('FMR')
        rtable.fillna('', inplace=True)
        return rtable

    def to_dict(self):
        dictionary = {
            "roc_df": self.roc_df,
            "threshold": self.threshold,
            "fpr_thresh": self.fpr_thresh,
            "tpr_thresh": self.tpr_thresh,
            "fnr_thresh": self.fnr_thresh,
            "auc": self.auc
        }
        return dictionary

    def adjust_for_gallery(self, num_probes, gallery_size, num_match, num_non_match):
        """ Modify results to account for gallery size """

        missing_nm_fraction = (num_probes*gallery_size -
                               num_probes)/num_non_match
        missing_m_fraction = num_probes/num_match

        diff = np.log10(self.roc_df['fpr'])-np.log10(missing_nm_fraction)
        self.roc_df['fpr'] = np.power(10, diff)
        self.roc_df['tpr'] = self.roc_df['tpr']/missing_m_fraction


def roc_calc(results, rank_col='rank', truth_col='truth', score_col='score', threshold=None, num_probes=None, gallery_size=None, rankone=False):
    """
    Returns the roc calculation statistics
    Modifies to adjust for candidate list size for a given gallery size
    results : pd.DataFrame() with truth, 'scores', and 'rank' column
    Returns two Ac_Results instances one normal, one with gallery adjustment
    roc_res_adjust returns None if gallery_size is not set
    """
    if rankone:
        results = results[results[rank_col] == 1]

    roc_res = Ac_Results()
    roc_res.calc_roc_df(results[truth_col], results[score_col])
    if threshold is not None:
        roc_res.calc_metrics(threshold)

    # below results are adjusted for Gallery Size
    roc_res_adjust = None
    if gallery_size is not None:
        roc_res_adjust = roc_res
        num_match = results[truth_col].sum()
        num_non_match = len(results)-num_match
        with np.errstate(divide='ignore'):
            roc_res_adjust.adjust_for_gallery(
                num_probes, gallery_size, num_match, num_non_match)
            if threshold is not None:
                roc_res_adjust.calc_metrics(threshold)

    return roc_res, roc_res_adjust


# Calculate CMC table
def calc_CMC(data, total_count, rank_col='rank', score_col='score', truth_col='truth', threshold=None):
    """
    Plot an CMC
    data : pandas dataframe
    total_count : total number of probes
    """

    rank_pivot = data.pivot_table(
        index=rank_col, columns=truth_col, values=score_col, aggfunc=[
            min, max, np.mean, "count"]
    )  # .reset_index()

    def top(g):
        return "%s" % (g.sort_values(by=score_col, ascending=False).head(1).values[0][2:5])

    def bottom(g):
        return "%s" % (g.sort_values(by=score_col, ascending=False).head(1).values[0][2:5])

    rank_ids = data.pivot_table(
        index=rank_col, columns=truth_col, values=[
            score_col], aggfunc=[top, bottom]
    )
    # display(rank_ids)

    rank_output = rank_pivot["count"].rename(
        {True: "Match_Count", False: "False_Match_Count"}, axis="columns")
    rank_score_max = rank_pivot["max"].rename({True: "Match_Max_Score",
                                               False: "False_Match_Max_Score"}, axis="columns")
    rank_score_min = rank_pivot["min"].rename({True: "Match_Min_Score",
                                               False: "False_Match_Min_Score"}, axis="columns")
    rank_score_mean = rank_pivot["mean"].rename({True: "Match_Mean_Score",
                                                 False: "False_Match_Mean_Score"}, axis="columns")
    rank_top = rank_ids["top"].rename({True: "Match_Top",
                                       False: "False_Match_Top"}, axis="columns")
    rank_bottom = rank_ids["bottom"].rename({True: "Match_Bottom",
                                             False: "False_Match_Bottom"}, axis="columns")
    rank_output = rank_output.merge(rank_score_max, on=rank_col)
    rank_output = rank_output.merge(rank_score_min, on=rank_col)
    rank_output = rank_output.merge(rank_score_mean, on=rank_col)
    rank_output = rank_output.merge(rank_top, on=rank_col)
    rank_output = rank_output.merge(rank_bottom, on=rank_col)
    rank_output = rank_output.reset_index()

    hist, _ = np.histogram(
        data[data[truth_col] == True][rank_col].values, bins='auto')

    if total_count is None:
        raise Exception(
            "for calc_CMC() The number of probes used in the test must be supplied")
        # total_count=len(data[c_pid].unique()) #total number of probes.
    cdf = np.cumsum(hist)/total_count
    cdf_show_len = min(len(cdf), 20)
    xvals = range(1, cdf_show_len+1)

    # fig = plot_CMC_mpl(data, cdf, cdf_show_len) #TODO FIG MUST BE MOVED

    return pd.DataFrame({"rank": xvals, "identification rate": cdf[0:cdf_show_len]})


# Main analysis calculations
class Analysis():
    """
    This class contains methods to analyse the data and store the results.
    """

    def __init__(self, dtype, label):
        """
        dtype is the type of the data e.g. "ALL" "1" ...
        label is label of data e.g. "Finger" "Face" "Gate"
        Results to be calculated
        """
        self.dtype = dtype
        self.label = label
        self.data = pd.DataFrame()
        self.threshold = None
        self.gallery_size = None
        self.nr_probes = 0
        self.match_scores = []
        self.non_match_scores = []
        self.accuracy_results = None  # Ac_Results()
        self.ac_res_gallery_adjusted = None  # Ac_Results()
        self.alarm_results = None  # Ac_Results()
        self.alarm_gallery_adjusted = None  # Ac_Results()
        self.accuracy_table = pd.DataFrame()
        self.alarm_table = pd.DataFrame()
        self.cmc_table = pd.DataFrame()

    def analyse(self, data, id_col='probeid', rank_col='rank', score_col='scores', truth_col='truth', threshold=None, gallery_size=None, fpr_arry=[0.1, 0.05, 0.01, 0.001, 0.00001], is_identification=True):
        """
        Perform the main analysis
        data : a pandas Dataframe columns=['probeid','rank','scores','truth']
        externall calls : roc_calc()->Ac_results() calc_CMC()
        """
        if threshold is not None:
            self.threshold = threshold
        if gallery_size is not None:
            self.gallery_size = gallery_size

        self.match_scores = data[data[truth_col] == True][score_col]
        self.non_match_scores = data[data[truth_col] == False][score_col]

        # calculate accuracy results
        unique_probes = len(data[id_col].unique())
        self.nr_probes = unique_probes
        #possibly: df['truth'] = df['truth'].map({True: 1, False: 0})
        res, res_adj = roc_calc(data[[truth_col, score_col]], truth_col=truth_col, score_col=score_col,
                                threshold=threshold, num_probes=unique_probes, gallery_size=gallery_size, rankone=False)
        self.accuracy_results = res
        self.ac_res_gallery_adjusted = res_adj

        # calculate alarm results
        if is_identification:
            a_res, a_res_adj = roc_calc(data[[truth_col, score_col, rank_col]], threshold=threshold,
                                        num_probes=unique_probes, gallery_size=gallery_size, rankone=True)
            self.alarm_results = a_res
            self.alarm_gallery_adjusted = a_res_adj

        # create roc table
        table = self.accuracy_results.roc_table(
            col_name=f'FNMR {self.label} {self.dtype}', fpr_arry=fpr_arry)
        if gallery_size is not None and self.ac_res_gallery_adjusted is not None:
            table2 = self.ac_res_gallery_adjusted.roc_table(
                col_name=f'FNMR {self.label} {self.dtype} gallery_adjusted', fpr_arry=fpr_arry)
            table = table.join(table2)
        table.insert(0, table.index.name, table.index)
        self.accuracy_table = table

        # create alarm table (TODO abstract alarm and roc table)
        if is_identification:
            atable = self.alarm_results.roc_table(
                col_name=f'FNMR {self.label} {self.dtype}', fpr_arry=fpr_arry)
            if gallery_size is not None and self.ac_res_gallery_adjusted is not None:
                atable2 = self.alarm_gallery_adjusted.roc_table(
                    col_name=f'FNMR {self.label} {self.dtype} gallery_adjusted', fpr_arry=fpr_arry)
                atable = atable.join(atable2)
            atable.insert(0, atable.index.name, atable.index)
            self.alarm_table = atable

            self.cmc_table = calc_CMC(data[[id_col, rank_col, truth_col, score_col]], unique_probes,
                                      rank_col=rank_col, score_col=score_col, truth_col=truth_col, threshold=threshold)

        self.data = data


# Outlier Functions
def return_outliers_zscore(df, col, truth_col, sign, max_num, threshold=3):
    in_array = df[df[truth_col] == sign]
    zscore = stats.zscore(in_array[col])
    if sign:
        sel = in_array[(zscore < -threshold)]
    else:
        sel = in_array[(zscore >= threshold)]

    return sel.sort_values(col, ascending=sign)[0:max_num]


def return_outliers_quantile(df, col, truth_col, sign, max_num, threshold=0.005):
    in_array = df[df[truth_col] == sign]
    if not sign:
        threshold = 1-threshold
    qscore = in_array[col].quantile(threshold)
    if sign:
        sel = in_array[in_array[col] < qscore]
    else:
        sel = in_array[in_array[col] >= qscore]

    return sel.sort_values(col, ascending=sign)[0:max_num]


def calc_outliers(df, score_col='scores', truth_col='truth', rank_col='rank', ft='', errors=[]):
    try:
        outlier_table1 = return_outliers_quantile(
            df, score_col, truth_col, True, 10)  # match outliers
        outlier_table2 = return_outliers_quantile(
            df, score_col, truth_col, False, 10)  # non-match outliers
        rank_1_results = df[df[rank_col] == 1]
        outlier_table3 = return_outliers_quantile(
            rank_1_results, score_col, truth_col, True, 10)  # match outliers rank 1
        outlier_table4 = return_outliers_quantile(
            rank_1_results, score_col, truth_col, False, 10)  # non-match outliers rank 1
    except Exception as ex:
        errors.append(
            f"For {ft} type, unable to calculate outliers due to exception: {ex}")
    return [outlier_table1, outlier_table2, outlier_table3, outlier_table4]

# Functions to calculate edge cases
def biometric_misses(score_data, truth_table, rpid_col='probeid', rgid_col='galleryid', tpid_col='probeid', tgid_col='galleryid', truth_col='truth'):
    r_merge_df = pd.merge(score_data, truth_table, how='right', left_on=[
                          rpid_col, rgid_col], right_on=[tpid_col, tgid_col], indicator=True)
    biometric_miss_df = r_merge_df[r_merge_df['_merge'] == 'right_only']
    biometric_miss_df.drop(labels='_merge', axis='columns', inplace=True)
    biometric_miss_df = biometric_miss_df[biometric_miss_df[truth_col] == True]
    biometric_miss_df.dropna(inplace=True, axis='columns')
    return biometric_miss_df


def alternative_registration(truth_table, score_data, truth_id_col='galleryepi', res_id_col='galleryepi', rpid_col='probeid', rgid_col='galleryid', tpid_col='probeid', tgid_col='galleryid'):
    """
    truth_id_col : different id column (for gallery in truth table) than tgid
    res_id_col : different id column (for gallery in results file) than rgid
    """
    alt_reg = pd.DataFrame()
    if (truth_id_col is not None) and (res_id_col is not None):
        alt_reg = score_data[score_data[rpid_col].isin(truth_table[tpid_col]) & score_data[res_id_col].isin(
            truth_table[truth_id_col]) & (~score_data[rgid_col].isin(truth_table[tgid_col]))]
        alt_reg.dropna(axis='columns', inplace=True)
    return alt_reg


def missing_score(df, score_col='scores'):
    lmissing = pd.DataFrame()
    if df.dtypes[score_col] == object:
        lmissing = df[df[score_col].str.replace(
            '.', '', 1).str.isdigit().apply(lambda x: not x)]
    nullscore = df[df[score_col].isnull()]
    no_score = pd.concat([lmissing, nullscore])
    return no_score


def finger_pos_check(df, ppos_col='ppos', gpos_col='gpos'):
    known_df = df[df[ppos_col] != 'Unknown'][df[gpos_col] != 'Unknown']
    diff_df = known_df[known_df[ppos_col] != known_df[gpos_col]]
    return diff_df


def mrr_check(df, probeid_col='probemrr', galleryid_col='gallerymrr'):
    identical_mrr = df[df[probeid_col] == df[galleryid_col]]
    return identical_mrr


def match_mrr_check(df, flag, probeid_col='probeid', galleryid_col='galleryid', check_galleryid_col='gallerymrr', truth_col='truth', ppos_col='ppos'):
    flaged_dfs = []
    # split into pairs of probes and gallerys
    for match in df[df[truth_col] == True].groupby([probeid_col, galleryid_col]):
        df_check = match[1]
        # TODO find better way to handle probeid/probemrr.
        nr_same = df_check[df_check[probeid_col] ==
                           df_check[check_galleryid_col]].shape[0]
        nr_total = df_check.shape[0] - \
            df_check[df_check[ppos_col] == 'ALL'].shape[0]
        if (nr_same/nr_total) >= flag:
            flaged_dfs.append(df_check)
    return flaged_dfs

# Functions to calculate summary data for the introduction
def candidate_length(data, pid_col='probeid', rank_col='rank', is_identification=True):
    if is_identification:
        # code for finding minimum and maximum candidate length
        c_lengths = []
        # record the maximum rank for each probe.
        for p in data[pid_col].unique():
            can_len = data[data[pid_col] == p][rank_col].max()
            c_lengths.append(can_len)
        c_lengths = np.array(c_lengths)
        max_length = c_lengths.max()
        min_length = c_lengths.min()
    else:
        max_length = 'no candidates'
        min_length = 'no candidates'
    return {"max_length": max_length, "min_length": min_length}


def counts(data, pid_col='probeid', truth_col='truth'):
    unique_probes = len(data[pid_col].unique())
    total_matches = data[data[truth_col] == True][truth_col].size
    total_non_matches = data[data[truth_col] != True][truth_col].size
    total_nr = data[truth_col].size
    return {
        "unique_probes": unique_probes,
        "total_matches": total_matches,
        "total_non_matches": total_non_matches,
        "total_nr": total_nr
    }


def scores_summary(data, score_col='score', truth_col='truth'):
    # Initial score analysis.
    positives = data[data[truth_col] == True][score_col]
    negatives = data[data[truth_col] == False][score_col]
    # calculate extreme outliers
    pq1, pq3 = positives.quantile([0.25, 0.75])
    px = pq1 - (pq3-pq1)*3
    nq1, nq3 = negatives.quantile([0.25, 0.75])
    nx = nq3 + (nq3-nq1)*3
    return {
        "min_pos_score": positives.min(),
        "max_neg_score": negatives.max(),
        "pos_score_05": positives.quantile(0.05, interpolation='lower'),
        "pos_score_95": positives.quantile(0.95, interpolation='lower'),
        "neg_score_05": negatives.quantile(0.05, interpolation='lower'),
        "neg_score_95": negatives.quantile(0.95, interpolation='lower'),
        "nr_pos_eo": len(positives[positives < px]),
        "nr_neg_eo": len(negatives[negatives > nx])
    }
