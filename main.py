"""
Test script for grading homework.
"""
from grader import Grader

# Initialize the grader
# The first argument is the submission file (downloaded from Canvas)
# The second argument is the submission directory (where the files will be extracted)
# The third argument is the test directory (where the test files are located)
# The fourth argument is the wait time for each test (in seconds)
# You may not need to change these arguments
g = Grader('submissions.zip', 'submissions', 'tests', wait_time=60)

# Grade the students
# The argument is the homework string (hw00, hw01, etc.)
# The output file is the CSV file where the grades will be saved
g.grade(hw_str='hw00', output_file='grades.csv')
