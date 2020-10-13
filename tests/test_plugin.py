# -*- coding: utf-8 -*-
import time

import pytest

sleep = 1
uri = "ip:192.168.86.35"
devs = [
    "ad7291",
    "ad9361-phy",
    "xadc",
    "ad9517-3",
    "cf-ad9361-dds-core-lpc",
    "cf-ad9361-lpc",
]


# Mocks
def mock_Context(uri):
    class Channel(object):
        scan_element = True

    class Device(object):
        channels = [Channel()]

        def __init__(self, name):
            self.name = name

    class Context(object):
        def __init__(self, uri, devs):
            self.attrs = {"uri": uri}
            self.devices = []
            for dev in devs:
                self.devices.append(Device(dev))

    return Context(uri, devs)


def mock_scan_contexts():
    info = uri[2:] + " "
    uri_s = "ip:" + info
    info += "(" + ",".join(devs) + ")"
    ctxs = {uri_s: info}

    return ctxs


# Tests
def test_check_version():
    from pytest_libiio import __version__ as v
    import re

    matched = re.match("[0-9].[0-9].[0-9]", v)
    assert bool(matched)


def test_context_fixture_smoke(testdir, use_mocking, mocker):
    """Make sure that pytest accepts our fixture."""
    if use_mocking:
        mocker.patch("iio.scan_contexts", mock_scan_contexts)
        mocker.patch("iio.Context", mock_Context)

    time.sleep(sleep)

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        def test_sth(context_desc):
            print(context_desc)
            assert isinstance(context_desc,list)

    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest("--scan-verbose", "-v", "-s")

    # fnmatch_lines does an assertion internally
    print(result.stdout.str())
    assert "PASSED" in result.stdout.str()
    assert result.ret == 0


def test_context_fixture_uri_unknown(testdir, use_mocking, uri_select, mocker):
    """Make sure that pytest accepts our fixture."""
    if use_mocking:
        mocker.patch("iio.scan_contexts", mock_scan_contexts)
        mocker.patch("iio.Context", mock_Context)

    time.sleep(sleep)

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        def test_sth(context_desc):
            assert context_desc
            found = False
            for ctx in context_desc:
                if ctx['hw'] == 'Unknown':
                    found = True
            assert found
    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest("--uri=" + uri_select, "--scan-verbose", "-v", "-s")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_sth PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_context_fixture_scan_adi_map(testdir, use_mocking, hw_select, mocker):
    """Make sure that pytest accepts our fixture."""
    if use_mocking:
        mocker.patch("iio.scan_contexts", mock_scan_contexts)
        mocker.patch("iio.Context", mock_Context)

    time.sleep(sleep)

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        def test_sth(context_desc):
            assert context_desc
            found = False
            for ctx in context_desc:
                if ctx['hw'] == '"""
        + hw_select
        + """':
                    found = True
            assert found
    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest("--adi-hw-map", "-v", "-s")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_sth PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_context_fixture_uri_adi_map(
    testdir, use_mocking, uri_select, hw_select, mocker
):
    """Make sure that pytest accepts our fixture."""
    if use_mocking:
        mocker.patch("iio.scan_contexts", mock_scan_contexts)
        mocker.patch("iio.Context", mock_Context)

    time.sleep(sleep)

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        def test_sth(context_desc):
            assert context_desc
            found = False
            for ctx in context_desc:
                if ctx['hw'] == '"""
        + hw_select
        + """':
                    found = True
            assert found
    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest("--adi-hw-map", "--uri=" + uri_select, "-v", "-s")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_sth PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_context_desc_fixture_uri_adi_map(
    testdir, use_mocking, uri_select, hw_select, mocker
):
    """Make sure that pytest accepts our fixture."""
    if use_mocking:
        mocker.patch("iio.scan_contexts", mock_scan_contexts)
        mocker.patch("iio.Context", mock_Context)

    time.sleep(sleep)

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.iio_hardware('"""
        + hw_select
        + """')
        def test_sth(context_desc):
            assert context_desc
            found = False
            for ctx in context_desc:
                if ctx['hw'] == '"""
        + hw_select
        + """':
                    found = True
            assert found
    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest("--adi-hw-map", "--uri=" + uri_select, "-v", "-s")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_sth PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


# def test_help_message(testdir):
#     result = testdir.runpytest("--help",)
#     # fnmatch_lines does an assertion internally
#     result.stdout.fnmatch_lines(["libiio:", "*--uri=URI*Set libiio URI to utilize"])


# def test_print_scan_message(testdir):
#     result = testdir.runpytest("--scan-verbose", "--help")
#     # fnmatch_lines does an assertion internally
#     result.stdout.fnmatch_lines(
#         ["libiio:", "*--uri=URI*Set libiio URI to utilize",]
#     )
