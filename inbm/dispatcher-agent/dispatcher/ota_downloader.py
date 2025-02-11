"""
    Downloads OTA file

    Copyright (C) 2017-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import abc
import logging
from typing import Optional, Any, Mapping

from inbm_common_lib.utility import canonicalize_uri, CanonicalUri

from dispatcher.constants import UMASK_OTA, REPO_CACHE
from dispatcher.dispatcher_exception import DispatcherException
from dispatcher.downloader import download
from dispatcher.packagemanager.local_repo import DirectoryRepo
from .dispatcher_broker import DispatcherBroker

logger = logging.getLogger(__name__)


class OtaDownloader(metaclass=abc.ABCMeta):
    """Base class for starting OTA downloader.

    @param parsed_manifest:
    """

    def __init__(self,
                 parsed_manifest: Mapping[str, Optional[Any]]) -> None:

        self._parsed_manifest = parsed_manifest
        if 'uri' in parsed_manifest and parsed_manifest['uri'] is not None:
            self._uri: CanonicalUri = canonicalize_uri(parsed_manifest['uri'])
        else:
            raise DispatcherException('no URI provided to OtaDownloader')

        repo = parsed_manifest.get('repo', None)
        self._repo = repo if repo else DirectoryRepo(REPO_CACHE)
        self._username = parsed_manifest['username']
        self._password = parsed_manifest['password']

    def download(self) -> None:
        pass


class FotaDownloader(OtaDownloader):
    """Performs OTA download.

    @param dispatcher_broker: DispatcherBroker object used to communicate with other INBM services
    @param parsed_manifest:
    """

    def __init__(self,
                 dispatcher_broker: DispatcherBroker,
                 parsed_manifest: Mapping[str, Optional[Any]]) -> None:
        super().__init__(parsed_manifest)
        self._dispatcher_broker = dispatcher_broker

    def download(self) -> None:
        """Starts the FOTA download.  Used when in a host/node scenario.  If not, download will be performed by
        the FOTA thread.
        """
        logger.debug("")
        download(dispatcher_broker=self._dispatcher_broker,
                 uri=self._uri,
                 umask=UMASK_OTA,
                 repo=self._repo,
                 username=self._username,
                 password=self._password)


class SotaDownloader(OtaDownloader):
    """"Performs SOTA download.

    @param parsed_manifest:
    """

    def __init__(self,
                 parsed_manifest: Mapping[str, Optional[Any]]) -> None:
        super().__init__(parsed_manifest)

    def download(self) -> None:
        """Starts the SOTA download.  Used when in a host/node scenario.  If not, download will be performed by
        the SOTA thread.
        """
        logger.debug("Currently not used.")


class AotaDownloader(OtaDownloader):
    """"Performs thread synchronization, AOTA and returns the result.

    @param parsed_manifest:
    """

    def __init__(self,
                 parsed_manifest: Mapping[str, Optional[Any]]) -> None:
        super().__init__(parsed_manifest)

    def download(self) -> None:
        """Starts the AOTA download.  Used when in a host/node scenario.  If not, download will be performed by
        the AOTA thread.
        """
        logger.debug("Currently not used.")
