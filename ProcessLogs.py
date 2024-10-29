import csv, os
from collections import defaultdict

class ProcessLogs:
    """
    Assuming flow log format is strictly of version 2 in the below order
    ["version", "account-id", "interface-id", "srcaddr", "dstaddr", "srcport", 
     "dstport", "protocol", "packets", "bytes", "start", "end", "action", "log-status"]
    """

    def read_lookup_table(self, file_path):
        """
        read_lookup_table function reads lookup_table.csv file and creates a dictionary for tag lookup
        tag_lookup -> {(dstport, protocol): tag}
        eg. tag_lookup = {(25,"tcp"): "sv_p1", (31,"udp"): "sv_p3"}
        """
        tag_lookup = {}
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (int(row['dstport'].strip()), row['protocol'].strip().lower())
                tag_lookup[key] = row['tag'].strip().lower()
        return tag_lookup
    
    def read_protocol_numbers(self, file_path):
        """
        read_protocol_numbers function reads protocol_numbers.csv file and creates a dictionary for protocols
        protocols -> {port: protocol}
        eg. protocols = {6: "tcp", 17: "udp"}
        """
        protocols = {}
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Keyword']: # if protocol keyword empty then skip
                    protocols[row['Decimal'].strip()] = row['Keyword'].strip().lower()
        return protocols


    def process_flow_logs(self, flow_log_path, lookup_table_path, protocol_numbers_path, tag_output_path, combination_output_path):
        """
        process_flow_logs function calls read_lookup_table and read_protocol_numbers to get the tag_lookup and protocols_map
        dictionaries respectively. 
        process_flow_logs function then reads and process the log file line by line to create 
        tag counts and combination counts using the fetched dictionaries. 
        Funciton saves tag counts and combination counts in two separate csv files as output.
        """
        tag_lookup = self.read_lookup_table(lookup_table_path)
        protocols_map = self.read_protocol_numbers(protocol_numbers_path)
        tag_counts = defaultdict(int)
        combination_counts = defaultdict(int)

        with open(flow_log_path, 'r') as f:
            for line in f:
                fields = line.strip().split()
                # check for valid logs with version 2 entry
                if len(fields) < 14 or fields[0] != '2':
                    continue

                dst_port = int(fields[6])
                protocol = protocols_map.get(fields[7], "unknown")
                key = (dst_port, protocol)
                tag = tag_lookup.get(key, 'untagged')

                # tags can map to more than one port, protocol combinations
                # keeping tag count and combination count separate 
                tag_counts[tag] += 1
                combination_counts[f"{dst_port},{protocol}"] += 1

        # Write tag counts to file
        with open(tag_output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Tag', 'Count'])
            for tag, count in tag_counts.items():
                writer.writerow([tag, count])
        print("Tag count written to file", tag_output_path)

        # Write combination counts to file
        with open(combination_output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Port', 'Protocol', 'Count'])
            for combination, count in combination_counts.items():
                combination_split = combination.split(",")
                writer.writerow([combination_split[0], combination_split[1], count])
        print("Port/Protocol Combination count written to file", combination_output_path)

# Run code
# update dir_path in case of running locally to current directory path
dir_path = '/workspaces/Process-Flow-Logs/'
flow_log_path = dir_path + 'logs.txt'
lookup_table_path = dir_path + 'lookup_table.csv'
protocol_numbers_path = dir_path + 'protocol_numbers.csv'
tag_output_path = dir_path + 'output_tag_counts.csv'
combination_output_path = dir_path + 'output_combination_counts.csv'
obj = ProcessLogs()
obj.process_flow_logs(flow_log_path, lookup_table_path, protocol_numbers_path, tag_output_path, combination_output_path)