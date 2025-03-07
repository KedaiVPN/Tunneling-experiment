import asyncio
import json
import ssl
from utils.colors import *

class V2RayHandler:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.servers = []
        self.connections = {
            'vmess_ws_tls': 0,
            'vmess_ws': 0,
            'vless_ws_tls': 0,
            'vless_ws': 0
        }

    async def start(self):
        try:
            # Start VMESS WS TLS
            await self._start_vmess_ws_tls()

            # Start VMESS WS non-TLS
            await self._start_vmess_ws()

            # Start VLESS WS TLS
            await self._start_vless_ws_tls()

            # Start VLESS WS non-TLS
            await self._start_vless_ws()

            print(f"{OKGREEN}V2Ray services started successfully{ENDC}")
            self.logger.info(f"All V2Ray services started - Ports: VMESS-WS-TLS:{self.config.v2ray_config['vmess_ws_tls_port']}, " +
                           f"VMESS-WS:{self.config.v2ray_config['vmess_ws_port']}, " +
                           f"VLESS-WS-TLS:{self.config.v2ray_config['vless_ws_tls_port']}, " +
                           f"VLESS-WS:{self.config.v2ray_config['vless_ws_port']}")

        except Exception as e:
            print(f"{FAIL}Failed to start V2Ray services: {str(e)}{ENDC}")
            self.logger.error(f"V2Ray startup error: {str(e)}")
            raise

    async def _start_vmess_ws_tls(self):
        try:
            server = await asyncio.start_server(
                self._handle_vmess_ws_tls,
                '0.0.0.0',
                self.config.v2ray_config['vmess_ws_tls_port'],
                ssl=self._create_ssl_context()
            )
            self.servers.append(server)
            self.logger.info(f"VMESS WS TLS started on port {self.config.v2ray_config['vmess_ws_tls_port']}")
        except Exception as e:
            self.logger.error(f"Failed to start VMESS WS TLS: {str(e)}")
            raise

    async def _start_vmess_ws(self):
        try:
            server = await asyncio.start_server(
                self._handle_vmess_ws,
                '0.0.0.0',
                self.config.v2ray_config['vmess_ws_port']
            )
            self.servers.append(server)
            self.logger.info(f"VMESS WS started on port {self.config.v2ray_config['vmess_ws_port']}")
        except Exception as e:
            self.logger.error(f"Failed to start VMESS WS: {str(e)}")
            raise

    async def _start_vless_ws_tls(self):
        try:
            server = await asyncio.start_server(
                self._handle_vless_ws_tls,
                '0.0.0.0',
                self.config.v2ray_config['vless_ws_tls_port'],
                ssl=self._create_ssl_context()
            )
            self.servers.append(server)
            self.logger.info(f"VLESS WS TLS started on port {self.config.v2ray_config['vless_ws_tls_port']}")
        except Exception as e:
            self.logger.error(f"Failed to start VLESS WS TLS: {str(e)}")
            raise

    async def _start_vless_ws(self):
        try:
            server = await asyncio.start_server(
                self._handle_vless_ws,
                '0.0.0.0',
                self.config.v2ray_config['vless_ws_port']
            )
            self.servers.append(server)
            self.logger.info(f"VLESS WS started on port {self.config.v2ray_config['vless_ws_port']}")
        except Exception as e:
            self.logger.error(f"Failed to start VLESS WS: {str(e)}")
            raise

    def _create_ssl_context(self):
        try:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(
                self.config.tls_config['cert_path'],
                self.config.tls_config['key_path']
            )
            return ssl_context
        except Exception as e:
            self.logger.error(f"Failed to create SSL context: {str(e)}")
            raise

    async def _handle_vmess_ws_tls(self, reader, writer):
        self.connections['vmess_ws_tls'] += 1
        peer = writer.get_extra_info('peername')
        self.logger.info(f"New VMESS WS TLS connection from {peer}")
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except Exception as e:
            self.logger.error(f"VMESS WS TLS error: {str(e)}")
        finally:
            self.connections['vmess_ws_tls'] -= 1
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"Closed VMESS WS TLS connection from {peer}")

    async def _handle_vmess_ws(self, reader, writer):
        self.connections['vmess_ws'] += 1
        peer = writer.get_extra_info('peername')
        self.logger.info(f"New VMESS WS connection from {peer}")
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except Exception as e:
            self.logger.error(f"VMESS WS error: {str(e)}")
        finally:
            self.connections['vmess_ws'] -= 1
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"Closed VMESS WS connection from {peer}")

    async def _handle_vless_ws_tls(self, reader, writer):
        self.connections['vless_ws_tls'] += 1
        peer = writer.get_extra_info('peername')
        self.logger.info(f"New VLESS WS TLS connection from {peer}")
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except Exception as e:
            self.logger.error(f"VLESS WS TLS error: {str(e)}")
        finally:
            self.connections['vless_ws_tls'] -= 1
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"Closed VLESS WS TLS connection from {peer}")

    async def _handle_vless_ws(self, reader, writer):
        self.connections['vless_ws'] += 1
        peer = writer.get_extra_info('peername')
        self.logger.info(f"New VLESS WS connection from {peer}")
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except Exception as e:
            self.logger.error(f"VLESS WS error: {str(e)}")
        finally:
            self.connections['vless_ws'] -= 1
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"Closed VLESS WS connection from {peer}")