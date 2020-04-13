"""@ UML Test"""
from px_build_doc.util import display, FigureManager, Checklist

display('# Figure Demo')

display('## WBS demo')
display('A demo of a long WBS diagram')

figs = FigureManager()

figs.set_uml("wbs","A long caption two",height=5,uml=r"""
<style>
 wbsDiagram {
  Linecolor black
  BackGroundColor white
   LineColor green
  }
}
</style>

* World 2
** Cluster 0:
*** clearview
*** enforcement
*** 550m
** Cluster 1:
*** face
*** recognition
*** facial
*** masks
** Cluster 2:
*** surveillance
*** coronavirus
*** state
*** china
*** enabling
** Cluster 3:
*** london
*** police
*** fellow
*** live
*** tech
** Cluster 4:
*** facebook
*** million
*** privacy
** Cluster 5:
*** time
*** tech
*** india
*** protests
""").display()

display('## UML demo')
display('A demo of a short UML diagram')


figs.set_uml("uml","A long caption three",r"""
start
:Hello world;
:This is defined on
several **lines**;
stop
""").display()

display('## Mindmap demo')
display('A demo of a short Mindmap diagram')


figs.set_uml("mindmap","A long caption four",height=9, uml=r"""
caption figure 1
title My super title

* <&flag>Debian
** <&globe>Ubuntu
*** Linux Mint
*** Kubuntu
*** Lubuntu
*** KDE Neon
** <&graph>LMDE
** <&pulse>SolydXK
** <&people>SteamOS
** <&star>Raspbian with a very long name
*** <s>Raspmbc</s> => OSMC
*** <s>Raspyfi</s> => Volumio

header
My super header
endheader

center footer My super footer

legend right
  Short
  legend
endlegend
""").display()

Checklist().display(["First Item","Second Item","Third Item","Last Item"],[None,True,False,None])