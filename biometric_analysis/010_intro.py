from datetime import datetime, timedelta
from textwrap import dedent
import data

_, _, _, _, mets, params = data.get(reload_data=True)

#Title
date = datetime.today().strftime('%d %B %Y')
print(f"# {params.data_type} for {params.test_type} ({date})")

#Introduction
print(f"This report provides analysis of the {params.data_type} for {params.test_type} including estimation of accuracy and identification of outliers.")
    
print("A summary of the matching data used to generate this report is shown below.")

print(dedent(f"""
    * Number of unique probe IDs: {mets["unique_probes"]}
    * Maximum candidate length: {mets["max_length"]}
    * Minimum candidate length: {mets["min_length"]}
    * Total number of matches: {mets["total_matches"]}
    * Total number of non-matches: {mets["total_non_matches"]}
    * Total number of rows in data file: {mets["total_nr"]}
    * Minimum match score: {mets["min_pos_score"]}
    * Maximum non-match score: {mets["max_neg_score"]}
    * Match score 5% quantile: {mets["pos_score_05"]}
    * Match score 95% quantile: {mets["pos_score_95"]}
    * Non-match score 5% quantile: {mets["neg_score_05"]}
    * Non-match score 95% quantile: {mets["neg_score_95"]}
    
    These values were calculated using the data from all fingerprint types (including type 'ALL' and all numbered positions).
    """))
    
if(mets["nr_pos_eo"] > 0):
    print(f"WARNING: {mets['nr_pos_eo']} extreme outlier(s) were found for the match data. These are scores that have been found to be unusually low for a match. Please see the outliers section in the appendix at the end of the report for details.")
if(mets["nr_neg_eo"] > 0):
    print(f"WARNING: {mets['nr_neg_eo']} extreme outlier(s) were found for the non-match data. These are scores that have been found to be unusually high for a non-match. Please see the outliers section in the appendix at the end of the report for details.")
