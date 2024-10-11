
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
from sklearn.feature_extraction.text import TfidfVectorizer
from pyvis.network import Network
import networkx as nx

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
    with subprocess.Popen(command,
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    text = True,
                    shell = False
                    ) as process:
        try:
            std_out, std_err = process.communicate(timeout=max_wait)
            output = ''.join(re.findall('PASS|FAIL', std_out.strip()))
            if std_err:
                output += '  {{Implementation Error}}@[' + \
                    std_err.strip().replace('\n','').replace(',', '') + ']'
            return output
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as err:
            if isinstance(err, subprocess.TimeoutExpired):
                kill(process.pid)
                return '  {{TimeOut Error}}  '
            return '  {{RunTime Error}}  '

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
    data_frame = pd.read_csv(csv_file)

    # Remove duplicate IDs (remain the maximum score value)
    data_frame = data_frame.sort_values('Score', ascending=False)\
                .drop_duplicates('ID').sort_values('ID')

    # Write the updated data to the CSV file
    data_frame.to_csv(csv_file, index=False)


def detect_similarity(submission_dir, hw_str, threshold):
    """
    check the similarity between files under a directory.
    """

    matlab_documents = []
    matlab_users = []

    python_documents = []
    python_users = []

    for student_dir in os.listdir(submission_dir):
        if os.path.isdir(os.path.join(submission_dir, student_dir)):
            if os.path.exists(os.path.join(submission_dir, student_dir, hw_str + '.m')):
                with open(os.path.join(submission_dir, student_dir, hw_str + '.m'),
                          'r', encoding='utf-8') as file:
                    matlab_documents.append( file.read() )
                    matlab_users.append(student_dir)
            if  os.path.exists(os.path.join(submission_dir, student_dir, hw_str + '.py')):
                with open(os.path.join(submission_dir, student_dir, hw_str + '.py'),
                          'r', encoding='utf-8') as file:
                    python_documents.append( file.read() )
                    python_users.append(student_dir)

    network = Network('1200px', '1200px')

    g_matlab = check_similarity(matlab_documents, matlab_users, threshold)
    nx.draw(g_matlab, with_labels = True)
    network.from_nx(g_matlab)
    network.show('matlab.html', notebook=False)


    network = Network('1200px', '1200px')

    g_python = check_similarity(python_documents, python_users, threshold)
    nx.draw(g_python, with_labels = True)
    network.from_nx(g_python)
    network.show('python.html', notebook=False)


def check_similarity(documents, users, threshold):
    """
    check the similarity between documents.
    """

    tfidf = TfidfVectorizer().fit_transform(documents)

    pairwise_similarity = tfidf * tfidf.T

    graph_similarity = nx.Graph()

    for i, user_i in enumerate(users):
        for j, user_j in enumerate(users):
            if i > j and pairwise_similarity[i, j] > threshold:
                graph_similarity.add_edge(user_i.split('_')[0],
                                          user_j.split('_')[0],
                                          title=str(pairwise_similarity[i, j]))

    return graph_similarity
