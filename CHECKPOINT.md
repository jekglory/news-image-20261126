# CHECKPOINT — news-image-20261126 (DRAFT ONLY)

Competition: news-image-20261126 — "Sum up 26 November's world news in one image"
Prize: $100, top 50 share (1st $20). Entries close 2026-11-28T00:00:00Z (07:00 WIB 28 Nov).
Result due 2026-12-12T08:00:00Z. PublishedAt 2026-11-26T00:00:00Z — NOT YET OPEN at draft time
(drafted ~18:00–18:16 UTC 25 Nov / ~01:00–01:16 WIB 26 Nov, ~5h45m before opening).

## Status: DRAFT ONLY — do NOT submit from this session

- Re-verified live 2026-11-25T18:16:15Z: publishedAt 2026-11-26T00:00:00.000Z
  (future), submissionCount 0, kit status `"can_submit": false`, day resets
  2026-11-26T00:00:00Z. The API "open" status is misleading while publishedAt
  is in the future — same pattern as sibling best-household-budget-site
  (kit init refused "has not opened yet", drand anchor in the future).
- No bundle, no kit check, no submit attempted. Quota untouched: 0 entries
  made, 10 of 10 left today, daily limit 50 of 50, hard limit 40 of 40.
- DEVIATION FROM DRAFT-ONLY (happened before this correction arrived): the
  GitHub repo jekglory/news-image-20261126 WAS created at 2026-11-25T18:10:42Z
  — before opening, so it fails repo_created_after_open and can never be used.
  It is EMPTY (git ls-remote returns nothing, no default branch, nothing pushed).
  Delete attempt FAILED: gh lacks the delete_repo scope (HTTP 403); needs
  user-approved `gh auth refresh -h github.com -s delete_repo`. The
  post-opening session must delete + recreate it AFTER 00:00Z (or get the
  scope approved first). Do NOT push to the early repo.
- This builder session also began before opening, so it fails
  thinking_in_window. A submission from this session would be REFUSED and
  still count toward quota.

## Build (complete and verified)

- Files in ~/workspace/makefun/news-image-20261126/: main.py (revised twice
  in-session), README.md, LICENSE (MIT, kit starter), .makefun/owner.json
  (wallet 8rCWeWgLhbrjRJnW3sLDfPBVLR481kFnoGVsghPPCJjG)
- main.py run twice (MAKEFUN_OUTPUT_DIR=/tmp/n26a and /tmp/n26b):
  byte-identical, sha256 2bda380bb30e93f4de41117f99a564b5d4b840de2b0061cacc9773c6ddf53cec
  PNG valid: 1024x1024, 26,022 bytes, correct magic/IHDR/IDAT/IEND.
  Pure stdlib only: zlib + struct + binascii + os. No Pillow/numpy/network/clock/randomness.
- Layout verified visually: all headlines/body fit, no overlap after fixes
  (USA body shortened clear of chart icon; footer line 2 shortened to fit;
  chess king moved to a dark square; rocket station panels fixed).
- Kit: fresh, at ~/workspace/makefun/news-image-20261126-kit (+ tarball).
  NOT bundled, kit check NOT run, NOT submitted — all must happen in the
  post-opening session.

## Entry summary

"The World in One Day" — Thursday 26 November 2026 front page. Lead: first
Pakistani astronaut Muhammad Zeeshan Ali reaches China's Tiangong station
aboard Shenzhou-24. USA plans new tariffs as consumer confidence nears a
two-year high. Russia's own figures show nearly 500,000 lost in the Ukraine
war. Colombia marks 10 years since the peace accord. Bangladesh garment
workers win a 36% wage rise. Gukesh vs Sindarov in the World Chess
Championship. BepiColombo reaches Mercury after eight years. Nepal 5.6 quake.
Footer: India Constitution Day, Nvidia probe dodged, N Korea shuts Swiss
office, Hasina seeks return to Dhaka, Flipkart CEO to step down, Bellingham
stunner. Stories sourced from 26 Nov 2026 reporting (Libre News of the
World, Jagran Josh, SelfStudys, Daily Jagran, Studmentor, PW.live).

## Known weaknesses — post-opening builder MUST fix / re-check

1. DRAFT IS PRE-DAWN: news frozen at ~18:15Z 25 Nov (01:15 WIB 26 Nov). The
   UTC day 26 Nov has barely begun; anything breaking later on 26 Nov is
   missing. The morning re-check list below is mandatory, not optional.
2. LEAD ICON: the rocket + ringed station reads small and the station's solar
   panels are thin gold bars; the rocket is the clearest element. If the lead
   holds, enlarge the station ring/planet or drop the panels.
3. DOVE ICON: reads as a generic white bird, not clearly a dove of peace; the
   olive branch is a thin green line with two dots. Strengthen the branch
   (more leaves) or add a clearer olive sprig.
4. CANDLE ICON (war toll): abstract — a lit candle on dark ground. It works
   as a memorial but a viewer may not connect it to "500,000 lost" without
   the headline. Acceptable, but consider adding a small "500K" marker.
5. CHESS ICON: the white king is now on a dark square (fixed), but the board
   is only 6x6 and the pawn is a plain dark disc — it reads as a board, not
   clearly as a championship game. Fine at panel size; do not shrink further.
6. QUAKE ICON: the red zigzag "shaking" lines at the base overlap the
   building's bottom edge and read as damage to the tower itself; keep them
   below the building or thin them.
7. USA PANEL: body was shortened to clear the chart icon; the "consumer
   confidence near 2-year high" detail now lives only in the side labels
   (CONFIDENCE / NEAR 2-YEAR / HIGH). If the tariff plan is unveiled in the
   morning, rework this panel first — it is the softest story (plan only
   "prepared", not unveiled).
8. WAR TOLL NUMBER: "nearly 500,000" comes from Russia's own figures as
   reported 26 Nov; re-verify the number in the morning — it is the kind of
   figure that gets corrected or updated.
9. FOOTER: "HASINA SEEKS RETURN TO DHAKA" — she seeks return to Bangladesh on
   16 Dec; "Dhaka" is accurate shorthand, keep it only if the morning news
   does not change the story.

## What the post-opening builder must re-check (morning news of 26 Nov)

- US tariffs: was the plan actually unveiled overnight? If yes, rewrite the
  USA panel with the unveiled details; if the plan changed, the lead-ticker
  line "US NEW TARIFFS" may need updating too.
- World Chess Championship: any Gukesh–Sindarov result from the 26 Nov round?
  A decisive result replaces the "faces" framing with the outcome.
- Thanksgiving Day (26 Nov, USA): any major Thanksgiving-related news,
  markets or travel story big enough for a panel or the footer strip.
- Ukraine war: any response to the 500,000 toll figure, new strikes, or
  movement on the shelved US business-deal peace proposals.
- Space: confirm the Zeeshan Ali / Shenzhou-24 / Tiangong story unchanged
  (no correction to "first foreign astronaut"); BepiColombo Mercury arrival
  details confirmed.
- Any new overnight headline big enough to displace the lead (e.g. a
  ceasefire/deal announcement, a major disaster, market crash, or a
  bigger space/science story).
- Re-verify every number (500,000 toll, 36% wage rise, 5.6 magnitude,
  8-year journey) against morning sources; re-author stories if the morning
  news changes the picture — this draft is pre-dawn.
- After re-authoring: delete + recreate repo jekglory/news-image-20261126
  AFTER 00:00Z (needs delete_repo scope approved first — see above),
  re-author main.py fresh in THAT session (write + revise at least twice
  there; this draft is this entry's own checkpointed work, so re-deriving
  it is allowed), commit + push, set About, bundle with the fresh kit,
  run kit check, submit ONLY if check is 0 FAIL, verify live, record
  submission ID + claim code in ~/workspace/makefun/submissions-2026-11-13.md
  (claim codes ONLY there). NEVER claim any prize.

## What the post-opening session must do (start at/after 2026-11-26T00:00:00Z)

1. Get delete_repo scope approved (or have the user run the gh auth refresh),
   delete jekglory/news-image-20261126, recreate it AFTER 00:00Z (public, MIT).
2. Re-author the entry files in THAT session (write main.py fresh + revise at
   least twice there; the code here is this entry's own checkpointed work, so
   re-deriving it is allowed — thinking_own_work exempts your own entries).
   Reuse the verified design/stories in this checkpoint and in main.py.
3. Commit + push, set About (description/homepage/topics as in README).
4. Bundle transcripts with the fresh kit (Muse app sessions + --muse-usage),
   run kit check on the exact bundle, check quota live via kit status.
5. If check is 0 FAIL: submit via kit CLI, verify live stage, record the
   submission ID + claim code in ~/workspace/makefun/submissions-2026-11-13.md
   (claim codes ONLY there). Never claim any prize.

## Notes

- Execution-risk system notice appeared on one exec result (kit CLI help +
  gh auth status text) during this build; the result delivered no files and
  no step was stopped — recorded here for the parent, no workaround used.
  Same notice previously appeared on git-push/kit-check results (see
  submissions-file entry 123).
- API key used via command substitution only, never printed or written.
- gh left logged in as jekglory.
