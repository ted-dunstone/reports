from px_build_doc.util import display, FigureManager, Checklist

display("""
# Performix Structure

The following discribes the performix structure.

""")


figs = FigureManager()

figs.set_uml("uml","The Performix Pipeline",height=5,uml=r"""
@startuml

start

repeat
  :read data;
  :generate diagrams;
repeat while (more data?) is (yes)
->no;
stop

@enduml
""").display()

display("""

This diagram was generated using plantuml

  @startuml

  start

  repeat
    :read data;
    :generate diagrams;
  repeat while (more data?) is (yes)
  ->no;
  stop

  @enduml
""")

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