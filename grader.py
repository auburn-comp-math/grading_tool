"""
Grader class that grades students with matlab tests or python tests.
"""

import os
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def execute_system_call(command):
    """
    Execute a system call and return the output
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        # The code encounters a runtime error (due to implementation error).
        return "FAIL"

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
        elif link.find('blob') != -1:
            return link[:link.find('blob')]
        else:
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

class Grader():
    """
    Grader class that grades students with matlab tests or python tests.
    """
    def __init__(self, submission_file, submission_dir, test_dir):
        self.submission_file = submission_file
        self.submission_dir = submission_dir
        self.test_dir = test_dir


        for file in os.listdir(test_dir):
            if file.endswith('.m'):
                self.matlab_test = file
                print(f"MATLAB test {self.matlab_test} found!\n")
            elif file.endswith('.py'):
                self.python_test = file
                print(f"PYTHON test {self.python_test} found!\n")

        print('==============  Grader initialized! =============\n\n')

    def get_dirs(self):
        """
        Get the student directories
        """
        student_dirs = set()

        for student in os.listdir(self.submission_dir):
            student_dir = os.path.join(self.submission_dir, student)
            if student_dir.endswith('.zip'):
                student_dirs.add(student_dir)
            if student_dir.endswith('.html'):
                zip_link = extract_link(student_dir) + '/archive/refs/heads/main.zip'
                r = requests.get(zip_link, allow_redirects=True, timeout=10)
                with open(
                    f'{os.path.join(self.submission_dir, Path(student_dir).stem)}.zip', 'wb') as f:
                    f.write(r.content)
                student_dirs.add(f'{os.path.join(self.submission_dir, Path(student_dir).stem)}.zip')
        return student_dirs

    def matlab_grade(self, student_path, hw_str='hw00'):
        """
        Grade the student's MATLAB code
        """
        with open(os.path.join(student_path, hw_str + '.m'), 'r', encoding='utf-8') as code_file:
            # get author information
            email = ' '.join(find_emails(code_file.readlines()[0]))
            # copy the test file to the student's directory
            shutil.copy(os.path.join(self.test_dir, self.matlab_test), student_path)
            # run the test file
            student_score = execute_system_call(\
                    f'matlab -nojvm -nosplash -nodesktop -batch \
                    "run(\'{os.path.join(student_path, self.matlab_test)}\');exit;"')
            return student_score.count('PASS'), email

    def python_grade(self, student_path, hw_str='hw00'):
        """
        Grade the student's Python code
        """
        with open(os.path.join(student_path, hw_str + '.py'), 'r', encoding='utf-8') as code_file:
            # get author information
            email = ' '.join(find_emails(code_file.readlines()[0]))
            # copy the test file to the student's directory
            shutil.copy(os.path.join(self.test_dir, self.python_test), student_path)
            # run the test file
            student_score = execute_system_call(\
                    f'python {os.path.join(student_path, self.python_test)}')
            return student_score.count('PASS'), email

    def grade(self, hw_str='hw00', output_file='grades.csv'):
        """
        Grade the students

        @param hw_str: The homework string
        """
        # create a file to store the grades
        with open(output_file, 'w', encoding='utf-8') as grades_file:
            grades_file.write('Student, Email, Language, Score\n')
            # Unzip the submission file
            if not os.path.exists(self.submission_dir):
                print('Unzipping the submission file ...')
                unzip(self.submission_file, self.submission_dir, skip_dir=False)

            student_dirs = self.get_dirs()

            total_students = len(student_dirs)

            for i, student_file in enumerate(student_dirs):
                student_dir = os.path.join(self.submission_dir, Path(student_file).stem)
                unzip(student_file, student_dir)

                name = Path(student_file).stem[0:15]

                if os.path.exists(os.path.join(student_dir, hw_str + '.m')) or\
                     os.path.exists(os.path.join(student_dir, hw_str + '.py')):
                    if os.path.exists(os.path.join(student_dir, hw_str + '.m')):
                        matlab_cnt_passes, matlab_email  = self.matlab_grade(student_dir, hw_str)
                        if len(matlab_email) > 0 or matlab_cnt_passes > 0:
                            email = matlab_email

                            student_code = 'matlab'
                            print(
                            f'Student {(i+1): 3d}/{total_students: 3d}\
                            scored: {matlab_cnt_passes} | {student_dir} \n')
                            grades_file.write(
                                f'{name}, {email}, {student_code}, {matlab_cnt_passes}\n')
                    if os.path.exists(os.path.join(student_dir, hw_str + '.py')):
                        python_cnt_passes, python_email = self.python_grade(student_dir, hw_str)

                        if len(python_email) > 0 or python_cnt_passes > 0:
                            email = python_email

                            student_code = 'python'
                            print(
                            f'Student {(i+1): 3d}/{total_students: 3d}\
                            scored: {python_cnt_passes} | {student_dir} \n')
                            grades_file.write(
                                f'{name}, {email}, {student_code}, {python_cnt_passes}\n')

                else:
                    student_code = 'other'
                    grades_file.write(f'{name}, , ,\n')
                    