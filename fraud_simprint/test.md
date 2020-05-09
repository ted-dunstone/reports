# Introduction


This report has been automatically produced using Performix. It provides two benefits:

1. once we have generated the flat comparison scores there are a lot of scripts and manual effort that go into setting the right thresholds for match/non-match, 
2. determining different ways to cluster the outputs, and extracting more specific trends or anomalous patterns that we should be sharing to our partners. 

Beneficiary
:   Someone enrolled into the Simprints database. Suppose Simprints is part of a maternal healthcare system, the beneficiaries would be the mothers who are receiving healthcare. We take their fingerprints, and assign them GUIDs (unique IDs). 
\vskip 0.1 cm

User
:   Someone who uses Simprints' technology to enrol beneficiaries into the system and deliver services. So in the maternal healthcare example, a User would be a Health Worker who visits mothers and delivers services. Each user is assigned a unique pseudoUserId.
\vskip 0.1 cm

Module
:   A geographical area. We make the (okay-ish) assumption that beneficiaries are unlikely to move between modules. So, during identification or deduplication, we only compare fingerprints from within the same module (so that the total number of comparisons we make is not too large). Each module is assigned a unique pseudoModuleId.
\vskip 0.1 cm

See table \ref{features_table}.

| Function name | Description                    |
| ------------- | ------------------------------ |
| `help()`      | Display the help window.       |
| `destroy()`   | **Destroy your computer!**     |

Table: Performix Features \label{features_table}


blah
## Errors

to_presentation
window



Hello!


### Suberrors

Suberrors

## NewSection

Last section

# Data

* **enrolments_for_biometix.csv** contains a list of all our beneficiaries. Their unique ID is guid, the user who enrolled them is pseudoUserId, the module (geographical area) in which they were enrolled is pseudoModuleId, and enrolmentTime (if not NULL) is the time at which they were enrolled.
* **user_guids_for_biometix.csv** contains a list of those GUIDs which correspond to users whose biometric data we happened to collect (note that this was not done for all users, and note that some users have been given multiple GUIDs because we accidentally registered them multiple times). For some subset of the users, we have also registered them as beneficiaries (as in we have given them guids that correspond to their own fingerprints). Note that we only have this data for some users and some users have been registered multiple times (i.e. been given multiple guids that correspond to their own fingerprints). For an initial analysis, where you're just trying to find duplicates, and nothing to do with trends that correspond to different users, you can just ignore this table. Note that for comparisons (more below), we have artificially treated each of these user-specific GUIDs as if they were enrolled in all modules.
* **quality_scores.csv** (compressed using GZIP) contains the quality scores for each of the fingerprint images we collected during registration. You can ignore sessionId, but for each guid, finger is LEFT_THUMB, LEFT_INDEX_FINGER, RIGHT_THUMB, or RIGHT_INDEX_FINGER, and quality is the quality score returned by our extractor.
* **comparisons** contains a bunch of CSVs (each compressed using GZIP) that contains pairwise comparisons of our beneficiaries' registered fingerprints. This was done module by module, so it only contains all pairs of GUIDs guid1 x guid2 where guid1 and guid2 are from within the same module (during registration, from table 1.) or if guid1 or guid2 are users (from table 2.). Note that all GUIDs have been stored as bytes, not as strings. I've given you sample code below to convert between bytes and GUID strings (in Python, but any language you use will have a Base 64 encoder/decoder, I'm sure). Our matcher is not finger agnostic, so left thumbs are only compared with left thumbs, left indices with left indices, and so on - the column finger specifies which finger is being compared (LEFT_THUMB, LEFT_INDEX_FINGER, RIGHT_THUMB, or RIGHT_INDEX_FINGER) and matchScore is the score returned by our matcher, where the higher the number, the more likely it is that those fingerprints belonged to the same person.


## Meta Data

A data section







![](020_virus_figs_01.png)

Figure 1: from dict



this comes after






![](020_virus_figs_02.png)

Figure 2: my new cap 1



this comes after






![](020_virus_figs_03.png)

Figure 3: override caption










![](020_virus_figs_04.png)

Figure 4: override caption










![](020_virus_figs_05.png)

Figure 5: Counts of enrollments versus dates with scores above 500










![](020_virus_figs_06.png)

Figure 6: Counts of enrollments versus dates with scores above 500





## Match and Score Distributiuons

The following section provides an overiew of the match and quality distributions.







![](020_virus_figs_07.png)

Figure 7: Counts of enrollments versus dates with scores above 500





# Matches

subsection [test_params]






![](020_virus_figs_08.png)

Figure 8: Counts of enrollments versus dates with scores above 500





# Quality

subsection [test_params1]






![](020_virus_figs_09.png)

Figure 9: Counts of enrollments versus dates with scores above 500





# Analysis

A deeper look 
\warningbox{Should be a waring}







![](020_virus_figs_10.png)

Figure 10: From Caption




|   moduleId_10 |   moduleId_110 |   moduleId_12 |   moduleId_13 |   moduleId_14 |   moduleId_16 |   moduleId_2 |   moduleId_32 |   moduleId_4 |   moduleId_45 |   moduleId_47 |   moduleId_49 |   moduleId_57 |   moduleId_75 |   moduleId_79 |   moduleId_90 |   moduleId_93 |
|---------------|----------------|---------------|---------------|---------------|---------------|--------------|---------------|--------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
|           nan |            nan |           nan |           nan |             1 |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |           nan |           nan |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |           nan |             3 |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |             2 |          nan |           nan |           nan |           nan |           nan |           nan |           nan |           nan |           nan |
|             9 |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |             1 |           nan |           nan |           nan |           nan |           nan |           nan |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |             2 |             1 |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |            2 |           nan |          nan |           nan |           nan |           nan |           nan |           nan |           nan |           nan |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |             3 |             1 |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |             1 |           nan |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |           nan |             8 |           nan |
|           nan |            nan |           nan |             1 |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |           nan |           nan |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |             2 |           nan |           nan |           nan |           nan |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |            1 |           nan |           nan |           nan |           nan |           nan |           nan |           nan |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |             3 |           nan |           nan |           nan |           nan |
|           nan |             14 |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |            10 |            31 |             7 |
|           nan |            nan |           nan |           nan |           nan |             1 |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |           nan |           nan |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |             7 |             4 |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |           nan |           nan |            10 |
|           nan |            nan |             1 |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |             1 |           nan |           nan |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |             1 |           nan |           nan |           nan |           nan |           nan |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |             8 |             2 |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |            35 |            67 |           nan |
|           nan |            nan |           nan |           nan |           nan |           nan |          nan |           nan |          nan |           nan |           nan |           nan |           nan |           nan |             3 |             1 |           nan |

Table: A categorical table



# Conclusion

In conclusion this is the end of the report.

[**Duns2008**] Dunstone, T. and Yager, N., 2008. Biometric system and data analysis: Design, evaluation, and data mining. Springer Science & Business Media.

\appendix
\section*{Appendices}
\addcontentsline{toc}{section}{Appendices}


# Appendix

Imported from file


# Document Extras

There are a variety of extra parameters that can be added to a script. For instance.

## Margin Paragraphs

Margin paragraphs can be used to highlight specfic text paragraphics.

    \reversemarginpar
    \marginpar{This is a margin paragraph}

\reversemarginpar
\marginpar{This is a margin paragraph}

## Tips

See <https://ctan.kako-dev.de/graphics/awesomebox/awesomebox.pdf> for more detailed info.

    \begin{tipblock}
    Tip information.
    \end{tipblock}

\begin{tipblock}
Tip information.
\end{tipblock}

    \notebox{Lorem ipsum…}

\notebox{Lorem ipsum…}

    \warningbox{Lorem ipsum…}

\warningbox{Lorem ipsum…}

    \cautionbox{Lorem ipsum…}

\cautionbox{Lorem ipsum…}

    \importantbox{Lorem ipsum…}

\importantbox{Lorem ipsum…}

## Other callout

    \awesomebox{5pt}{\faPassport}{blue}{
    Alternate ways to call out info. Note supports fontAwesome icons including: faFingerprint.
    }

\awesomebox{5pt}{\faPassport}{blue}{
Alternate ways to call out info. Note supports fontAwesome icons including: faFingerprint.
}



