from grader import Grader

# Initialize the grader
# The first argument is the submission file (downloaded from Canvas)
# The second argument is the submission directory (where the files will be extracted)
# The third argument is the test directory (where the test files are located)
# You may not need to change these arguments
g = Grader('submissions.zip', 'submissions', 'tests')

# Grade the students
# The argument is the homework string (hw00, hw01, etc.)
g.grade(hw_str='hw00')