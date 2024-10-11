"""
check similarity
"""

from utility import detect_similarity

# Check the similarity between files under a directory
# The first argument is the submission directory
# The second argument is the homework string (hw00, hw01, etc.)
# The third argument is the threshold for similarity (0.0 to 1.0)

detect_similarity('submissions', 'hw00', 0.92)
