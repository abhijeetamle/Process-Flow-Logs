import csv, os
from collections import defaultdict

class ProcessLogs:

    def read_lookup_table(self, file_path):
        lookup = {}
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (int(row['dstport']), row['protocol'].strip().lower())
                lookup[key] = row['tag'].strip().lower()
        return lookup
    
    def read_protocol_numbers(self, file_path):
        protocols = {}
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Keyword']: # if protocol keyword empty then skip
                    protocols[row['Decimal'].strip()] = row['Keyword'].strip().lower()
        return protocols


    def process_flow_logs(self, flow_log_path, lookup_table_path, protocol_numbers_path, tag_output_path, combination_output_path):
        lookup = self.read_lookup_table(lookup_table_path)
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
                protocol = protocols_map.get(fields[7], "Unknown")
                key = (dst_port, protocol)

                tag = lookup.get(key, 'Untagged')
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
dir_path = '/workspaces/Process-Flow-Logs/'
flow_log_path = dir_path + 'logs.txt'
lookup_table_path = dir_path + 'lookup_table.csv'
protocol_numbers_path = dir_path + 'protocol_numbers.csv'
tag_output_path = dir_path + 'output_tag_counts.csv'
combination_output_path = dir_path + 'output_combination_counts.csv'
obj = ProcessLogs()
obj.process_flow_logs(flow_log_path, lookup_table_path, protocol_numbers_path, tag_output_path, combination_output_path)