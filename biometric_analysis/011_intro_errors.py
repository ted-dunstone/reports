from px_build_doc.util import fetch_vars


mets=fetch_vars()

print("## Errors")

if(int(mets["nr_pos_eo"]) == 0):
    print(r"\warningbox{")
    print(f"{mets['nr_pos_eo']} extreme outlier(s) were found for the match data. These are scores that have been found to be unusually low for a match. Please see the outliers section in the appendix at the end of the report for details.")
    print(r"}")
if(int(mets["nr_neg_eo"]) > 0):
    print(r"\warningbox{")
    print(f"WARNING: {mets['nr_neg_eo']} extreme outlier(s) were found for the non-match data. These are scores that have been found to be unusually high for a non-match. Please see the outliers section in the appendix at the end of the report for details.")
    print(r"}")

print(r"\notebox{There are no warnings present for this data}")

