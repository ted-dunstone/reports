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

