"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
from python_part_2.task_read_write_2 import read_write_2


def test_read_write_2(tmpdir, mocker):
    mocker.patch('python_part_2.task_read_write_2.generate_words', return_value=['abc', 'def', 'xyz'])
    file_1 = tmpdir.join('file_1.txt')
    file_2 = tmpdir.join('file_2.txt')
    read_write_2(file_1, file_2, 3)

    assert file_1.read() == "abc\ndef\nxyz"
    assert file_2.read() == "xyz,def,abc"