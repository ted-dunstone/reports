from px_build_doc.util import fetch_var, News, display
display('# News\n')
display(r'\twocolumn')
News().query(fetch_var("news")).display()
display(r'\onecolumn')
