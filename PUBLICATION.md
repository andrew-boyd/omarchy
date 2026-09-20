# Publication handoff — local preparation only

Nothing in this packet authorizes remote publication. No push or PR creation has been performed.

The existing coordinating forks are `andrew-boyd/omarchy` and `andrew-boyd/omarchy-pkgs`. The 17 proposed draft bodies and their exact commits, bases and hashes are in `manifest.json`. The extra `intel-mac/review-index` branch carries this evidence/index only; it is not an eighteenth PR and is not part of any feature diff.

When publication is separately authorized:

1. Refresh source heads/states and upstream targets. Compare them with the packet. Reconcile any changes that affect a candidate; rerun relevant checks on changed trees. The current failures and missing hardware evidence remain disclosed.
2. Inspect existing fork branches and matching open PRs first. Reuse an already-published exact candidate; do not overwrite someone else's branch or create duplicates. Use ordinary pushes without force only after resolving any collision.
3. Push the prepared index/evidence branch, then the three package branches and fourteen feature branches to their respective coordinating forks. Verify the public index, body, patch, source and evidence links resolve. The private preview is not public evidence. These links intentionally do not resolve until the branch is pushed.
4. Create drafts using the exact repository, target base, `andrew-boyd:<feature-branch>` head, title and UTF-8 body file from `manifest.json`. `draft` is true for all 17. Do not add closing keywords or alter originals. Suggested labels are informational and require applicable rights.
5. Record each returned PR URL and add the corresponding link to the series index and paired bodies. Branch/index links already identify the right targets; never guess PR numbers. Re-read published bodies to verify all source rows and companion relationships survived.
6. Leave drafts open for review, hardware-owner contributions and maintainer-controlled CI. Preserve original failures, exclusions and author credit when updating a candidate. A future combined release branch is a separate integration task.

Portable local Git bundles are provided alongside the packet. Clone each full bundle, inspect its named branches, and verify the candidate tree/parent against the manifest. Keep full-suite failures, missing visual evidence and unavailable CI visible; local draft readiness is not permission to merge or install.
