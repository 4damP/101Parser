## Routine to remove quotes and commas from descriptions
## to import 101 entries
## regex to match , between "" : ("[^",]+),([^"]+")

import argparse
import csv
import os

def parse_file(filename):
    print('parse_file function=> Opening file: {}'.format(filename))
    batch_list = {}
    with open(filename) as fn:
        try:
            for line in fn:
                line_list = line.split('","')
                if line_list[5] == 'JOURNAL':
                    continue
                else:
                    i = 0
                    dept_no = line_list[0][-2:]
                    batch = line_list[9].strip('\r\n').strip('"')
                    idate = line_list[3]
                    amt = line_list[5].split(',')
                    amount = float(amt[2])
                    # print('{:12}{:12}{:16,.2f}'.format(idate, batch, amount))
                    if dept_no not in batch_list:
                        batch_list[dept_no] = {batch: [idate, amount]}
                    elif batch not in batch_list[dept_no]:
                        batch_list[dept_no][batch] = [idate, amount]
                    else:
                        batch_list[dept_no][batch][1] += amount
                        
        except Exception as e:
            print(str(e))
    return batch_list
    
def write_report(parsed_data):
    with open('101.txt', 'w') as report:
        depts = sorted(parsed_data.keys())
        for dept in depts:
            report.write('{}\r\n'.format('*'*60))
            report.write('Dept No: {:^10}\r\n'.format(dept))
            # print(parsed_data[dept])
            batches = sorted(parsed_data[dept].keys())
            # print(batches)
            sum_total = 0
            for e in batches:
                report.write('{:20}{:<20}{:20,.2f}'.format(e, parsed_data[dept][e][0], parsed_data[dept][e][1]))
                report.write('\r\n')
                sum_total += parsed_data[dept][e][1]
            report.write('{}\r\n'.format('='*60))
            report.write('{:20}{:>20}{:20,.2f}\r\n'.format(' ', 'Sum Total: ', sum_total))
    report.close()
    print('File 101.txt complete')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help="Enter filename you want to parse as first argument")
    args = parser.parse_args()
    print('Opening file: {}'.format(args.file))
    parsed_data = parse_file(args.file)
    write_report(parsed_data)