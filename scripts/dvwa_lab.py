#!/usr/bin/env python3
"""Alternativa parametrizável para DVWA Low em laboratório IPv4 RFC1918.

Reconstituída para esta publicação; não executada nas VMs do participante.
"""

import argparse
import getpass
import ipaddress
import re
import sys
from pathlib import Path

from dvwa_guiado import Inconclusive, WORDLIST, load_candidates, run, validate_cookie

NETWORKS = tuple(ipaddress.ip_network(cidr) for cidr in
                 ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"))


def private_ipv4(value):
    try:
        address = ipaddress.IPv4Address(value)
    except ipaddress.AddressValueError:
        raise argparse.ArgumentTypeError("Informe um IPv4 literal do laboratório.") from None
    if not any(address in network for network in NETWORKS):
        raise argparse.ArgumentTypeError("O alvo precisa estar em uma faixa privada RFC1918.")
    return str(address)


def username(value):
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", value):
        raise argparse.ArgumentTypeError("Nome de usuário inválido para este exercício.")
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description="DVWA Low: uma conta, até dez candidatas.")
    parser.add_argument("--target", required=True, type=private_ipv4, help="IPv4 da VM autorizada")
    parser.add_argument("--username", default="admin", type=username)
    parser.add_argument("--wordlist", type=Path, default=WORDLIST)
    args = parser.parse_args(argv)
    try:
        cookie = validate_cookie(getpass.getpass("Valor de PHPSESSID (oculto): "))
        candidates = load_candidates(args.wordlist, limit=10)
        target = f"http://{args.target}/dvwa/vulnerabilities/brute/"
        return run(target, args.username, candidates, cookie, limit=10)
    except Inconclusive as exc:
        print(f"INCONCLUSIVO: {exc}")
        return 2
    except (EOFError, KeyboardInterrupt):
        print("\nInterrompido.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
