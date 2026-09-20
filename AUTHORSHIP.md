# Commit authorship

Each candidate retains a contributing source identity as its Git Author. Other included commit authors receive native `Co-authored-by` trailers; existing source-declared co-author trailers are retained. Andrew Boyd remains the consolidating committer. This does not imply source-author approval or sign-off.

| Candidate | Git Author | Other included commit authors |
| --- | --- | --- |
| P01 | Roman Elizarov | adityagarud |
| P02 | Oliver Oxenham | None |
| P03 | Taksh | None |
| P04 | adityagarud | None |
| P05 | Piotr Synowiec | Vincent Ritter |
| P06 | Josh Hudson | omarchybot |
| P07 | jeissonneira | None |
| P08 | Bradley Marks | rand0mdud3 |
| P08-packages | xiota | Harrison, Hugo Osvaldo Barrera |
| P09 | Nicolas Nistal | None |
| P10 | Justin Schroeder | Shawn Yeager, Omabot, Matteo Murgida |
| P11 | Shawn Yeager | J7, S-M Robinson, David Heinemeier Hansson, Jake Pillai, inspiretelapps |
| P11-packages | Shawn Yeager | J7, Jake Pillai |
| P12 | Nicolas Nistal | Toni Bergholm |
| P12-packages | Andrew Boyd | None |
| P13 | Nipun H Sud | None |
| P14 | ganjeez | None |

PR openers are not automatically the authors of every commit. The selected audio history includes earlier Shawn Yeager work, S-M Robinson and David Heinemeier Hansson contributions, and Jake Pillai/Hope follow-ups. Merge-only identities and the excluded s2idle commit are omitted. Historical name aliases remain in the evidence. P08 package credit follows retained AUR recipe lines, with contributor notices unchanged. P12 package credit is verified against released recipe files and their Git history.

The [complete mapping](commit-authorship.json) records original commits, identities, inherited trailers, exclusions, old/new hashes and preserved contribution diffs. These are newly assembled commits: original source commit IDs/signatures are not transplanted. Original PR histories remain untouched.

GitHub profile/contribution attribution depends on email association and the eventual merge strategy. Original emails remain even when GitHub did not associate them with an account (including Piotr Synowiec, S-M Robinson and ganjeez; AUR-to-GitHub association was not verified); no noreply address is guessed. Preserve author/co-author metadata during later squash/rebase. See [GitHub co-author documentation](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors).

The initial authorship correction changed metadata only. The later [upstream refresh](UPSTREAM-REFRESH.md) preserves the exact contribution diffs and attribution while advancing their parent bases. Whole trees therefore include new upstream changes. New check receipts identify the actual rebased commits tested; old tested and pre-rebase commits remain as audit refs in the portable Git bundles.
