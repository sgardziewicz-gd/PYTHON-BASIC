"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
from python_part_2.task_read_write import read_write


def test_read_write(tmpdir):
    file = tmpdir.join("result.txt")
    read_write("practice/tests/data", file)
    assert file.read() == "23, 78, 3"