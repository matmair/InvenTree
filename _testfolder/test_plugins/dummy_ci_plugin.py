
from plugin import InvenTreePlugin

PLG_VERSION = "0.1.0"

print(">>> LOADING DUMMY PLUGIN v" + PLG_VERSION + " <<<")

class DummyCIPlugin(InvenTreePlugin):

    NAME = "DummyCIPlugin"
    SLUG = "dummyci"
    TITLE = "Dummy plugin for CI testing"

    VERSION = PLG_VERSION
