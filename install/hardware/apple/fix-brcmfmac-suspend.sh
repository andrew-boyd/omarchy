# Apple Macs with Broadcom Wi-Fi driven by brcmfmac lose Wi-Fi after a long
# suspend: the firmware stops answering commands on wake and the interface
# never recovers without a reboot. A system-sleep hook that rebinds the device
# across sleep reloads the firmware cleanly.
#
# The hardware gate mirrors fix-brcmfmac-supplicant.sh: T2 Macs are detected by
# the T2 PCI ID, older Macs by the brcmfmac PCI IDs from brcm_hw_ids.h. Only
# machines whose Wi-Fi brcmfmac actually drives get the hook.
sys_vendor="$(cat /sys/class/dmi/id/sys_vendor 2>/dev/null || true)"

if lspci -nn | grep "106b:180[12]" >/dev/null ||
  { [[ $sys_vendor == Apple* ]] &&
    lspci -nn | grep -E "14e4:(43ba|43bb|43bc|43a3|43dc|4464|4488|4425|4433)" >/dev/null; }; then
  echo "Detected a Mac with Broadcom Wi-Fi; rebinding brcmfmac across suspend"

  hook=/usr/lib/systemd/system-sleep/rebind-brcmfmac
  if [[ -f $hook && ! -L $hook ]] && cmp -s "$OMARCHY_PATH/default/systemd/system-sleep/rebind-brcmfmac" "$hook"; then
    return 0
  fi
  # Replace only the previously shipped hook, never administrator changes.
  if [[ -e $hook || -L $hook ]]; then
    if [[ -L $hook || ! -f $hook ]] ||
      [[ $(sha256sum "$hook" | cut -d ' ' -f1) != 0e16be9962c708bfe9fe20829fbd54af4d792388f2baeaa868e16351e12148a1 ]]; then
      echo "Preserving customized Broadcom sleep hook: $hook. Reconcile it with $OMARCHY_PATH/default/systemd/system-sleep/rebind-brcmfmac, then retry." >&2
      return 1
    fi
  fi
  sudo install -Dm 0755 -o root -g root \
    "$OMARCHY_PATH/default/systemd/system-sleep/rebind-brcmfmac" \
    "$hook"
fi
