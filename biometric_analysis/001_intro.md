# Introduction

This report provides an comprenhsive analysis of the {{data_type}} for *{{test_type}}*. This includes the estimation of accuracy and identification of outliers. The report was run on {{date}}.



## Summary Counts

A summary of the imported matching data used to generate this report is shown in table \ref{summary_counts}.

| Attribute     | Counts  |
| ------------- | -----:|
| Number of unique probe IDs    | {{unique_probes}}
| Number of matches      | {{total_matches}} |
| Number of non-matches      | {{total_non_matches}} |
| Total rows      | {{total_nr}} |

Table: Summary Data Counts \label{summary_counts}

## Summary Score Attributes

A summary of the imported matching data overall score ranges for match and non match data is shown in table \ref{summary_score}. This shows the extent to which the match and non-match ranges overlap.

| Attribute     | Score  1| Score  2|
| ------------- | -----:| -----:|
| Maximum non-match score  | {{max_neg_score}} | |
| Minimum match score      | | {{min_pos_score}} |
| Match score   (5%,95%) quantile  | {{pos_score_05}} |  {{pos_score_95}}|
| Non-match Match score  (5%,95%) quantile   |  {{neg_score_05}} | {{neg_score_95}}|

Table: Summary Score Ranges Counts \label{summary_score}

The maximum candidate length was {{max_length}} (min length {{min_length}}).

These values were calculated using the data[^1] from all fingerprint types (including type 'ALL' and all numbered positions).

[^1]: Data imported at {{date}}.
