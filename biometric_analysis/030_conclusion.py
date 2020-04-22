from textwrap import dedent
import pandas as pd
from px_build_doc.util import display, fetch_var, TableManager
import data

_, _, results, _, _, _ = data.get()

tables = TableManager()

finger_types = fetch_var("finger_types")

#Conclusion

display(dedent(f"""
    # Conclusion
    Performed analysis on {len(finger_types)} finger types.
    """))

conclsn_table = pd.DataFrame(columns=['Finger Type','Test Size (Probes)', 'FPR', 'AUC'])

for ft in finger_types:
    dres = results[ft]
    conclsn_table.loc[ft] = [ft, f'{dres.nr_probes}', f'{dres.accuracy_results.fpr_thresh}', f'{dres.accuracy_results.auc:.3f}']

tables.read_df(conclsn_table).display(f"Summary of analysis performed.")


# display(dedent(f"""
# * Analysis completed with {len(errors)} errors and {missing_score_df.shape[0]} records with missing score data.
# """))
version = 1.0
display(dedent(f"""
    * This report was generated using the Performix script version {version}.
    """))