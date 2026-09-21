#!/usr/bin/env python3
"""Exercise installed guest lock/password paths through QMP hardware input."""
import argparse
import json
from pathlib import Path
import socket
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument("base_dir", type=Path)
p.add_argument("artifacts", type=Path)
p.add_argument("--port", default=2222, type=int)
args = p.parse_args()
base = args.base_dir.resolve()
artifacts = args.artifacts.resolve()
artifacts.mkdir(parents=True, exist_ok=True)
ssh = ["ssh", "-i", str(base / "id_ed25519"), "-p", str(args.port),
       "-o", "BatchMode=yes", "-o", "IdentitiesOnly=yes",
       "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
       "-o", "LogLevel=ERROR", "omarchy@127.0.0.1"]
subprocess.run(ssh + ['test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'], check=True)
qmp_path = None
for pidfile in sorted(base.glob("runs/**/qemu.pid"), reverse=True):
    try:
        cmdline = Path(f"/proc/{int(pidfile.read_text())}/cmdline").read_bytes().decode().split("\0")
        assert str(base) in " ".join(cmdline) and "qemu-system-x86_64" in cmdline[0]
        qmp_path = cmdline[cmdline.index("-qmp") + 1].removeprefix("unix:").split(",")[0]
        break
    except (OSError, ValueError, AssertionError):
        continue
assert qmp_path, "No live QEMU under the supplied base directory"

def qmp(command, arguments=None):
    with socket.socket(socket.AF_UNIX) as s:
        s.settimeout(10)
        s.connect(qmp_path)
        stream = s.makefile("rwb", buffering=0)
        json.loads(stream.readline())
        for request in [{"execute": "qmp_capabilities"}, {"execute": command, "arguments": arguments or {}}]:
            stream.write(json.dumps(request).encode() + b"\n")
            while True:
                response = json.loads(stream.readline())
                if "error" in response:
                    raise RuntimeError(response)
                if "return" in response:
                    break
        return response

def key(*codes):
    qmp("send-key", {"keys": [{"type": "qcode", "data": c} for c in codes], "hold-time": 80})
    time.sleep(0.12)

def password(value):
    key("ctrl", "a")
    key("backspace")
    for letter in value:
        key(letter)
    key("ret")

env = '''export XDG_RUNTIME_DIR=/run/user/$(id -u)
export DBUS_SESSION_BUS_ADDRESS=unix:path=$XDG_RUNTIME_DIR/bus
export HYPRLAND_INSTANCE_SIGNATURE=$(ls -t "$XDG_RUNTIME_DIR/hypr" | head -n1)
export OMARCHY_PATH=/usr/share/omarchy
'''

def guest(command):
    return subprocess.run(ssh + ["bash -s"], input=env + command, text=True, capture_output=True)

def locked():
    r = guest("omarchy-hyprland-session-locked")
    assert r.returncode in (0, 1), r.stderr
    return r.returncode == 0

def wait_lock(want):
    deadline = time.monotonic() + 20
    while locked() != want:
        assert time.monotonic() < deadline, f"Lock state did not become {want}"
        time.sleep(1)

def screenshot(name):
    ppm = artifacts / (name + ".ppm")
    qmp("screendump", {"filename": str(ppm)})
    subprocess.run(["magick", str(ppm), str(artifacts / (name + ".png"))], check=True)
    ppm.unlink()

if locked():
    password("omarchy")
    wait_lock(False)
    print("PASS: password unlocks the session left locked by the full suite.", flush=True)
guest("omarchy-system-lock").check_returncode()
wait_lock(True)
time.sleep(1)
screenshot("locked")
password("wrong")
time.sleep(4)
assert locked(), "Wrong password unexpectedly unlocked the guest"
screenshot("wrong-password-rejected")
password("omarchy")
wait_lock(False)
time.sleep(1)
screenshot("correct-password-unlocked")
print("PASS: installed lock rejects an incorrect password and unlocks with the valid guest password.", flush=True)
(artifacts / "result.json").write_text(json.dumps({"locked": True, "wrong_password_rejected": True, "valid_password_unlocked": True, "input": "QMP virtual hardware keyboard", "physical_fingerprint": "not tested"}, indent=2) + "\n")
