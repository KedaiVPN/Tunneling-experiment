#!/usr/bin/env python3
import asyncio
import os
import sys
from protocols import ssh_handler, v2ray_handler, trojan_handler
from utils import monitor, logger, cert_manager, colors
from utils.user_management import UserManager
from utils.terminal_menu import TerminalMenu
from config import Config

async def main():
    print(f"{colors.HEADER}Multi-Protocol Tunneling Server{colors.ENDC}")

    # Initialize components
    config = Config()
    log = logger.Logger()
    cert_mgr = cert_manager.CertificateManager()

    # Initialize user management
    user_mgr = UserManager(config, log)

    # Check if user management menu was requested
    if len(sys.argv) > 1 and sys.argv[1] == '--manage-users':
        menu = TerminalMenu(user_mgr, log)
        menu.run()
        return

    # Initialize protocol handlers
    ssh = ssh_handler.SSHHandler(config, log)
    v2ray = v2ray_handler.V2RayHandler(config, log)
    trojan = trojan_handler.TrojanHandler(config, log)

    # Start monitoring
    system_monitor = monitor.Monitor([ssh, v2ray, trojan], log)

    try:
        # Start all services
        await asyncio.gather(
            ssh.start(),
            v2ray.start(),
            trojan.start(),
            system_monitor.start_monitoring()
        )
    except Exception as e:
        print(f"{colors.FAIL}Error starting services: {str(e)}{colors.ENDC}")
        log.error(f"Startup error: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{colors.WARNING}Shutting down services...{colors.ENDC}")