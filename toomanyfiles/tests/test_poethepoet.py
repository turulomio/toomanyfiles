"""Unit tests for poethepoet task functions."""

import pytest
from unittest.mock import patch
from toomanyfiles.poethepoet import release, video


def test_release():
    """Verify that release() executes without errors."""
    release()


def test_video_invalid_target():
    """Verify that video() exits when given an invalid target."""
    with patch("toomanyfiles.poethepoet.which", return_value="/usr/bin/vhs"):
        with pytest.raises(SystemExit):
            video(target="invalid_target")


def test_video_missing_vhs():
    """Verify that video() exits when vhs is not installed."""
    with patch("toomanyfiles.poethepoet.which", return_value=None):
        with pytest.raises(SystemExit):
            video()

