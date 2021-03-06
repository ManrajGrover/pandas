import pytest

from distutils.version import LooseVersion
import numpy
import pandas
import pandas.util.testing as tm
import dateutil


def pytest_addoption(parser):
    parser.addoption("--skip-slow", action="store_true",
                     help="skip slow tests")
    parser.addoption("--skip-network", action="store_true",
                     help="skip network tests")
    parser.addoption("--run-high-memory", action="store_true",
                     help="run high memory tests")
    parser.addoption("--only-slow", action="store_true",
                     help="run only slow tests")


def pytest_runtest_setup(item):
    if 'slow' in item.keywords and item.config.getoption("--skip-slow"):
        pytest.skip("skipping due to --skip-slow")

    if 'slow' not in item.keywords and item.config.getoption("--only-slow"):
        pytest.skip("skipping due to --only-slow")

    if 'network' in item.keywords and item.config.getoption("--skip-network"):
        pytest.skip("skipping due to --skip-network")

    if 'high_memory' in item.keywords and not item.config.getoption(
            "--run-high-memory"):
        pytest.skip(
            "skipping high memory test since --run-high-memory was not set")


# Configurations for all tests and all test modules

@pytest.fixture(autouse=True)
def configure_tests():
    pandas.set_option('chained_assignment', 'raise')


# For running doctests: make np and pd names available

@pytest.fixture(autouse=True)
def add_imports(doctest_namespace):
    doctest_namespace['np'] = numpy
    doctest_namespace['pd'] = pandas


@pytest.fixture(params=['bsr', 'coo', 'csc', 'csr', 'dia', 'dok', 'lil'])
def spmatrix(request):
    tm._skip_if_no_scipy()
    from scipy import sparse
    return getattr(sparse, request.param + '_matrix')


@pytest.fixture
def ip():
    """
    Get an instance of IPython.InteractiveShell.

    Will raise a skip if IPython is not installed.
    """

    pytest.importorskip('IPython', minversion="6.0.0")
    from IPython.core.interactiveshell import InteractiveShell
    return InteractiveShell()


is_dateutil_le_261 = pytest.mark.skipif(
    LooseVersion(dateutil.__version__) > '2.6.1',
    reason="dateutil api change version")
is_dateutil_gt_261 = pytest.mark.skipif(
    LooseVersion(dateutil.__version__) <= '2.6.1',
    reason="dateutil stable version")
