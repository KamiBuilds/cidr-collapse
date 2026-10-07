# CIDR Collapse

`cidr-collapse` turns IPv4/IPv6 addresses and CIDR blocks into the smallest equivalent set of non-overlapping networks. It is useful before reviewing firewall allowlists, route lists, monitoring targets, and infrastructure configuration.

It uses only Python's standard library, makes no network connections, and never changes firewall or routing state.

## Download and install

Clone the repository on Linux, macOS, or Windows:

```bash
git clone https://github.com/KamiBuilds/cidr-collapse.git
cd cidr-collapse
```

No package installation is required. On Linux/macOS, use `python3`; on Windows PowerShell, replace `python3` with `py` in the commands below.

## Requirements

- Python 3.9 or newer
- No third-party packages

## Usage

Pass addresses and networks as arguments:

```bash
python3 cidr_collapse.py \
  192.0.2.0/25 \
  192.0.2.128/25 \
  198.51.100.42
```

Output:

```text
192.0.2.0/24
198.51.100.42/32
```

Host bits are normalized because inputs are parsed with non-strict CIDR semantics. For example, `192.0.2.42/24` becomes `192.0.2.0/24`.

### Read from standard input

With no positional arguments, input is read one item per line from standard input:

```bash
python3 cidr_collapse.py < examples/networks.txt
```

Blank lines and `#` comments are ignored. Inline comments are also supported.

### JSON output

```bash
python3 cidr_collapse.py --json < examples/networks.txt
```

Example:

```json
["10.0.0.0/24", "192.0.2.0/24", "2001:db8::/32"]
```

IPv4 and IPv6 inputs are collapsed independently, then emitted in that order. Duplicate and contained networks disappear automatically. Scoped IPv6 literals such as `fe80::1%eth0` are rejected because merging them would discard interface-specific meaning.

## Errors and exit statuses

Invalid input is reported on standard error with its 1-based item position. Exit status is `0` for valid input and `2` for invalid input or command-line usage.

```bash
python3 cidr_collapse.py 192.0.2.0/24 not-a-network
```

```text
error: item 2 is not a network: 'not-a-network'
```

## Safety

This tool only transforms text. Review the result before applying it to access controls: collapsing networks preserves the exact address set represented by the input, but it cannot determine whether that set is appropriate for your security policy.

## Tests and quality checks

Run the complete test suite:

```bash
python3 -m unittest discover -s tests -v
```

Run syntax compilation:

```bash
python3 -m compileall -q cidr_collapse.py tests
```

Exercise the documented example:

```bash
python3 cidr_collapse.py < examples/networks.txt
python3 cidr_collapse.py --json < examples/networks.txt
```

Check whitespace before committing:

```bash
git diff --check
```

## License

MIT — see [LICENSE](LICENSE).
