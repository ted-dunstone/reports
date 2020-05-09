# Presentations (Powerpoints)

Performix produces both pdf reports and powerpoint presentation. This presentation should be a summary of the information in the full report.

## Template

The base template is given by the file `template.potx`. This file can be loaded and edited in Powerpoint.

## Content

A presentation is built using files ending with `.pres`. A simple example is below showing how to set different columns and settings. Note a level 1 heading is a section slide and a level 2 heading is a detail slide:

    # Introduction

    ## In the morning

    - Item 1
    - Item 2

    ## Slide with just an image

    ![symptoms](https:imagr.png)

    ## Basic Slide

    test

    # Point 1

    ## Sub point

    EPS

    ## This slide has columns

    ::: columns

    :::: column

    - Item 1
    - Item 2

    ::::

    :::: column
    ![symptoms](https:imagr.png)
    ::::

    :::

    ## Last slide with bullets

    - Item 1
    - Item 2

    # Conclusion

    ![map](image.png)
