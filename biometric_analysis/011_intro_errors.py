from px_build_doc.util import fetch_vars
from px_build_doc.util import display, FigureManager
import data

mets=fetch_vars()

print("## Issues and Warings")

if(int(mets["nr_pos_eo"]) == 0):
    print(r"\warningbox{")
    print(f"{mets['nr_pos_eo']} extreme outlier(s) were found for the match data. These are scores that have been found to be unusually low for a match. Please see the outliers section in the appendix at the end of the report for details.")
    print(r"}")
if(int(mets["nr_neg_eo"]) > 0):
    print(r"\warningbox{")
    print(f"WARNING: {mets['nr_neg_eo']} extreme outlier(s) were found for the non-match data. These are scores that have been found to be unusually high for a non-match. Please see the outliers section in the appendix at the end of the report for details.")
    print(r"}")

print(r"\notebox{There are no warnings present for this data}")

print("## Structure")

figs = FigureManager()

data_df, col, results, outliers, metrics, params = data.get()
finger_types = data.get_finger_types(data_df, col, params.show_types)

mindmap ="""
*[#Orange] <&globe> Analysis
"""
#Main Analysis.
for ft in finger_types:
    dres = results[ft]
    mindmap+=f"""
** {ft}
*** number of probes {dres.nr_probes}
"""

figs.set_uml("mindmap","The Performix Pipeline",uml=mindmap).display()
