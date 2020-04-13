\section*{Executive Summary}                                    
\addcontentsline{toc}{section}{Executive Summary} 
This is the exec summary ...

# Introduction

**{{title}}**

Intro2 Wow

This readme file describes how to use the **Performix Reporting CLI (Command Line Interface)**. This tool provides the resources necessary to access a performix server. This server provides the functionality of the Performix tool which can be used to generate detailed reports from biometric data.

To enable easy interaction with the performix server, a pxrest Python package, four python scripts, and some shell scripts have been provided.

\reversemarginpar
\marginpar{The analysis}

The pxrest python package and four python scripts allow advanced interaction with Performix Server to generate custom reports.
 
 The shell scripts provide easy access to the Performix server. They are especially designed for generating the example reports using the example data and configuration files provided.

Here's a simple footnote,[^1] and here's a longer one.[^bignote]

[^1]: This is the first footnote.

[^bignote]: Here's one with multiple paragraphs and code.

    Indent paragraphs to include them in the footnote.

    `{ my code }`

    Add as many paragraphs as you like.

[see @doe2005, pp. 33-35; also @joe07, chap. 1]

# Setup

In order to use the cli and run the examples you will need python 3.6 and the following python packages:

* requests
* urllib
* shutil
* json

\awesomebox{5pt}{\faPassport}{blue}{
Ensure they are installed, these packages may already be installed by default with Python 3.
}

\awesomebox{5pt}{\faFingerprint}{red}{
Ensure they are installed, these packages may already be installed by default with Python 3.
}

Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |

| There must be at least 3 dashes separating each header cell. The outer pipes are optional, and you don't need to make the  raw Markdown line up prettily. You can also use inline Markdown. x|
| ------------- |

There must be at least 3 dashes separating each header cell.
The outer pipes (|) are optional, and you don't need to make the 
raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3



\begin{tipblock}

In order to use the cli and run the examples you will need python 3.6 and the following python packages:

* requests
* urllib
* shutil
* json

```sh
pip install <package name>
```
\end{tipblock}

if a package is not installed then install them using pip:

```sh
pip install <package name>
```

Or with pipenv:

```sh
pipenv install <package name>
```
Installation of python and pip can be found [here](https://realpython.com/installing-python/).


The pxrest library and associated files are also required. These files should be provided with the px-rest-examples package, within the directory of this readme. However, they can be placed in a directory of your choosing. Below is the minimum folder structure that is required:
```sh
<cli directory>
└── pxrest
    └── __init__.py
    └── analysis.py
    └── job.py
    └── script.py
    └── source.py
    └── util.py
└── logs
└── config.ini
└── PxJobCreate.py
└── PxJobRetrieve.py
└── PxRemoveConfig.py
└── PxUpload.py
└── px-create-report.sh
└── px-create-report.bat
└── px-setup-report.sh
└── px-setup-report.bat
└── README.md
```


## Config

The congif file must be unpdated to point to the correct Performix server. The default specified is for the biometix test server.

```sh
[Defaults]
server_url = https://performix-test.biometix.com
```

## Report Requirements:

These are the minimum files required to generate a report:

 * Truth file (in csv format)
 * Score data file (in csv format)
 * An analysis parameter file (in json format)
 * A report generation script (as a jupyter notebook file)

### Report Generation Script

This file is provided by Biometix. This is the script that tells Performix how to generate the report.

The latest version of the performix script provided by Biometix is v1.13.

### Truth File

The purpose of the truth file is to contain information about which probe and gallery pairs are matches.

The file is a csv file which must contain the columns: ‘probeid’, ‘galleryid’, and ‘truth’. In version 1.13 the probeid, galleryid, and truth columns can be set to a custom name, this is done in the analysis parameter file.

For a given probeid and galleryid pair the truth column records True if this pair is a match.
In the truth file it is only necessary to store records that are matches. Any probe gallery pair that is not found in the truth file is assumed to be a non-match, the truth value is automatically set to False.

### Score Data File

This file contains the results of a matching algorithm.

The file is a csv and must be formatted as per the BAT Ping Specifications.

For the current version of the performix script the minimum required columns are: 'probeid', 'galleryid', 'ppos', 'gpos', and 'score'. These columns specify the probe and gallery ids, the probe and gallery finger position, and the score for the match. The ‘probeid’ and ‘galleryid’ column names can be set to a custom name, this is done in the analysis  parameter file.

The current version of the performix script ignores impression information in the finger position column.

The performix script can detect cases of a record:

 * with a missing score.
 * with different finger positions for the probe and gallery.
 * with identical probe mrr and gallery mrr id.

 Additionally the performix script can detect a bimetric miss (a probe gallery id pair labelled as match in the ground truth file that is not found in the score data file) and detect alternative registrations (a gallery record that, for a given probe, is not labeled as a match in the ground truth file at the record id level, but actually is a match, which is identified at the level of a person id). The script will detect these cases and print them out in the report.

### Analysis Parameter File

 The analysis parameter file, or configuration file, contains parameters for the analysis in a json format. These parameters are used by the performix script to perform the analysis and configure the report.

 For further details, please see the Setting Up the Parameter File section.

## Provided Example Files

The px-rest-examples package includes example files that can be used to generate example reports. These files have been provided in the data folder. They were generated using a random number generator purely for the purpose of testing, to show what a report generated with performix will look like.

The data folder contains the following:

 * analysis folder – Contains one json parameter file set up for each data type.
 * Source folder – Contains ground truth files for each data type. These were generated with the result files.
 * Job folder – Contains result files for each data type which have randomly generated scores, with probe and gallery ids that match the ground truth file.
 * Script – Contains the performix script provided by Biometix.

The Performix script file provided is the latest version of the script, v1.13. All the commands listed in this readme assume the use of this script.

For the Ground Truth files, Score Data files, and Analysis Parameter files, there are multiple files for each of the test types. The provided files allow the generation of five example analysis, one for each test type.

These are:

* TP to TP search
* TP to TP verify
* UL to TP search
* TP to UL search
* UL to UL search

When running the performix script in BAT Ping mode, the script will search for previous jobs that use the same analysis to compare results with. To test this simply rerun the job with a different score data set without recreating the analysis instance. Re-runing the job with the same data set will allow the script to compare results with the first run but the comparison will show no change in the results.

## Validation Tests

The following command can be used to test the deployed system using the following smoketest data:

* data/job/SMOKE_LE1-Results.csv
* data/analysis/smoke_analysis.json
* data/source/SMOKE_LE1_Truth_File_amend.csv

After running the following commands a pdf report ```SmokeTest_report.pdf``` should be generated.

```console
sh px-setup-report.sh SmokeTest data/source/SMOKE_LE1_Truth_File_amend.csv data/script/Performix_Script_v1.13.ipynb data/analysis/smoke_analysis.json
```

```console
sh px-create-report.sh SmokeTest data/job/SMOKE_LE1-Results.csv data/analysis/smoke_analysis.json SmokeTest_report.pdf 50
```

### Error conditions

If there is an error reported e.g.

```sh
Action "create job" complete
Unable to download the report
Action "job retrieve" failed
job_id: F86F7714-FA07-48CB-A1A3-074E0EDB66F1
````

The error condition can be found by going to the server:

```sh
[server_url]/job/[job_id]
```

e.g.

```sh
https://performix-test.biometix.com/job/F86F7714-FA07-48CB-A1A3-074E0EDB66F1
```

a full list of all jobs run can be seen at:

```sh
https://performix-test.biometix.com/job
```



## Shell Commands

The shell scripts provided streamline the process of using the CLI. The usage of these scripts are defined below. For advanced usage please refer to the Python section of this readme. These commands show how to verify the cli and performix script using the example data.

To run one example, using the example data and config files, use the make_report.sh script.

Run this command in the current directory (the directory containing this readme file with all supporting files).

```sh
sh make_report.sh [script file] [truth file] [config json file] [results file] [analysis name] [log file]
```

Example (using UL to TP search data):

```sh
sh make_report.sh script/Performix_Script_v1.13.ipynb source/UL-TP_truth.csv analysis/UL-TP_analysis.json job/UL-TP_res.csv UL-TPtest logs/debug.log
```

Alternatively the files 'set_up_examples.sh' and 'job_run_examples.sh' will run all examples and generate five reports.

```sh
sh set_up_examples.sh
sh job_run_examples.sh
```

The command job_run_examples.sh and make_report.sh may take some time to finish as the analysis is performed and the report created on the server. Depending on the speed of the server, the shell script may attempt to retrieve the report before the analysis has finished running. If this command fails, check for this case by checking the logs to see what caused the error. If the analysis was still running, try increasing the --attempts parameter to increase how long the shell script will wait for the analysis to finish. This can be done by edditing the shell script.

\begin{tipblock}
Shell script logs are output to `/logs/debug.log`)
\end{tipblock}

## Parameter File Details

The parameter file contains parameters for the analysis in a json format. These parameters are used by the Performix Script.

Example:
```json
{
"threshold" : 2000,
"fpr_arry" : [0.1,0.01,0.05,0.001],
"max_fpr_diff" : 2.5,
"max_fnr_diff" : 2.5,
"max_auc_diff" : 0.2,
"data_type" : "UL to TP Search",
"test_type" : "BAT Ping",
"truth_probe_col" : "ProbeID",
"truth_gallery_col" : "GalleryID",
"truth_match_col" : "Truth",
"results_probe_col" : "ProbeMRR",
"results_gallery_col" : "GalleryMRR",
"show_types" : "ALL, 1, 2, 3",
"gallery_size" : 10000,
"identical_mrr_check" : "True",
"truth_alt_col" : "GalleryEPI",
"results_alt_col" : "GalleryEPI"
}
```

* “Threshold” - The score threshold for the analysis used to calculate matches and determine the accuracy.

* “fpr_arry” - An array of the False Positive Rates required the table that shows false non-match rates that are evaluated from these specific false match rates

* “max_fpr_diff” - The maximum difference in the false positive rate allowed when compared to previous results. Performix will make a note in the conclusion of the report if this metric or any of the two below exceed the maximum difference specified in this parameter file.

* “max_fnr_diff” - The maximum difference in the false negative rate allowed when compared to previous results.

* “max_auc_diff” - The maximum difference in the AUC of the ROC graph allowed when compared to previous results.

* “data_type” - The type of data being analysed. This variable is used to create the title of the report in the format ‘data_type for test_name’

* “test_type” - The type of test being run. This variable is used to create the title of the report in the format ‘data_type for test_type’. Setting “test_type” to “BAT Ping” will enable BAT Ping mode allowing the script to compare results with previous jobs. If “test_type” is set to “SA BAT” then an SA BAT operation will be performed where comparison with previous jobs will not be performed. Result data is only stored if the script is running in “BAT Ping” mode.

* "test_type" - Same as "test_name". used in version 1.12 while "test_name" is deprecated in version 1.12.

* “test_description” - Deprecated in version 1.10

* “truth_probe_col” - Set the name of the column in the truth file to be used as the Probe Id in the analysis (e.g. ProbeMRR).

* “truth_gallery_col” - Set the name of the column in the truth file to be used as the Gallery Id in the analysis (eg GalleryMRR).

* "truth_match_col" - Set the name of the column in the truth file with the match information. This column contains True if the probe gallery pair is a match.

* “results_probe_col” - Set the name of the column in the results file to be used as the Probe Id in the analysis (e.g. ProbeMRR).

* “results_gallery_col” - Set the name of the column in the results file to be used as the Gallery Id in the analysis (eg GalleryMRR).

* "show_types" - Set which finger type/position to perform the analysis on. This is done as a comma seperated list. Setting this parameter to "*" will set the script to perform an analysis on all finger types.

* "Gallery Size" - Set the size of the gallery that was used to generate the results. This parameter is used by the script in evaluating the accuracy of the results. If it is not supplied then no accuracy projection is used.

* “identical_mrr_check” - A flag to enable the script to check for records in the results file that have the same ProbeMRR and GalleryMRR. The script will perform this analysis only if this variable is set to “True”. Only enable this check if the results file being provided contains the columns “ProbeMRR” and “GalleryMRR” and these columns are populated.

* "truth_alt_col" - An alternative gallery id which, when set, will enable identification of alternative registrations (gallery registrations that are a match for the probe but not labeled in the truth file). This gallery id should be a person level rather than record level id. This parameter must be set with its companion "results_alt_col".

* "results_alt_col" - An alternative gallery id which, when set, will enable identification of alternative registrations (gallery registrations that are a match for the probe but not labeled in the truth file). This gallery id should be a person level rather than record level id. This parameter must be set with its companion "truth_alt_col".

## Config File Setup

The most important file to set up is the json parameter file. To set up an analysis instance, the parameter file must be set up correctly to reflect what kind of analysis and data is to be used in this analysis. Not all the parameters described in the previous section are required, some are optional for additional functionality. This section describes the minimum set up required to create an analysis.

Set the "test_type" variable to either “SA BAT” or “BAT Ping” to run either of these tests.
Set the “data_type” variable to the type of data that will be used in the analysis. e.g. “TP to TP search”.

Make sure the “threshold” variable is set to the desired threshold for the analysis. This threshold should be within the range of scores of the data set. Ideally set close to an optimal threshold.

For BAT Ping ensure the following variables are set: "max_fpr_diff", "max_fnr_diff", "max_auc_diff" to the desired amount. Any variation between past jobs greater than these values will be flagged in the conclusion.

Ensure the variables: "truth_probe_col", "truth_gallery_col", "results_probe_col", "results_gallery_col" are set to the name of the columns in the truth and result files that will be used to compare records between the truth file and the result file. What these values will be set to may differ between data types, but generally the “ProbeMRR” and “GalleryMRR” are used.

If the ground truth file being used does not have a "truth" column, then use the "truth_match_col" parameter to set the name of the column that contains truth information.

If all these parameters are correctly set then use the CLI to set up an analysis using the parameter file.

## Jupyter

The Performix server being used may have Jupyter Notebook or Lab installed.

Jupyter Notebook or Lab can be accessed using a browser and provide the ability to view analysis and jobs uploaded to the server and to run scripts interactivly.

To access the server go to the following address replacing SERVER_ADDRESS with the same address used in the config file.

```
http://SERVER_ADDRESS:8080/
```

Jupyter will ask for a token to access the server. This token can be found in the settings for the Performix server.


## Further Shell Script Usage

This section provides information on the additional shell scripts provided in the px-rest-examples package. These shell scripts provide an alternative method of accessing the performix server. This may be usefull for advanced usage without going to the python scripts. For generating the example reports, please see the above section.

There are 2 steps in this process:
* Setup the analysis
* Create the report

### Setup an analysis

A script to setup an analysis, the inputs are:

  * analysis_name: The name of the analysis
  * truth_file: The csv ground truth file
  * script_file: The analysis script file
  * config_file: A json config file

```
MacOS / Linux

> sh px-setup-report.sh [analysis_name] [truth_file] [script_file] [config_file]

Windows

> px-setup-report.bat [analysis_name] [truth_file] [script_file] [config_file]

```

#### Example

```
MacOS / Linux

> sh px-setup-report.sh analysis_test data/source/UL-TP_truth.csv data/script/Performix_Script_v1.13.ipynb data/analysis/UL-TP_analysis.json

Windows

> px-setup-report.bat analysis_test data/source/UL-TP_truth.csv data/script/Performix_Script_v1.13.ipynb data/analysis/UL-TP_analysis.json

```

### Create a report

A script to create a report for a given analysis, the inputs are:

  * analysis_name: The name of the analysis
  * score_file: The csv file with scores
  * param_file: A json parameters file (optional)
  * output_file: The name of the output pdf

This step includes downloading the report.

The script generates a job_id and prints it out for reference.

```
MacOS / Linux

> sh px-create-report.sh [analysis_name] [score_file] [param_file] [output_filename] [retrieve_attempts]

Windows

> px-create-report.bat [analysis_name] [score_file] [param_file] [output_filename] [retrieve_attempts]
```


#### Example
```
MacOS / Linux

> sh px-create-report.sh analysis_test data/job/UL-TP_res.csv data/job/job.json test_report 20

Windows

> px-create-report.bat analysis_test data/job/UL-TP_res.csv data/job/job.json test_report 20
```

### Download report

A script to download a report that has already been created.
This step is really only necessary if a report needs to be accessed for a job that has already been completed.

The input parameters:

  * job_id: A job id provided by the service that started the job (note this must be unique)
  * output_file: The name of the output pdf

note: the job_id can be found in the log file when the report was created or in the previous step.

```
MacOS / Linux

> sh px-download-report.sh [job_id] [output_filename]

Windows

> px-download-report.bat [job_id] [output_filename]
```

#### Example
```
MacOS / Linux

> sh px-download-report.sh job_1456 test_report

Windows

> px-download-report.bat job_1456 test_report
```

## Python Advanced Usage

These instructions show how to perform advanced analysis to generate custom scripts.

To set up and run a custom analysis only 4 commands are required. These commands use the python scripts: PxUpload.py, PxRemoteConfig.py, PxJobCreate.py and PxJobRetrieve.py.

The example commands use the provided example files.

These files can be set up for BAT Ping. When running for BAT Ping, the script will search for previous jobs that use the same analysis to compare results with. To test this simply rerun steps 3 and 4 with a different score data set.

### 1. PxUpload.py

This script is used to upload the script itself and the source file to the Performix server.

Command Format:

```
python3 PxUpload.py [script or source] [file to upload] [name on server] --log [log file]
```

Example:

Upload Script:
```
python3 PxUpload.py script data/script/Performix_Script_v1.10.ipynb script_1 --log logs/script_upload.log
```
Upload ground truth files:
```
python3 PxUpload.py source data/source/TP-TPsearch_truth.csv TP-TPs_truth --log logs/source_upload.log
python3 PxUpload.py source data/source/TP-TPverify_truth.csv TP-TPv_truth --log logs/source_upload.log
python3 PxUpload.py source data/source/UL-TP_truth.csv UL-TP_truth --log logs/source_upload.log
python3 PxUpload.py source data/source/TP-UL_truth.csv TP-UL_truth --log logs/source_upload.log
python3 PxUpload.py source data/source/UL-UL_truth.csv UL-UL_truth --log logs/source_upload.log
```
When uploading these files ensure each file is given a unique name.

The above examples creates a script called script_1 and multiple source files. If
these lines were to be reran with a different file then their files on the server
would be updated to the new file. Note also that a log file can be used.

### 2. PxRemoteConfig.py

Once at least a script has been uploaded, as seen in the previous section, an Analysis
instance can be created on the server. Creating an analysis requires a json parameter file.
```
python3 PxRemoteConfig.py [analysis name] [script name] --config [parameter file] --sources [truth file name] --log [log file]
```
Note the [script name] must be the same name used in step 1 when uploading the script.

Note the [truth file name] must be the same name used in step 1 when uploading the ground truth file.

Example:
```
python3 PxRemoteConfig.py TP-TPs_analysis script_1 --config data/analysis/TP-TPsearch_analysis.json --sources TP-TPs_truth --log logs/analysis.log
python3 PxRemoteConfig.py TP-TPv_analysis script_1 --config data/analysis/TP-TPverify_analysis.json --sources TP-TPv_truth --log logs/analysis.log
python3 PxRemoteConfig.py  UL-TP_analysis script_1 --config data/analysis/UL-TP_analysis.json --sources UL-TP_truth --log logs/analysis.log
python3 PxRemoteConfig.py  TP-UL_analysis script_1 --config data/analysis/TP-UL_analysis.json --sources TP-UL_truth --log logs/analysis.log
python3 PxRemoteConfig.py  UL-UL_analysis script_1 --config data/analysis/UL-UL_analysis.json --sources UL-UL_truth --log logs/analysis.log
```
### 3. PxJobCreate.py

Once we have successfully created an Analysis instance we can create a job to process
some data.
```
python3 PxJobCreate.py [job name] [analysis name] [score data file] --log [log file]
```
[job name] must be unique compared to all previously created jobs.

Ensure [analysis name] is the same name of the analysis to be used that was created in step 2.

Example:
```
python3 PxJobCreate.py TP-TPs_job_1 TP-TPs_analysis data/job/TP-TPsearch_res.csv --log logs/job_create.log
python3 PxJobCreate.py TP-TPv_job_1 TP-TPv_analysis data/job/TP-TPverify_res.csv --log logs/job_create.log
python3 PxJobCreate.py UL-TP_job_1 UL-TP_analysis data/job/UL-TP_res.csv --log logs/job_create.log
python3 PxJobCreate.py TP-UL_job_1 TP-UL_analysis data/job/TP-UL_res.csv --log logs/job_create.log
python3 PxJobCreate.py UL-UL_job_1 UL-UL_analysis data/job/UL-UL_res.csv --log logs/job_create.log
```
### 4. PxJobRetrieve.py

The final step is to get the report PDF from the job.
```
python3 PxJobRetrieve.py [job name] --filename [report name] --log [log file] --attempts [number of attempts]
```
[job name] must be the same name used in step 3.

This step will fail if the job is still running. Check the logs to see if the job is still running. Otherwise just try again later.

Example:
```
python3 PxJobRetrieve.py TP-TPs_job_1 --filename TP-TPs_report --log logs/job_retrieve.log --attempts 20
python3 PxJobRetrieve.py TP-TPv_job_1 --filename TP-TPv_report --log logs/job_retrieve.log --attempts 20
python3 PxJobRetrieve.py UL-TP_job_1 --filename UL-TP_report --log logs/job_retrieve.log --attempts 20
python3 PxJobRetrieve.py TP-UL_job_1 --filename TP-UL_report --log logs/job_retrieve.log --attempts 20
python3 PxJobRetrieve.py UL-UL_job_1 --filename UL-UL_report --log logs/job_retrieve.log --attempts 20
```

