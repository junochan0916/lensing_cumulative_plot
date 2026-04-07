## This code is for automatically updating the README.md.
## So, even if you manually update the README.md, your changes will
## be overwritten and gone when this code is subsequently executed.

import os
import datetime

file_readme = 'README.md'

CI_PROJECT_URL         = os.getenv('CI_PROJECT_URL',         'N/A')
CI_COMMIT_SHORT_SHA    = os.getenv('CI_COMMIT_SHORT_SHA',    'N/A')
CI_COMMIT_TIMESTAMP    = os.getenv('CI_COMMIT_TIMESTAMP',    'N/A')
CI_PIPELINE_ID         = os.getenv('CI_PIPELINE_ID',         'N/A')
CI_PIPELINE_URL        = os.getenv('CI_PIPELINE_URL',        'N/A')
CI_PIPELINE_CREATED_AT = os.getenv('CI_PIPELINE_CREATED_AT', 'N/A')
CI_JOB_ID              = os.getenv('CI_JOB_ID',              'N/A')
CI_JOB_URL             = os.getenv('CI_JOB_URL',             'N/A')
CI_JOB_STARTED_AT      = os.getenv('CI_JOB_STARTED_AT',      'N/A')
CI_COMMIT_BRANCH       = os.getenv('CI_COMMIT_BRANCH',       'N/A')

if 'N/A' in '{} {} {} {} {} {} {} {} {} {}'.format(CI_PROJECT_URL, CI_COMMIT_SHORT_SHA, CI_COMMIT_TIMESTAMP, CI_PIPELINE_ID, CI_PIPELINE_URL, CI_PIPELINE_CREATED_AT, CI_JOB_ID, CI_JOB_URL, CI_JOB_STARTED_AT, CI_COMMIT_BRANCH):
    file_readme = 'README_notForCommit.md'

## Use this file only to check the name of the event that occurred most recently
#file_evelist = 'dataO4a.txt'
file_evelist = 'dataO4c.txt'
SEVENT = "S999999" #dummy event name
with open(file_evelist, "r") as ff:
    first_line = ff.readline() # Read the first line.
    words = first_line.split() # Split a line into words
    if words:
        first_word = words[0] # Get the first word
        SEVENT = first_word
    else:
        print("The word does not exist in the first line.")

## Read out the timestamp of PNG picture
file_pict = "cumulative_events.png"
print(file_pict)
if os.path.exists(file_pict): # if PNG file exists
    timestamp = os.path.getmtime(file_pict)
    last_modified = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
    pict_generated_datetime = last_modified.strftime('%Y-%m-%d %H:%M:%S')
    print(f'PNG plot file exists. Last Update is on: {pict_generated_datetime}')
else:
    print('PNG plot file doesn\'t exists')


## Template of README.md
output = \
"# LVK Cumulative Detection Plot, O1 - O4c (to date)\n" +\
"<img src=\"" + CI_PROJECT_URL + "/-/jobs/artifacts/" + CI_COMMIT_BRANCH + "/raw/cumulative_events.png?job=build\" align=\"center\" width=\"70%\"/>\n" +\
"\n" +\
"***\n"+\
"\n" +\
"## Introduction\n"+\
"These scripts generate plots of detections/candidates identified by the LVK during the observing runs, excluding any events that have subsequently been retracted. The plots are automatically updated three times daily (07:00, 15:00, and 23:00 UTC), in synch with the shift transitions of the RRT Lv-0 shifters. These Python scripts are based on the MATLAB code from https://dcc.ligo.org/LIGO-G2302098-v4, with the additional functionality of automatically updating the event list by fetching data from GraceDB.\n" +\
"\n" +\
"From O1 through O4a, the counts refer to the detected gravitational-wave events that are included in the GWTC catalog papers. In contrast, the counts for O4b and O4c refer to candidate events for which a significant low-latency alert was issued and that were not subsequently retracted. Once the corresponding GWTC paper is released, these counts are revised to reflect the officially published detections.\n" +\
"\n" +\
"For O4a, the event count is fixed at 128, following GWTC-4.0 (https://arxiv.org/abs/2508.18082). This total includes one event detected in a five day segment of data from the engineering run preceding O4a, which was analyzed and reported in GWTC-4.0. Consequently, in the figure, these five-days from pre-O4a engineering run are included within O4a, thereby making the O4a period appear five days longer than actual.\n" +\
"\n" +\
"The O4c data collection period is divided into two segments: \"January 28 – April 1, 2025\" and \"June 11 – November 18, 2025\". These segments are distinguished in the figure by different fill colors: the first is represented in dark blue, and the second in light blue. The intervening gap is omitted from the figure.\n" +\
"\n" +\
"QR code links to https://dcc.ligo.org/LIGO-G2302098/public\n" +\
"\n" +\
"## You can download the latest plot from\n" +\
"  - Latest plots (generated on `" + pict_generated_datetime +" UTC`): [**PNG**](" + CI_PROJECT_URL + "/-/jobs/artifacts/" + CI_COMMIT_BRANCH + "/raw/cumulative_events.png?job=build), [**PDF**](" + CI_PROJECT_URL + "/-/jobs/artifacts/" + CI_COMMIT_BRANCH + "/raw/cumulative_events.pdf?job=build)\n" +\
"  - Latest O4c event list fetched from graceDB and used for plotting: [**TXT**](" + CI_PROJECT_URL + "/-/jobs/artifacts/" + CI_COMMIT_BRANCH + "/raw/dataO4c.txt?job=build)\n\n" +\
"## Last update log\n" +\
"  - Project url: " + CI_PROJECT_URL + "\n" +\
"  - Commit: " + CI_COMMIT_SHORT_SHA + ", " + CI_COMMIT_TIMESTAMP + "\n" +\
"  - Pipeline: [#" + CI_PIPELINE_ID + "]("+ CI_PIPELINE_URL +"), " + CI_PIPELINE_CREATED_AT + "\n" +\
"  - Job: [#" + CI_JOB_ID + "]("+ CI_JOB_URL +"), " + CI_JOB_STARTED_AT + "\n" +\
"  - Last event included in this plot: [" + SEVENT + "](https://gracedb.ligo.org/superevents/" + SEVENT + "/view/)"

#"  - Preview of latest plot:\n" +\
#"<img src=\"" + CI_PROJECT_URL + "/-/jobs/artifacts/" + CI_COMMIT_BRANCH + "/raw/cumulative_events.png?job=build\" align=\"center\" width=\"65%\"/>"

## export to a file
with open(file_readme, mode='w') as f:
    f.write(output)
