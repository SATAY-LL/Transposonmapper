import sys
import os
import mock
import pytest
import pkg_resources

from transposonmapper import transposonmapper


def test_raise_exception_pysam():
    """Test the exception raised when pysam is not installed    
    """
    data_path = pkg_resources.resource_filename(
        "transposonmapper", "data_files/files4test"
    )
    filename = "SRR062634.filt_trimmed.sorted.bam"
    filepath = os.path.join(data_path, filename)

    with mock.patch.dict(sys.modules, {"pysam": None}):
        with pytest.raises(SystemExit) as e:
            transposonmapper(bamfile=filepath)
        assert e.type == SystemExit
        assert e.value.code == 1
