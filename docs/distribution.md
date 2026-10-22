# Reproducible installer downloads

The current 0.4.0 tree is a candidate, not a published release or certified live
Codex integration. Building does not upload, tag, publish, or install anything.

```sh
python scripts/package_installers.py
```

`work/downloads/` receives the full suite and seven independent ZIPs,
`SHA256SUMS`, and `distribution.json`. The JSON records the source manifest's
version, selected skills, file count, archive size, license presence, and SHA-256
for each ZIP. It deliberately excludes local paths and build timestamps.
Every installer ZIP contains its own README with recovery instructions; no
companion skill or online document is needed to uninstall or recover.

ZIP entries use sorted paths, a fixed timestamp, normalized Unix file metadata,
and explicit compression settings. Identical source bytes produce identical
archives with the same Python/compression toolchain. This is not a promise of
identical DEFLATE output across different library versions. Source bytes matter:
use the repository's LF checkout settings, not a manual newline conversion.
The optional plugin ZIP uses the same deterministic archive writer.

Each ZIP is verified before replacing its prior output. A multi-archive batch is
not transactional: a failed build can leave old and new ZIPs together. Existing
checksum and manifest files are invalidated before rebuilding, and new ones are
written only after all eight archives succeed. A failed metadata write removes
both files. Treat a failed command or missing metadata as an incomplete build;
rerun successfully before distributing. Use a fresh output directory for a
release candidate and distribute only the eight listed ZIPs plus both metadata
files, not unrelated or leftover files in that directory. Do not run concurrent
builds into the same output directory.

## Verify a download

From the directory containing all eight ZIPs and the checksum file, on systems
with the utility available:

```sh
sha256sum -c SHA256SUMS
```

For one ZIP on Windows PowerShell:

```powershell
Get-FileHash .\source-selection.zip -Algorithm SHA256
```

Compare the result with the matching filename in `SHA256SUMS`. Checksums detect
byte changes; they do not authenticate a publisher if an attacker can replace
both the ZIP and checksum. Obtain both from a trusted distribution channel.

## Minimal publication preparation

1. Run the required repository tests and validator on the exact source revision.
   Preserve Windows and Linux results separately from any live-host evidence.
2. Build in a fresh directory. Rebuild using the same toolchain and compare
   checksums. Inspect the full suite and all individual archives.
3. Review the manifest version and candidate/release wording. Packaging checks
   alone cannot certify native skill discovery, hook trust, invocation, adherence,
   or measured usage improvements.
4. Preserve the canonical MIT `LICENSE`. Each standalone skill folder carries
   the same notice; installer and plugin archives include it. Do not remove notices
   when adapting or redistributing the package. Research references are not
   relicensed by this project's license.
5. The validation workflow builds and uploads these exact ten files after tests
   and validation succeed. Artifact names include OS, source SHA, and run attempt;
   repository permissions remain `contents: read`. Pull requests and pushes to
   `main` run the checks; a feature-branch push does not duplicate its PR run.
   Use the manual workflow trigger for a branch build before opening a PR. Artifacts expire after 14 days
   and require a signed-in GitHub user to download. They are candidate build
   outputs, not public versioned releases. The
   [official upload action documentation](https://github.com/actions/upload-artifact/blob/v7.0.2/README.md)
   describes file lists, expiry, and missing-file behavior.
6. With separate approval, publish versioned assets and checksums from the
   reviewed revision. Update download links only after verifying the real assets
   exist. Do not advertise local build paths as released downloads.

The source ZIP linked by the main README follows `main`; it is not an immutable
versioned release. Do not silently replace that distinction with a guessed link.
