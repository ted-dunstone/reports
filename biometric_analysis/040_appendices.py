from textwrap import dedent
import data

data_df, col, results, outliers, metrics, params = data.get()

c_pid = col['pid']
c_gid = col['gid']
c_rank = col['rank']
c_score = col['score']
c_truth = col['truth']
c_ppos = col['ppos']
c_gpos = col['gpos']

def print_outliers(outliers, ft, errors):
    try:
        selec = [c_rank, c_pid, c_gid, c_ppos, c_gpos, c_score, c_truth]
        if len(outliers) == 4:
            if outliers[0].shape[0] > 0 or outliers[1].shape[0] > 0 or outliers[2].shape[0] > 0 or outliers[3].shape[0] > 0:
                print(dedent(f""" 
                    ## Outliers for type {ft}
                    The following tables show any outlier cases for high non-matches and low matches. 
                    The tables below are for combined matches.    
                """))

            if outliers[0].shape[0] > 0:
                tables.render(outliers[0][selec],"Match Outliers, combined results (ALL)")

            if outliers[1].shape[0] > 0:
                tables.render(outliers[1][selec],"Non-Match Outliers, combined results (ALL)")

            if outliers[2].shape[0] > 0:
                tables.render(outliers[2][selec],"Match Outliers, combined results (Rank 1)")

            if outliers[3].shape[0] > 0:
                tables.render(outliers[3][selec],"Non-Match Outliers, combined results (Rank 1)")
    except Exception as ex:
        errors.append(f"For {ft} type, unable to output Outlier analysis due to exception: {ex}")