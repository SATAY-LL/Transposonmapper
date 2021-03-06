from transposonmapper.importing import verify_data_files
import os
import pkg_resources
import pytest


def test_packaged_data_files():
    """Test if all required data files are packaged(positive control for the data files path)"""
    data_path = pkg_resources.resource_filename("transposonmapper", "data_files/")
    try:
        verify_data_files(path=data_path)
    except AssertionError as err:
        assert False, f"packaged data raises an error: {err}"


def test_incorrect_data_path():
    """Test assertion error on incorrect data pathc(negative control for the path)"""
    data_path = "/incorrect_path/"
    with pytest.raises(AssertionError) as err:
        verify_data_files(data_path)

    assert err.type == AssertionError
    assert f"{data_path} was not found." in str(err.value)


def test_incorrect_data_files():
    """Test assertion error on incorrect data file (negative control for the file type and path)"""
    data_path = pkg_resources.resource_filename("transposonmapper", "data_files/")
    file_type = "test_type"
    file_path = "test_file"
    with pytest.raises(AssertionError) as err:
        verify_data_files(path=data_path, data_files={file_type: file_path})

    assert err.type == AssertionError
    assert f"{file_type} not found at {os.path.join(data_path, file_path)}" in str(
        err.value
    )

