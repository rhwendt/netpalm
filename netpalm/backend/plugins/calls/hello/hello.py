import logging

from netpalm.backend.core.utilities.rediz_meta import write_meta_error
from netpalm.backend.plugins.drivers.ncclient.ncclient_drvr import ncclien

log = logging.getLogger(__name__)


def hello(**kwargs):
    """main function for getting device capabilities via a library """
    log.debug(f'called w/ {kwargs}')
    lib = kwargs.get("library", False)

    result = False

    try:
        result = {}
        if lib == "ncclient":
            ncc = ncclien(**kwargs)
            sesh = ncc.connect()
            result = ncc.getcapabilities(sesh)
            ncc.logout(sesh)
        else:
            raise NotImplementedError(f"unknown 'library' parameter {lib}")
    except Exception as e:
        write_meta_error(f"{e}")

    return result
