from textwrap import dedent
from px_build_doc.util import display, fetch_var, TableManager
import data

_, _, outliers = data.get()

tables = TableManager()

finger_types = fetch_var("finger_types")

col = fetch_var("column_names")
c_pid = col['pid']
c_gid = col['gid']
c_rank = col['rank']
c_score = col['score']
c_truth = col['truth']
c_ppos = col['ppos']
c_gpos = col['gpos']

def print_outliers(outliers, ft):
    selec = [c_rank, c_pid, c_gid, c_ppos, c_gpos, c_score, c_truth]
    if len(outliers) == 4:
        if outliers[0].shape[0] > 0 or outliers[1].shape[0] > 0 or outliers[2].shape[0] > 0 or outliers[3].shape[0] > 0:
            display(dedent(f""" 
                ## Outliers for type {ft}
                The following tables show any outlier cases for high non-matches and low matches. 
                The tables below are for combined matches.    
            """))

        if outliers[0].shape[0] > 0:
            tables.read_df(outliers[0][selec]).display("Match Outliers, combined results (ALL)",showindex=True)

        if outliers[1].shape[0] > 0:
            tables.read_df(outliers[1][selec]).display("Non-Match Outliers, combined results (ALL)",showindex=True)

        if outliers[2].shape[0] > 0:
            tables.read_df(outliers[2][selec]).display("Match Outliers, combined results (Rank 1)",showindex=True)

        if outliers[3].shape[0] > 0:
            tables.read_df(outliers[3][selec]).display("Non-Match Outliers, combined results (Rank 1)",showindex=True)

# Outliers
display("# Appendices")
for ft in finger_types:
    print_outliers(outliers[ft], ft)