from px_build_doc.util import WikipediaManager,fetch_query

wiki = WikipediaManager().query(fetch_query()).display()

"""@ UML Test"""
from px_build_doc.util import display, FigureManager

figs = FigureManager()

from collections import Counter
#tree = wiki.links_tree(max_level=1)
links=sorted(wiki.links())
single_words=[]
double_words=[]
all_words=[]
for link in links:
    single_words.append(link.split(' ')[0])
    double_words.append(' '.join(link.split(' ')[0:2]))
    all_words.extend(link.split(' '))
    #common_path = os.path.commonprefix(links[l_num:l_num+2])
    #common_path = links(l_num).split(' ')[-1] - 
    #if len(common_path)>3:
    #    common_paths.append(common_path)
#list_set = set(common_paths) 
#common_paths = (list(list_set)) 
#print(Counter(all_words).most_common(30))
md=wiki.full_page()

md="\n".join([' '.join(s.split()[:-1]).replace('=','#') if s.startswith('=') else s for s in md.splitlines()])
print(md)
#print(Counter(double_words).most_common(10))
#for key,val in Counter(double_words).most_common(10):
#    out+=out

#figs.set_uml("mindmap","A long caption four",height=9, uml=r"""
#caption figure 1
#title My super title
#
#""").display()
print('------')