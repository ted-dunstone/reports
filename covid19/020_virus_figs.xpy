# Load the support variables
from px_build_doc.util import fetch_query, TrendsManager, FigureManager
import statistics
import pandas

query=fetch_query()
#query="corona virus"
pytrends = TrendsManager().query(query)

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'serif'

all_geo=pytrends.interest_over_time()

ax1=None
lastvals={}
for country in ['CH','IT','AU','KR','ID','GB','NZ','JP','US','SG']:
  df=pytrends.query(query,geo=country).interest_over_time()
  if len(df)!=len(all_geo):
    continue
  df[query]=df[query]-all_geo[query]
  df=df.rename(columns={query:country})
  try:
    if ax1 is None:
      ax1=df.plot(figsize=(14,7))
    else:
      df.plot(ax=ax1)
    lastvals[country]=statistics.mean(df[country].values[-3:])
  except:
     print("error")
     pass

figs = FigureManager()
figs.save_plot("Trend 2",height=7).display()

pandas.DataFrame.from_dict(lastvals, orient='index').sort_values(by=0,ascending=False).plot.bar(y=0,legend=False,figsize=(14,7))
figs.save_plot("Current Issues",height=7).display()

pytrends.query(query,timeframe='today 3-m').interest_over_time()

try:
  pytrends.related_queries().plot.pie(y='value',legend=False, figsize=(14,7))
  figs.save_plot("BBB This shows the trend of the cororna virus by country",height=9).display()
except:
  pass

print("temp")