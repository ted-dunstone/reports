# Basic Setup

## Report Parameters

The main report parameters are found in the `params.yaml` file. An example for this document can be seen below.

    # Main Parameters
    title: Performix Technical Users Manual
    subtitle: Design and Usage Information
    author: Biometix
    date: 5th March 2020
    classification: Commercial in Confidential
    keywords: '[analytics]'

    # Contact Params
    contact: Ted Dunstone
    contact_phone: +61 (2) 419990968
    contact_email: ted@biometix.com
    
    # Report Specific Params

    end_customer: Biometix

\cautionbox{There is a sensitivity to line length of those fields that are used in the Latex template. This include title and subtitle. See the FAQ for more details}

There are three main types of information:

* Main Parameters: These will populate the front cover and control many of the display options.
* Contact Params: Sets details about the person/organisation resposible for the report
* Report Specific Params: Parameter that will be consumed by the scripts or referenced in the documents.

### Using parameters

In a markdown file you can reference there using double curly braces.

In a script file you can use the following to get a parameter:

    ```
    from px_build_doc.util import fetch_var, display

    end_customer = fetch_var("end_customer")

    display(end_customer)
    ```

### Latex template Other parameters

The parameters are passed in the pandoc templating systems, which then passes them to latex. Latex uses a template which relies on a wide-variety of these parameters. Many of these might be set by default.

The default template can be found in `px_build_doc\data\my-panadoc.latex`
