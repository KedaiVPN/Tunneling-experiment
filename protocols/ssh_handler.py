import asyncio
import socket
import ssl
from utils.colors import *

class SSHHandler:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.servers = []
        self.connections = {
            'openssh': 0,
            'dropbear': 0,
            'ws': 0,
            'udp': 0,
            'ssl_ws': 0
        }

    async def start(self):
        try:
            # Start OpenSSH
            await self._start_openssh()

            # Start Dropbear
            await self._start_dropbear()

            # Start WebSocket
            await self._start_ws()

            # Start UDP
            await self._start_udp()

            # Start SSL WebSocket
            await self._start_ssl_ws()

            print(f"{OKGREEN}SSH services started successfully{ENDC}")
            self.logger.info(f"All SSH services started - Ports: OpenSSH:{self.config.ssh_config['openssh_port']}, " +
                           f"Dropbear:{self.config.ssh_config['dropbear_port']}, WS:{self.config.ssh_config['ws_port']}, " +
                           f"UDP:{self.config.ssh_config['udp_port']}, SSL-WS:{self.config.ssh_config['ssl_ws_port']}")

        except Exception as e:
            print(f"{FAIL}Failed to start SSH services: {str(e)}{ENDC}")
            self.logger.error(f"SSH startup error: {str(e)}")
            raise

    async def _start_openssh(self):
        server = await asyncio.start_server(
            self._handle_openssh,
            '0.0.0.0',
            self.config.ssh_config['openssh_port']
        )
        self.servers.append(server)
        self.logger.info(f"OpenSSH server started on port {self.config.ssh_config['openssh_port']}")

    async def _start_dropbear(self):
        server = await asyncio.start_server(
            self._handle_dropbear,
            '0.0.0.0',
            self.config.ssh_config['dropbear_port']
        )
        self.servers.append(server)
        self.logger.info(f"Dropbear server started on port {self.config.ssh_config['dropbear_port']}")

    async def _start_ws(self):
        server = await asyncio.start_server(
            self._handle_ws,
            '0.0.0.0',
            self.config.ssh_config['ws_port']
        )
        self.servers.append(server)
        self.logger.info(f"SSH WebSocket server started on port {self.config.ssh_config['ws_port']}")

    async def _start_udp(self):
        transport, protocol = await asyncio.get_event_loop().create_datagram_endpoint(
            lambda: self._handle_udp(),
            local_addr=('0.0.0.0', self.config.ssh_config['udp_port'])
        )
        self.servers.append(transport)
        self.logger.info(f"SSH UDP server started on port {self.config.ssh_config['udp_port']}")

    async def _start_ssl_ws(self):
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(
            self.config.tls_config['cert_path'],
            self.config.tls_config['key_path']
        )
        server = await asyncio.start_server(
            self._handle_ssl_ws,
            '0.0.0.0',
            self.config.ssh_config['ssl_ws_port'],
            ssl=ssl_context
        )
        self.servers.append(server)
        self.logger.info(f"SSH SSL WebSocket server started on port {self.config.ssh_config['ssl_ws_port']}")

    async def _handle_openssh(self, reader, writer):
        self.connections['openssh'] += 1
        peer = writer.get_extra_info('peername')
        self.logger.info(f"New OpenSSH connection from {peer}")
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except Exception as e:
            self.logger.error(f"OpenSSH error: {str(e)}")
        finally:
            self.connections['openssh'] -= 1
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"Closed OpenSSH connection from {peer}")

    async def _handle_dropbear(self, reader, writer):
        self.connections['dropbear'] += 1
        peer = writer.get_extra_info('peername')
        self.logger.info(f"New Dropbear connection from {peer}")
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except Exception as e:
            self.logger.error(f"Dropbear error: {str(e)}")
        finally:
            self.connections['dropbear'] -= 1
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"Closed Dropbear connection from {peer}")

    async def _handle_ws(self, reader, writer):
        self.connections['ws'] += 1
        peer = writer.get_extra_info('peername')
        self.logger.info(f"New WebSocket connection from {peer}")
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except Exception as e:
            self.logger.error(f"WebSocket error: {str(e)}")
        finally:
            self.connections['ws'] -= 1
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"Closed WebSocket connection from {peer}")

    def _handle_udp(self):
        class UDPProtocol(asyncio.DatagramProtocol):
            def connection_made(self2, transport):
                self2.transport = transport

            def datagram_received(self2, data, addr):
                self.logger.info(f"UDP data received from {addr}")
                self.connections['udp'] += 1
                # Echo back the data
                self2.transport.sendto(data, addr)
                self.connections['udp'] -= 1
        return UDPProtocol()

    async def _handle_ssl_ws(self, reader, writer):
        self.connections['ssl_ws'] += 1
        peer = writer.get_extra_info('peername')
        self.logger.info(f"New SSL WebSocket connection from {peer}")
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except Exception as e:
            self.logger.error(f"SSL WebSocket error: {str(e)}")
        finally:
            self.connections['ssl_ws'] -= 1
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"Closed SSL WebSocket connection from {peer}")