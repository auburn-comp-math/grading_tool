"""
Grader class that grades students with matlab tests or python tests.
"""

import os
import shutil
import zipfile
from pathlib import Path
from time import time

import requests

from utility import execute_system_call, find_emails, extract_link, unzip, remove_duplicates

NULL_EMAIL = 'null___@null__.___'

class Grader():
    """
    Grader class that grades students with matlab tests or python tests.
    """
    def __init__(self, submission_file, submission_dir, test_dir, wait_time=30):
        self.total_students = -1
        self.submission_file = submission_file
        self.submission_dir = submission_dir
        self.test_dir = test_dir
        self.wait_time = wait_time

        self.matlab_test = []
        self.python_test = []


        for file in os.listdir(test_dir):
            if file.endswith('.m'):
                self.matlab_test.append(file)
            elif file.endswith('.py'):
                self.python_test.append(file)

        print(f"MATLAB test {self.matlab_test} found!\n")
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
                req = requests.get(zip_link, allow_redirects=True, timeout=10)
                with open(
                    f'{os.path.join(self.submission_dir, Path(student_dir).stem)}.zip'\
                        , 'wb') as f_in:
                    f_in.write(req.content)
                student_dirs.add(f'{os.path.join(self.submission_dir, Path(student_dir).stem)}.zip')
        return student_dirs

    def matlab_grade(self, student_path, hw_str='hw00'):
        """
        Grade the student's MATLAB code

        @param student_path: The student's directory
        @param hw_str: The homework string
        """
        with open(os.path.join(student_path, hw_str + '.m'), 'r',\
                   encoding='utf-8', errors='ignore') as code_file:
            # get author information
            email = ' '.join(find_emails(code_file.readlines()[0]))
            if email.find('@')== -1:
                email = NULL_EMAIL
            # copy the test file to the student's directory
            for _test in self.matlab_test:
                shutil.copy(os.path.join(self.test_dir, _test), student_path)
            # run the test file
            student_score = ""
            for _test in self.matlab_test:
                student_score += execute_system_call(\
                        f'matlab -nojvm -nosplash -nodesktop -batch \
                        "run(\'{os.path.join(student_path, _test)}\');exit;"',
                        max_wait=self.wait_time)
            return student_score.count('PASS'), email, student_score

    def python_grade(self, student_path, hw_str='hw00'):
        """
        Grade the student's Python code

        @param student_path: The student's directory
        @param hw_str: The homework string
        """
        with open(os.path.join(student_path, hw_str + '.py'), 'r', \
                  encoding='utf-8', errors='ignore') as code_file:
            # get author information
            email = ' '.join(find_emails(code_file.readlines()[0]))
            if email.find('@')== -1:
                email = NULL_EMAIL
            # copy the test file to the student's directory
            for _test in self.python_test:
                shutil.copy(os.path.join(self.test_dir, _test), student_path)
            # run the test file
            student_score = ""
            for _test in self.python_test:
                student_score += execute_system_call(\
                        f'python \"{os.path.join(student_path, _test)}\"',
                        max_wait=self.wait_time)
            return student_score.count('PASS'), email, student_score

    def convert_to_python(self, student_path, hw_str='hw00'):
        """
        Convert the student's Jupyter notebook to Python script

        @param student_path: The student's directory
        @param hw_str: The homework string
        """
        execute_system_call(f'jupyter nbconvert --to python\
                             {os.path.join(student_path, hw_str + ".ipynb")}',
                            max_wait=self.wait_time)

    def grade_exception_file(self, hw_str, student_dir):
        """
        Handle the file name exceptions

        @param hw_str: The homework string
        @param student_dir: The student directory
        """
        local_files = os.listdir(os.path.join(student_dir))
        for _file in local_files:
            if _file.startswith('.') or _file.find('test') != -1:
                local_files.remove(_file)

        student_code = 'unknown'
        cnt_passes = 0
        msg = ""
        email = NULL_EMAIL
        starting_time = time()

        if len(local_files) == 1: # only one file
            _file = local_files[0]
            if _file.endswith('.m') or _file.endswith('.asv'):
                student_code = 'matlab'
                shutil.copy(os.path.join(student_dir, _file), \
                        os.path.join(student_dir, hw_str+'.m'))
                cnt_passes, email, msg = self.matlab_grade(student_dir, hw_str)

            elif _file.endswith('.py'):
                student_code = 'python'
                shutil.copy(os.path.join(student_dir, _file), \
                        os.path.join(student_dir, hw_str+'.py'))
                cnt_passes, email, msg = self.python_grade(student_dir, hw_str)

            elif _file.endswith('.ipynb'):
                student_code = 'jupyter'
                try:
                    shutil.copy(os.path.join(student_dir, _file), \
                            os.path.join(student_dir, hw_str+'.ipynb'))
                except shutil.SameFileError:
                    pass

                self.convert_to_python(student_dir, hw_str)
                cnt_passes, email, msg = self.python_grade(student_dir, hw_str)

            else:
                # try to run with MATLAB or Python
                shutil.copy(os.path.join(student_dir, _file), \
                        os.path.join(student_dir, hw_str+'.m'))
                cnt_passes, email, msg = self.matlab_grade(student_dir, hw_str)
                running_time = time() - starting_time
                if cnt_passes > 0:
                    return cnt_passes, email, 'matlab', running_time, msg

                shutil.copy(os.path.join(student_dir, _file), \
                        os.path.join(student_dir, hw_str+'.py'))
                cnt_passes, email, msg = self.python_grade(student_dir, hw_str)
                running_time = time() - starting_time
                if cnt_passes > 0:
                    return cnt_passes, email, 'python', running_time, msg

            running_time = time() - starting_time
            return cnt_passes, email, student_code, running_time, msg

        student_code = 'multi-f'
        return 0, NULL_EMAIL, student_code, 0, msg

    def grade_standard_file(self, hw_str, student_dir):
        """
        Grade the standard file name

        @param hw_str: The homework string
        @param student_dir: The student directory
        """
        data = []

        if os.path.exists(os.path.join(student_dir, hw_str + '.m')):
            student_code = 'matlab'
            starting_time = time()
            cnt_passes, email, msg = self.matlab_grade(student_dir, hw_str)
            running_time = time() - starting_time
            data.append( (cnt_passes, email, student_code, running_time, msg))

        if os.path.exists(os.path.join(student_dir, hw_str + '.py')):
            student_code = 'python'
            starting_time = time()
            cnt_passes, email, msg = self.python_grade(student_dir, hw_str)
            running_time = time() - starting_time
            data.append( (cnt_passes, email, student_code, running_time, msg))

        return data

    def println(self, i, student_info, item):
        """
        Print the student's score

        @param i: The student index
        @param student_info: The student information
        @param item: The student item
        """
        cnt_passes, email, student_code, running_time, msg = item
        msg = msg.replace('PASS', 'P').replace('FAIL', 'F')

        if msg.find('@') != -1:
            msg = msg[:msg.find('@')]

        print(f'Student {(i+1): 3d}/{self.total_students: 3d} \t'\
              f'scored: {cnt_passes:4d} | {student_info[0]:<20} | {student_info[1]} | '\
              f'{email: <25} | {student_code:<8} | {running_time: 6.2f} sec | {msg:<25}\n')

    def output(self, grades_file, i, student_info, data):
        """
        Output the grades to the file

        @param grades_file: The grades file
        @param i: The student index
        @param student_info: The student information
        @param data: The student data
        """
        for _item in data:
            cnt_passes, email, student_code, running_time, msg = _item
            self.println(i, student_info, _item)
            msg = msg.replace('PASS', 'P').replace('FAIL', 'F')
            grades_file.write(f'{student_info[0]:<20}, {student_info[1]}, ' \
                              f'{email:<25}, {student_code:<8}, {cnt_passes:4d}, ' \
                              f'{running_time: 6.2f} sec, {msg:<25}\n')

    def grade(self, hw_str='hw00', output_file='grades.csv'):
        """
        Grade the students

        @param hw_str: The homework string
        @param output_file: The output file
        """
        # create a file to store the grades
        with open(output_file, 'w', encoding='utf-8') as grades_file:
            grades_file.write('Name,ID,Email,Language,Score,RunTime,Message\n')
            # Unzip the submission file
            if not os.path.exists(self.submission_dir):
                print('Unzipping the submission file ...')
                unzip(self.submission_file, self.submission_dir, skip_dir=False)

            print(f'Submissions unzipped in {self.submission_dir}\n')

            student_dirs = self.get_dirs()

            self.total_students = len(student_dirs)

            for i, student_file in enumerate(student_dirs):
                student_dir = os.path.join(self.submission_dir, Path(student_file).stem)
                try:
                    unzip(student_file, student_dir)
                except zipfile.BadZipFile:
                    print(f'Bad zip file: {student_file}')
                    continue

                student_info = Path(student_file).stem.split('_')[:2]

                if student_info[-1] == 'LATE':
                    student_info = Path(student_file).stem.split('_')[0], \
                        Path(student_file).stem.split('_')[2]

                data = self.grade_standard_file(hw_str, student_dir)

                if len(data) > 0:
                    self.output(grades_file, i, student_info, data)
                else:
                    data.append(self.grade_exception_file(hw_str, student_dir))
                    self.output(grades_file, i, student_info, data)

        grades_file.close()
        print(f'\nGrades saved in {output_file}\n')
        print('Cleaning up ...')
        remove_duplicates(output_file)
        print('==============  Grading completed! =============\n\n')
