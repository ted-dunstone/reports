from px_build_doc.util import display, TableManager

cols = ["Risk ID ","Programme delivery risks  - description","Previous Risk Rating","Risk Trend","Updates"]
TableManager().read("./RiskSheetExample.xls",4,usecols=cols).display("A new caption")
