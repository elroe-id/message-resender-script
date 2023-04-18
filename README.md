# message-resender-script

[For CentOS Only] Before running the script, make sure to run:

$ ./preinstall.sh

This installs the needed packages to run the program.

The script takes Registration Ids (RIDs) as input. Provide RID directly as argument or via a file. Example:

$ ./reprocess.py --rid 10002100740000520210122091401

OR

$ ./reprocess.py --file rids.txt

where rids.txt looks like:

10002100740000520210122091401

10001100130000120210114122006

...
...

