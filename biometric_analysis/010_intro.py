from datetime import datetime, timedelta
from textwrap import dedent
import data

_, _, _, _, mets, params = data.get(reload_data=True)

from px_build_doc.util import update_vars


#Title
date = datetime.today().strftime('%d %B %Y')

pvars= {"data_type":params.data_type, 
        "test_type":params.test_type, 
        "date":date, 
        }

for m in ["unique_probes","max_length","min_length","total_matches","total_non_matches","total_nr","min_pos_score","max_neg_score","pos_score_05","pos_score_95","neg_score_05","neg_score_95","nr_pos_eo","nr_neg_eo"]:
    if type(mets[m])==type(float):
        pvars[m]="%.2f"%mets[m]
    else:
        pvars[m]=str(mets[m])

update_vars(pvars)

