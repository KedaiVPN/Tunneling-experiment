{pkgs}: {
  deps = [
    pkgs.haproxy
    pkgs.netcat
    pkgs.rustc
    pkgs.libxcrypt
    pkgs.libiconv
    pkgs.cargo
    pkgs.zlib
    pkgs.pkg-config
    pkgs.openssl
    pkgs.grpc
    pkgs.c-ares
  ];
}
