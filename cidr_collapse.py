#!/usr/bin/env python3
"""Collapse IP addresses and CIDR networks into a minimal set."""

from __future__ import annotations

import argparse
import ipaddress
import json
import sys


class InputError(ValueError):
    """Raised when an input item is not a valid IP address or network."""


def collapse_networks(items: list[str]) -> list[str]:
    """Return canonical, collapsed networks for the supplied inputs."""
    networks = []
    for position, item in enumerate(items, start=1):
        value = item.split("#", 1)[0].strip()
        if not value:
            continue
        if "%" in value:
            raise InputError(f"item {position} uses unsupported IPv6 scope identifiers: {value!r}")
        try:
            networks.append(ipaddress.ip_network(value, strict=False))
        except ValueError as exc:
            raise InputError(f"item {position} is not a network: {value!r}") from exc
    collapsed = []
    for version in (4, 6):
        family = [network for network in networks if network.version == version]
        collapsed.extend(ipaddress.collapse_addresses(family))
    return [str(network) for network in collapsed]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Collapse IPv4 and IPv6 addresses and CIDRs into a minimal set."
    )
    parser.add_argument("networks", nargs="*", help="IP address or CIDR")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    items = args.networks if args.networks else sys.stdin.readlines()
    try:
        result = collapse_networks(items)
    except InputError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(result))
    else:
        for network in result:
            print(network)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
