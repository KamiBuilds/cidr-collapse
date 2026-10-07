# CIDR Collapse

`cidr-collapse` turns IPv4/IPv6 addresses and CIDR blocks into the smallest equivalent set of non-overlapping networks. It is useful before reviewing firewall allowlists, route lists, monitoring targets, and infrastructure configuration.

It uses only Python's standard library, makes no network connections, and never changes firewall or routing state.

## Linux quick start

`cidr-collapse` is a command-line tool, so run these commands in your Linux terminal. It does not open a graphical window.

### 1. Install Git and Python

First check whether they are already available:

```bash
git --version
python3 --version
```

Python 3.9 or newer is required. If either command is missing, install both with your distribution's package manager:

```bash
# Ubuntu, Debian, Linux Mint, Pop!_OS
sudo apt update && sudo apt install -y git python3

# Fedora, RHEL 9+, Rocky Linux, AlmaLinux
sudo dnf install -y git python3

# Arch Linux, Manjaro
sudo pacman -S --needed git python

# openSUSE
sudo zypper install git python3

# Alpine Linux
sudo apk add git python3
```

Use only the command for your distribution.

### 2. Clone and enter the repository

```bash
git clone https://github.com/KamiBuilds/cidr-collapse.git
cd cidr-collapse
```

### 3. Verify it works

```bash
python3 cidr_collapse.py 192.0.2.0/25 192.0.2.128/25
```

Expected output:

```text
192.0.2.0/24
```

No Python packages, virtual environment, root access, Docker, or installation script are required after Git and Python are present.

## Other operating systems

- **macOS:** install Git and Python 3, then use the same clone and `python3` commands.
- **Windows PowerShell:** install Git and Python 3, clone with the same Git command, and replace `python3` with `py`.

## Requirements

- Git, for cloning the repository
- Python 3.9 or newer
- No third-party Python packages

## VMware notes

VMware does not change how the tool runs. The guest VM only needs working internet access to clone from GitHub. If cloning fails, check the VM's network adapter:

- **NAT** is usually the simplest option.
- **Bridged** mode also works when the LAN permits it.
- Confirm connectivity with `git ls-remote https://github.com/KamiBuilds/cidr-collapse.git`.

After cloning, `cidr-collapse` runs entirely offline and makes no network connections.

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
