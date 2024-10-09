
"""
Utility functions.
"""

import os
import re
import zipfile
import subprocess
import psutil
import pandas as pd
from bs4 import BeautifulSoup


def kill(proc_pid):
    """
    kill the process with the given PID
    """
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def execute_system_call(command, max_wait=30):
    """
    Execute a system call and return the output
    """
    process = subprocess.Popen(command,
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    text = True,
                    shell = False
                    )
    print(process.pid)
    try:
        std_out, std_err = process.communicate(timeout=max_wait)
        output = " ".join(re.findall('PASS|FAIL', std_out.strip()))
        if std_err:
            output += "  {{Implementation Error}}@[" + std_err.strip().replace("\n","").replace(",", "") + "]"
        return output
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
        if isinstance(e, subprocess.TimeoutExpired):
            kill(process.pid)
            return "  {{TimeOut Error}}"
        return "  {{RunTime Error}}"

def find_emails(text):
    """
    Find all email addresses in the text using regular expressions.
    """
    # Define the regular expression pattern for matching email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    # Find all email addresses in the text using the regular expression pattern
    emails = re.findall(email_pattern, text)
    return emails


def extract_link(link_file_path):
    """
    Extract HTML content to a link using BeautifulSoup.
    """
    with open(link_file_path, 'r', encoding='utf-8') as link_file:
        index = link_file.read()
        link = BeautifulSoup(index, 'lxml').body.a['href']
        if link.endswith('.git'):
            return link[:-4]
        if link.find('blob') != -1:
            return link[:link.find('blob')]
        if link.find('tree') != -1:
            return link[:link.find('tree')]
        return link


def unzip(file, file_dir, skip_dir=True):
    """
    Unzip the submission file
    """
    if not skip_dir:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(file_dir)
    else:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            for zip_info in zip_ref.infolist():
                if zip_info.is_dir():
                    continue
                zip_info.filename = os.path.basename(zip_info.filename)
                zip_ref.extract(zip_info, file_dir)

def remove_duplicates(csv_file):
    """
    Remove duplicate IDs (remain the maximum score value) in the CSV file with panda
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Remove duplicate IDs (remain the maximum score value)
    df = df.sort_values('Score', ascending=False).drop_duplicates('ID').sort_values('ID')

    # Write the updated data to the CSV file
    df.to_csv(csv_file, index=False)
    