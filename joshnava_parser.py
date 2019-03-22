import ipaddress
from itertools import groupby
import re

class Vulnerability():
    '''
    A class to store vulnerabilities and their useful information
    '''
    def __init__(self,key='',summary='',lab_id=0,ip=0):
        self.key = key
        self.summary = summary
        self.lab_id = lab_id
        self.ip = ipaddress.ip_address(ip)

    def __str__(self):
        return f'Key: {self.key}\tSummary: {self.summary}\n\tLab ID: {self.lab_id}\tIP: {self.ip}'

def parse_file(ifile):
    '''
    Input: A raw text file of all vulnerability information
    Output: A list of vunerabilities grouped by key
    '''
    # empty object list to return
    long_list = []
    # flag to check for garbage text
    vuln_starts = False

    # read the file line by line and save into list
    text = open(ifile, 'r').readlines()
    for line in text:
        # splitting the list into categories based on tab character
        categories = re.split(r'\t+', line.rstrip('\n'))
        # create a long_list that is divided by \n and \t
        for section in categories:
            if section[0:5] == 'CLVM-':
                # set escape character to separate vulnerabilities
                long_list.append('||')
                vuln_starts = True
            if not vuln_starts:
                continue
            long_list.append(section)
    # split list into sections per vulnerability based on escape character '||'
    vulnerabilities = [list(group) for k, group in groupby(long_list, lambda x: x == "||") if not k]

    return vulnerabilities

def create_useful_vulnerability_list(vulnerability_list):
    '''
    This function can be changed if more information about each vulnerability is needed
    Input: A list of all vulnerabilities grouped by key
    Output: List of necessary vulnerability information
    '''
    # create an empty list of vulnerabilities
    # NOTE: some entries have a port # and others do not
    vulnerabilities = []
    for vulnerability in vulnerability_list:
        # if port number is included in entry, skip the port number and add IP address at [4]
        if '.' not in vulnerability[3]:
            vuln = Vulnerability(vulnerability[0],vulnerability[1],vulnerability[2],vulnerability[4])
            vulnerabilities.append(vuln)
        # no port number is included in entry, add IP address at [3]
        else:
            vuln = Vulnerability(vulnerability[0],vulnerability[1],vulnerability[2],vulnerability[3])
            vulnerabilities.append(vuln)
    # a full useful list of vulnerabilities is returned
    return vulnerabilities

if __name__ == "__main__":
    vulnerability_list = parse_file('vulnerabilities.txt')
    vulnerability_list = create_useful_vulnerability_list(vulnerability_list)
    # sort the list by IP address
    vulnerability_list.sort(key=lambda x: x.ip)
#    for vulnerability in vulnerability_list:
#        print(vulnerability.ip)
    print(f'There are: {len(vulnerability_list)} vulnerabilities\n')