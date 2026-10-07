import json
import subprocess
import sys
import unittest
from pathlib import Path

import cidr_collapse as cc


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cidr_collapse.py"


class CollapseTests(unittest.TestCase):
    def test_collapses_adjacent_and_contained_ipv4_networks(self):
        result = cc.collapse_networks(
            ["192.0.2.0/25", "192.0.2.128/25", "192.0.2.42", "198.51.100.0/24"]
        )

        self.assertEqual(result, ["192.0.2.0/24", "198.51.100.0/24"])

    def test_collapses_ipv4_and_ipv6_families_independently(self):
        result = cc.collapse_networks(
            ["2001:db8::/33", "10.0.0.0/25", "2001:db8:8000::/33", "10.0.0.128/25"]
        )

        self.assertEqual(result, ["10.0.0.0/24", "2001:db8::/32"])


    def test_ignores_blank_lines_and_comments(self):
        result = cc.collapse_networks(["", "  # office ranges", "203.0.113.7/32  # gateway"])

        self.assertEqual(result, ["203.0.113.7/32"])


    def test_invalid_network_reports_its_input_position(self):
        with self.assertRaisesRegex(cc.InputError, r"item 2.*not-a-network"):
            cc.collapse_networks(["192.0.2.0/24", "not-a-network"])


    def test_rejects_scoped_ipv6_addresses(self):
        with self.assertRaisesRegex(cc.InputError, "scope identifiers"):
            cc.collapse_networks(["fe80::1%eth0"])


class CliTests(unittest.TestCase):
    def test_cli_outputs_one_network_per_line(self):
        result = subprocess.run(
            [
                sys.executable,
                str(CLI),
                "192.0.2.0/25",
                "192.0.2.128/25",
                "2001:db8::1",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "192.0.2.0/24\n2001:db8::1/128\n")

    def test_cli_reads_stdin_and_can_emit_json(self):
        result = subprocess.run(
            [sys.executable, str(CLI), "--json"],
            input="10.0.0.0/25\n10.0.0.128/25\n",
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), ["10.0.0.0/24"])


if __name__ == "__main__":
    unittest.main()
