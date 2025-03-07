import asyncio
import psutil
from datetime import datetime
from utils.colors import *

class Monitor:
    def __init__(self, services, logger):
        self.services = services
        self.logger = logger
        self.update_interval = 5  # seconds

    async def start_monitoring(self):
        while True:
            try:
                await self._check_services()
                await self._log_system_stats()
                await asyncio.sleep(self.update_interval)
            except Exception as e:
                self.logger.error(f"Monitoring error: {str(e)}")

    async def _check_services(self):
        service_status = []
        for service in self.services:
            try:
                active_servers = sum(1 for server in service.servers if hasattr(server, 'is_serving') and server.is_serving())
                total_servers = len(service.servers)
                status = f"{service.__class__.__name__}: {active_servers}/{total_servers} active"
                service_status.append(status)

                if active_servers < total_servers:
                    inactive = [server for server in service.servers if not (hasattr(server, 'is_serving') and server.is_serving())]
                    for server in inactive:
                        print(f"{FAIL}Service down: {server}{ENDC}")
                        self.logger.error(f"Service down: {server}")
            except Exception as e:
                self.logger.error(f"Error checking service {service.__class__.__name__}: {str(e)}")
                service_status.append(f"{service.__class__.__name__}: Error")

        self.logger.info("Service Status: " + ", ".join(service_status))

    async def _log_system_stats(self):
        try:
            cpu_percent = psutil.cpu_percent()
            mem = psutil.virtual_memory()
            network = psutil.net_io_counters()

            stats = f"""
{HEADER}System Statistics{ENDC}
CPU Usage: {cpu_percent}%
Memory Usage: {mem.percent}%
Network: Sent {network.bytes_sent/1024:.2f}KB, Received {network.bytes_recv/1024:.2f}KB
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            print(stats)
            self.logger.info(f"System stats - CPU: {cpu_percent}%, Memory: {mem.percent}%, Network I/O: {network.bytes_sent/1024:.2f}KB/{network.bytes_recv/1024:.2f}KB")
        except Exception as e:
            self.logger.error(f"Error logging system stats: {str(e)}")