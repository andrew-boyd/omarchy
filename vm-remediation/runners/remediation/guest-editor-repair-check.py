#!/usr/bin/python
"""Baseline-only experiment inside a disposable guest; no ISO claim."""
from pathlib import Path
import subprocess, os
assert subprocess.check_output(['hostname'],text=True).strip()=='omarchy-test'
assert subprocess.check_output(['systemd-detect-virt'],text=True).strip()=='kvm'
assert Path('/dev/vda').exists() and os.geteuid()!=0
config=Path.home()/'.config/nvim/lua/plugins/all-themes.lua'
original=config.read_text()
assert original.count('gthelding/monokai-pro.nvim')==1
config.write_text(original.replace('gthelding/monokai-pro.nvim','loctvl842/monokai-pro.nvim'))
plugin=Path.home()/'.local/share/nvim/lazy/monokai-pro.nvim'
assert not plugin.exists()
env=dict(os.environ,GIT_TERMINAL_PROMPT='0')
subprocess.run(['git','clone','--depth','1','https://github.com/loctvl842/monokai-pro.nvim',str(plugin)],env=env,check=True)
head=subprocess.check_output(['git','-C',str(plugin),'rev-parse','HEAD'],text=True).strip()
assert head=='a68e38b8e55d69a215d0f02598900a79c356da9d',head
print('Pinned replacement plugin:',head,flush=True)
check='+lua print("NVIM_STARTUP_ERRMSG=" .. vim.v.errmsg); if vim.v.errmsg ~= "" then vim.cmd("cquit 1") end'
subprocess.run(['timeout','45','nvim','--headless',check,'+qa'],check=True)
subprocess.run(['timeout','45','nvim','--headless','+lua require("monokai-pro").setup()','+colorscheme monokai-pro',check,'+qa'],check=True)
print('PASS: existing editor startup and explicit Monokai load with the replacement source')
print('BOUNDARY: guest-only baseline experiment, not included in Build 7 or any Mac feature branch')
