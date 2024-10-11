# Grading Tool

A python code to grade the homework on canvas.

## Requirement

MATLAB and Python are installed.

```bash
pip install -r requirements.txt
```

## Usage

- Clone this project and ``cd`` to the repo folder.
- Download the submissions (one zip file) from canvas to the same folder.
- Prepare the test files in a directory, say ``/tests``, see the example tests for a reference.
- Run the python file ``main.py``.
- After grading, run the python file ``similarity_check`` to check the similarity between students' submissions. It will create webpages.

## Output

The score will be stored in csv format.
