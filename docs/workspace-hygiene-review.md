# Workspace hygiene through the artifact lifecycle

Version 0.6.9. The prior skill already bounded inventory and prevented recursive backups and broad deletion. The revision makes retirement happen as outputs are superseded during work, verifies what Git can actually recover before relying on it, and distinguishes dispensable artifacts from useful caches, unique data and supported legacy consumers. It preserves scoped recovery when genuinely needed; avoiding unnecessary backups must not destroy the only needed version of work.

## Primary-source comparison

Relevant original sources inspected on 2026-11-07. They inform the procedure, not a claim of universal cleanup safety.

| Source | Useful mechanism | Adaptation and limits |
| --- | --- | --- |
| Git, [gitignore](https://git-scm.com/docs/gitignore), [git-clean 2.43.0](https://git-scm.com/docs/git-clean/2.43.0), and [git-restore source](https://github.com/git/git/blob/master/Documentation/git-restore.adoc), blob `7d1942316514c8e0c82d0399bbc1b7fa524cf7ab` | Ignored files are intentionally untracked; cleanup can remove untracked/ignored data; restore uses content from an actual source/index/commit. | Verify the needed version exists before relying on Git. A repository, ignore pattern or tracked filename is not complete recovery. No broad git-clean, reset, auto-commit or stash workflow is introduced. The cited clean documentation is explicitly versioned; its destructive command is not used. |
| npm, [npm-cache](https://docs.npmjs.com/cli/commands/npm-cache) | Its cache is verified/self-healing and clearing it routinely is generally unnecessary, while it is also not a guaranteed permanent data store. | Distinguish useful current/offline caches from demonstrably dispensable artifacts and account for regeneration. Do not generalize npm's guarantees to every cache or erase global dependencies for tidiness. |
| Addy Osmani, [Deprecation and Migration](https://github.com/addyosmani/agent-skills/blob/main/skills/deprecation-and-migration/SKILL.md), relevant consumer/removal sections, blob `8789d4e0eba0f65b35da842430b345d4c76877e9` | Check unique value, consumers and replacement before removing old behavior. | A legacy name is not evidence of disuse; retiring supported functionality is a separate scoped change. No mandatory migration program or replacement infrastructure is added to ordinary scratch cleanup. |
| Superpowers, [Finishing a Development Branch](https://github.com/obra/superpowers/blob/main/skills/finishing-a-development-branch/SKILL.md), workspace-cleanup section, blob `fa8aecaf8813f1b19d19996f7957d1b0121f2d9c` | Cleanup depends on integration status and ownership; uncommitted/untracked work can exist nowhere else and must survive refusal to remove a worktree. | Preserve active/shared work and verify actual provenance. Do not infer ownership from a directory name, force worktree removal, or import mandatory merge menus and branch operations. |

## Resulting behavior

Generated material has a purpose, owner and retirement condition. Verified replacements allow old task-owned intermediates to be retired without waiting for the chat or entire project to finish. Requested variants, source material and active consumers remain protected. A backup needs a real recovery gap; a full-project copy requires a reason the scoped alternative cannot satisfy, bounded contents and a retirement condition outside its own input.

The new conditional reference explains recovery, retention, consumer classification and inventory limits. The existing metadata-only inventory helper is unchanged: it never deletes or classifies disposal safety. Implicit invocation remains enabled, and metadata/the generated selection pointer now emphasize lifecycle and justified recovery. No quota, expiry, schedule, monitor, global cache cleanup or new runtime is installed.

## Verification scope

Eight new scenarios extend the previous eight without changing their values: Git recovery without redundant copies, unique local content outside Git, incremental retirement, supported legacy consumers, useful offline caches, ignore patterns that do not free space, inventory/allocation limits, and a genuine need for a scoped recovery copy.

An independent expected-answer-blind application pass worked in an isolated synthetic Git repository. It removed only two verified superseded task-owned previews, totaling 3,000 logical bytes. It retained requested desktop/mobile outputs, an active preview, supported compatibility material, an ignored unique draft, uncertain recovery and uncommitted source changes. Parent verification confirmed that every surviving file and all Git metadata remained byte-identical to the pre-test hashes; no new files appeared. Its decisions preserved all 16 scenarios.

Local checks passed: 372 tests with 22 platform skips, 29 helper replays, skill-creator validation, repository validation and installer packaging. Packaged Workspace Hygiene files were compared against source before publication.

This tests one local cleanup and scenario decisions. It does not certify future invocation, every filesystem race/link case, deletion safety for unknown user material or actual physical space reclaimed. Logical bytes, partial coverage and skipped link targets remain explicit limits. The synthetic workspace is task-owned test material and can be retired after its verification evidence is recorded; it is not user recovery data.
