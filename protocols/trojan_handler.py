import asyncio
import ssl
import grpc
import grpc.aio
from utils.colors import *
from protocols import trojan_pb2, trojan_pb2_grpc

class TrojanServiceImplementation(trojan_pb2_grpc.TrojanServiceServicer):
    def __init__(self, logger):
        self.logger = logger

    async def Echo(self, request, context):
        self.logger.info(f"Received Echo request: {request.message}")
        return trojan_pb2.EchoResponse(message=request.message)

    async def StreamData(self, request_iterator, context):
        try:
            async for request in request_iterator:
                self.logger.info(f"Received StreamData request, size: {len(request.data)} bytes")
                yield trojan_pb2.DataResponse(data=request.data)
        except Exception as e:
            self.logger.error(f"StreamData error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))

class TrojanHandler:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.servers = []
        self.connections = {
            'ws_tls': 0,
            'ws': 0,
            'grpc': 0
        }

    async def start(self):
        try:
            # Start Trojan WS TLS
            await self._start_ws_tls()

            # Start Trojan WS non-TLS
            await self._start_ws()

            try:
                # Start Trojan gRPC
                await self._start_grpc()
            except Exception as grpc_error:
                self.logger.error(f"Failed to start gRPC service: {str(grpc_error)}")
                # Continue even if gRPC fails
                print(f"{WARNING}gRPC service failed to start, continuing with other services{ENDC}")

            print(f"{OKGREEN}Trojan services started successfully{ENDC}")
            self.logger.info(f"All Trojan services started - Ports: WS-TLS:{self.config.trojan_config['ws_tls_port']}, " +
                           f"WS:{self.config.trojan_config['ws_port']}, " +
                           f"gRPC:{self.config.trojan_config['grpc_port']}")

        except Exception as e:
            print(f"{FAIL}Failed to start Trojan services: {str(e)}{ENDC}")
            self.logger.error(f"Trojan startup error: {str(e)}")
            raise

    async def _start_ws_tls(self):
        try:
            server = await asyncio.start_server(
                self._handle_ws_tls,
                '0.0.0.0', 
                self.config.trojan_config['ws_tls_port'],
                ssl=self._create_ssl_context()
            )
            self.servers.append(server)
            self.logger.info(f"Trojan WS TLS started on port {self.config.trojan_config['ws_tls_port']}")
        except Exception as e:
            self.logger.error(f"Failed to start Trojan WS TLS: {str(e)}")
            raise

    async def _start_ws(self):
        try:
            server = await asyncio.start_server(
                self._handle_ws,
                '0.0.0.0',
                self.config.trojan_config['ws_port']
            )
            self.servers.append(server)
            self.logger.info(f"Trojan WS started on port {self.config.trojan_config['ws_port']}")
        except Exception as e:
            self.logger.error(f"Failed to start Trojan WS: {str(e)}")
            raise

    async def _start_grpc(self):
        try:
            server = grpc.aio.server()
            trojan_service = TrojanServiceImplementation(self.logger)
            trojan_pb2_grpc.add_TrojanServiceServicer_to_server(trojan_service, server)
            listen_addr = f'0.0.0.0:{self.config.trojan_config["grpc_port"]}'
            server.add_insecure_port(listen_addr)
            await server.start()
            self.servers.append(server)
            self.logger.info(f"Trojan gRPC started on port {self.config.trojan_config['grpc_port']}")
        except Exception as e:
            self.logger.error(f"Failed to start Trojan gRPC: {str(e)}")
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

    async def _handle_ws_tls(self, reader, writer):
        self.connections['ws_tls'] += 1
        peer = writer.get_extra_info('peername')
        self.logger.info(f"New Trojan WS TLS connection from {peer}")
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except Exception as e:
            self.logger.error(f"Trojan WS TLS error: {str(e)}")
        finally:
            self.connections['ws_tls'] -= 1
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"Closed Trojan WS TLS connection from {peer}")

    async def _handle_ws(self, reader, writer):
        self.connections['ws'] += 1
        peer = writer.get_extra_info('peername')
        self.logger.info(f"New Trojan WS connection from {peer}")
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except Exception as e:
            self.logger.error(f"Trojan WS error: {str(e)}")
        finally:
            self.connections['ws'] -= 1
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"Closed Trojan WS connection from {peer}")