from unittest import mock
from unittest.mock import patch, mock_open
import pytest
from main import *
import os



@mock.patch("main.iterOverDirectory", side_effect=[{"1": {"test/v", "test/vv"},
                                                    "2": {"test/x", "test/xx"}},
                                                   {"1": {"test/v", "test/vy"},
                                                    "3": {"test/q"}}
                                                   ])
def test_findDuplicate_mock(mock_iteroverdirectory):
    path_arr = ["test", "test2"]
    ans = findDuplicate(path_arr)
    mock_iteroverdirectory.assert_called()
    assert mock_iteroverdirectory.call_count == len(path_arr)
    expected = {"1": {"test/v", "test/vv", "test/vy"}, "2": {"test/x", "test/xx"}}
    for a in ans.keys():
        assert a in expected
        for p in ans[a]:
            assert p in expected[a]


def mock_hash(path):
    a = {
        "/test\\mock_file": "MH-1",
        "/test\\mock_file_copy": "MH-1",
        "/test\\mock_file2_copy": "MH-2",
        "/test/subtest1\\mock_file2": "MH-2",
        "/test/subtest2\\mock_file_copy(1)": "MH-1",
        "/test/subtest/subsubtest\\mock_file2_copy(1)": "MH-2"
    }
    if path in a:
        return a[path]
    return path


@mock.patch('os.walk')
def test_iterOverDirectory(mockwalk):
    with patch('main.hashFile') as mockhash:
        mockwalk.return_value = [
            ('/test', ('subtest1', 'subtest2'), ("mock_file", "mock_file_copy", "mock_file2_copy")),
            ('/test/subtest1', ('subsubtest'), ("spam", "mock_file2", "noise")),
            ('/test/subtest2', (), ("mock_file_copy(1)", "not_relevant")),
            ('/test/subtest2/subsubtest', (), ("mock_file2_copy(1)", "dirt"))
        ]
        mockhash.side_effect = mock_hash
        ans = findDuplicate("/test")
        expected = {
            "MH-1": {"/test\\mock_file", "/test\\mock_file_copy", "/test/subtest2\\mock_file_copy(1)"},
            "MH-2": {"/test\\mock_file2_copy", "/test/subtest1\\mock_file2",
                     "/test/subtest/subsubtest\\mock_file2_copy(1)"}
        }
        for a in ans.keys():
            assert a in expected
            for p in ans[a]:
                assert p in expected[a]

def create_file_system_and_exep_output(tmpdir):

    sub_dir_1 = tmpdir.mkdir("sub_dir_1")
    p1 = sub_dir_1.join("hello.txt")
    p1.write("content")
    p2 = sub_dir_1.join("bye.txt")
    p2.write("contentt")
    p3 = sub_dir_1.join("info.txt")
    p3.write("content's")

    sub_dir_2 = tmpdir.mkdir("sub_dir_2")
    p4 = sub_dir_2.join("test.txt")
    p4.write("content")
    p5 = sub_dir_1.join("fake.txt")
    p5.write("contents")

    sub_sub_dir_1 = sub_dir_1.mkdir("sub_sub_dir_1")
    p6 = sub_sub_dir_1.join("panic.txt")
    p6.write("content")
    p7 = sub_dir_1.join("fake.txt")
    p7.write("contentss")
    p8 = sub_dir_1.join("tut.txt")
    p8.write("conten")
    exe = {hashFile(p1): {p1.strpath, p4.strpath, p6.strpath}}
    return exe,[sub_dir_1, sub_dir_2, sub_sub_dir_1]


def test_create_file(tmpdir):
    expected, ffs_list = create_file_system_and_exep_output(tmpdir)
    ans = findDuplicate(ffs_list)
    for a in ans:
        assert a in expected
        for p in ans[a]:
            b = expected[a]
            c = p
            assert p in expected[a]