"""
    Main .py file for Dispatcher agent -- contains main() method

    Copyright (C) 2017-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import platform
import sys
from typing import List

from dispatcher.install_check_service import InstallCheckService
from dispatcher.dispatcher_class import Dispatcher
from dispatcher.dispatcher_broker import DispatcherBroker
from inbm_lib.windows_service import WindowsService


def make_dispatcher(args: List[str]) -> Dispatcher:
    """Make a dispatcher with the given args.

    Handle dependency injection in one place"""
    broker = DispatcherBroker()
    return Dispatcher(args=args, broker=broker, install_check_service=InstallCheckService(broker))


class WindowsDispatcherService(WindowsService):
    _svc_name_ = 'inbm-dispatcher'
    _svc_display_name_ = 'Dispatcher Agent'
    _svc_description_ = 'Intel Manageability coordinating agent'

    def __init__(self, args: List[str]) -> None:
        if args is None:
            args = []

        self.dispatcher = make_dispatcher(args)

        super().__init__(args)

    def svc_stop(self) -> None:
        self.dispatcher.stop()

    def svc_main(self) -> None:
        self.start()


def main() -> None:
    """Function called by __main__."""

    if platform.system() == 'Windows':
        import servicemanager
        import win32serviceutil

        if len(sys.argv) == 1:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(WindowsDispatcherService)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            win32serviceutil.HandleCommandLine(WindowsDispatcherService)
    else:
        dispatcher = make_dispatcher(sys.argv)
        dispatcher.start()


if __name__ == "__main__":
    main()
