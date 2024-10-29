## Process-Flow-Logs

### Run code
#### Run online using GitHub CodeSpaces
- Code can be executed online using github codespaces (requires github login).
- Go to Code -> Codespaces -> create new codespace
- Go to file ProcessLogs.py, run code using option run python file in terminal. (same environment as VS code)
- To update input files lookup_table.csv or logs.txt, upload those files and update file name in the last section of the code.
- Output files for tags and combination will be generated in the same directory.

#### Run locally on laptop
- To run code locally, input files required 
    - logs.txt
    - lookup_table.csv
    - protocol_numbers.csv
    - ProcessLogs.py
- Update dir_path to current directory where all above files are present

### Assumptions:
1) Flow log record format: fields taken from the AWS flow log records only version 2 in the same order
URL: https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html
Below is example of flow log fields
-----------------------------------------------------------------------
| Index | Field       | Example 1     | Example 2     | Example 3     |
|-------|-------------|---------------|---------------|---------------|
| 0     | version     | 2             | 2             | 2             |
| 1     | account-id  | 123456789012  | 123456789012  | 123456789012  |
| 2     | interface-id| eni-0a1b2c3d  | eni-4d3c2b1a  | eni-5e6f7g8h  |
| 3     | srcaddr     | 10.0.1.201    | 192.168.1.100 | 192.168.1.101 |
| 4     | dstaddr     | 198.51.100.2  | 203.0.113.101 | 198.51.100.3  |
| 5     | srcport     | 443           | 23            | 25            |
| 6     | dstport     | 49153         | 49154         | 49155         |
| 7     | protocol    | 6             | 6             | 6             |
| 8     | packets     | 25            | 15            | 10            |
| 9     | bytes       | 20000         | 12000         | 8000          |
| 10    | start       | 1620140761    | 1620140761    | 1620140761    |
| 11    | end         | 1620140821    | 1620140821    | 1620140821    |
| 12    | action      | ACCEPT        | REJECT        | ACCEPT        |
| 13    | log-status  | OK            | OK            | OK            |
-----------------------------------------------------------------------

2) Protocol numbers: to support all Assigned Internet Protocol Numbers, 
used a protocol_numbers.csv file for the mappings.
URL: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

3) Lookup table should contain all three fields on each row - dstport, protocol, tag 
  


### Test cases considered:
 - inputs are randomly capitalized to check if they map to the same tag
 - tags map to more than one port, protocol combinations 
    - 2 logs entries for 25,tcp,sv_P1 
    - 1 log entry for 23,tcp,sv_P1 
 - unknown protocol field, outputs in an additional untagged count
-  File constraints
    - local laptop can process below file requirements in-memory
    - lookup file can have up to 10000 mappings
    - flow log file size can be up to 10 MB


### Analysis

- For this solution, assumption is data is at rest.
- Logs file size won't increase in GB scale as in the code, log file is processed in-memory.
- If log file size is larger, then pratially processing file in chunks can be a possible workaround. 
- Also, map reduce can be used to process larger log files.
- In case of streaming data, using Spark for processing is efficient.