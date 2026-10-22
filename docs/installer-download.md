# PM Essential Skills installer download

Extract the entire archive before running anything. `START-HERE.txt` lists the
included skills. Only those skills are installed; companions are not required.
Source and current documentation: https://github.com/ibbuilds/pm-essential-skills

## Install and check

Windows: open `Install.cmd`. The launcher looks for Python 3.10+, including a
usable Codex-bundled runtime. Other systems, from the extracted folder:

```sh
python3 scripts/install_suite.py install
python3 scripts/install_suite.py status
```

On Windows, use `Install.cmd status`. `CODEX_HOME` chooses the Codex profile.
For named configuration profiles, Python status also accepts `--profile NAME` and
reads `NAME.config.toml` after the base config. It reports configured disabled skills
without changing settings; session overrides and actual activation remain unknown.
TOML diagnostics need Python 3.11+; installation still supports Python 3.10.
Advanced Python commands also accept `--codex-home PATH`; use the same home
for status, recovery, and uninstall. The Windows launcher takes only one action,
not Python options. Existing user preferences and originals are preserved.

Continue normally when Codex next loads its instructions. An existing session
can retain older instructions. Installation checks files and instruction placement,
not native discovery, live invocation, hook trust, model adherence, or savings.
No certified host-version compatibility matrix is supplied by this download.

Optional hooks: `python3 scripts/install_suite.py install --hooks` registers
reminders only. The host must support the hook events and separately review and
trust them. Registration does not prove execution. No server, Git account, plugin,
project activation prompt, telemetry, or background agent is required.

## Remove or recover

Windows: `Install.cmd uninstall`. Other systems:

```sh
python3 scripts/install_suite.py uninstall
```

This restores originals and removes managed guidance while preserving user text
outside it. Customized installed files are not overwritten. Keep this extracted
installer available while using the installation.

After an interrupted operation, preserve the receipt and transaction journal.
Run `Install.cmd recover` or `python3 scripts/install_suite.py recover` with the
same profile, then retry the intended operation. Recovery refuses to overwrite
later edits; reconcile those manually rather than deleting customizations or
blindly reinstalling. Do not edit managed files during installation or recovery.

If a force-killed process left `pm-essential-skills/install.lock` under the selected
Codex profile, first confirm no installer is running for that profile. Only then
remove that stale lock before recovery. Do not delete the receipt or journal.
Recovery covers process interruption, not guaranteed power-loss atomicity.
Windows ACLs, ownership, and extended attributes are not backed up; POSIX mode
bits are preserved where supported.

## Integrity and licensing

If supplied alongside this archive, `SHA256SUMS` and `distribution.json` describe
its bytes and contents. A matching checksum detects changed downloads; it is not
a publisher signature, release approval, or proof of safe/live host behavior.
Use checksums obtained through a trusted channel.

This project is MIT licensed. Retain the supplied copyright and permission notice
when copying, modifying, or redistributing it. The license disclaims warranties;
it is not a guarantee of compatibility or measured savings. Each independent skill
folder retains its own copy so copying one folder does not drop the notice.
