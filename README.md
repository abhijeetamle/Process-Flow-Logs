## Process-Flow-Logs

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


### Run code

- To run code, go to ProcessLogs.py file, run code using option run python file in terminal.
- To update input files lookup_table.csv or logs.txt, upload those files and update file name in the last section of the code.
- Output files for tags and combination will be generated in the same directory.