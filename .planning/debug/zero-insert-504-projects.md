---
status: investigating
trigger: "0 insert despite 504 projects extracted into projects_may table"
created: 2026-05-03T00:00:00Z
updated: 2026-05-03T00:00:00Z
---

## Current Focus
hypothesis: "Workers W0/W1 are dying silently after logging only [1/504] due to unhandled exception in crawl_project() that propagates through asyncio.gather and kills the parent process."
test: "Check if crawl_project() can throw an unhandled exception that crashes the entire asyncio event loop. Trace through crawl4ai error handling in project_extractor.py."
expecting: "If crawl4ai throws an unhandled exception inside arun(): it could crash the asyncio task. This would explain: no error log, no [2/504], no upserting, abrupt end."
next_action: "Look at project_extractor.py crawl_project() exception handling. Does crawler.arun() ever raise instead of returning a failed result object?"

## Symptoms
expected: Each batch of 35 projects extracted should be immediately upserted to projects_may via ingest_projects()
actual: projects_may is empty (0 rows) after 504 projects supposedly scraped. No "upserting" lines in log after browser crash
errors: "Browser.new_context: Target page, context or browser has been closed" - browser crashes on prachuap-khiri-khan endpoint
reproduction: "cd /home/phil/palanthai/phase1-project-directory && PHASE5_TEST_MODE=5 /home/phil/venv/bin/python3 sync_full_run.py --force-all"
started: "After browser crash at prachuap-khiri-khan scan, workers W0/W1 restarted but no ingest_projects() ever called"

## Eliminated
- hypothesis: "Browser crash at prachuap-khiri-khan causes ingest_projects() to not be called"
  evidence: "The prachuap-khiri-khan crash happens in _scan_endpoint() which is a SEPARATE browser from the worker browsers. The 504 count is derived AFTER the scan completes, so scan must have completed (or at least returned a non-zero new_cards). W0/W1 do start and log [1/504] which proves scan completed successfully before the crash."
  timestamp: 2026-05-03

- hypothesis: "Checkpoint file from previous run (49 records) is being mistaken for current run's output"
  evidence: "The checkpoint file /tmp/sync_projects_20260502_192033.jsonl (49 records) is from 19:29. The current run's checkpoint would be /tmp/sync_projects_20260502_193244.jsonl (19:32) which does NOT exist. The 504 enumerated projects came from the scan phase, not from checkpoint."
  timestamp: 2026-05-03

- hypothesis: "Previous run (18:42) with PHASE5_TEST_MODE=3 upserted to wrong table (fullrun_projects_live)"
  evidence: "The 18:42 run with MODE=3 got 'relation fullrun_projects_live does not exist' error. This is a SEPARATE issue from the current run. Current run with MODE=5 correctly routes to projects_may. The issue is NOT wrong table routing."
  timestamp: 2026-05-03

## Evidence
- timestamp: 2026-05-03
  checked: "/tmp/sync_may.log grep for 'upsert\|ingest'"
  found: "ZERO matches for 'upserting', 'ingest', 'Supabase upsert'. Only 4 W0/W1 lines total exist."
  implication: "ingest_projects() was NEVER called, or its log lines were never flushed"

- timestamp: 2026-05-03
  checked: "/tmp/sync_may.log W0/W1 lines"
  found: "Only 4 W0/W1 lines: 'browser batch 1' (2 lines), '[1/504]' for W1 (line 533), '[1/504]' for W0 (line 535). No [2/504], no upserting, no ingest result."
  implication: "Workers started, logged their first URL, then process died before completing batch 1"

- timestamp: 2026-05-03
  checked: "/tmp/sync_projects_20260502_192033.jsonl checkpoint file"
  found: "3.9MB, 49 records. This is from a PREVIOUS run (May 2 19:29). Current run's checkpoint (/tmp/sync_projects_20260502_193244.jsonl) does NOT exist."
  implication: "Current run's checkpoint never created. Process died before first checkpoint write."

- timestamp: 2026-05-03
  checked: "Browser crash at prachuap-khiri-khan location in log"
  found: "Crash happens during _scan_endpoint() for chon-buri (line 311) NOT prachuap-khiri-khan. Multiple pages (phuket page 3, surat-thani, chiang-mai, chon-buri) all fail with 'Browser.new_context: Target page, context or browser has been closed' in rapid succession."
  implication: "A different browser (scanner browser, not worker browsers) is crashing. Scan completes with 504 URLs before these crashes."

- timestamp: 2026-05-03
  checked: "Log file ends abruptly"
  found: "27KB, 408 newlines. Last line: '[W0] [1/504] https://...'. No ERROR traceback, no 'Extraction complete', no graceful shutdown. Log file not flushed (no trailing newline)."
  implication: "Process killed by SIGKILL (OS), segfault, or unhandled exception that bypasses all try/except."

- timestamp: 2026-05-03
  checked: "projects_may row count"
  found: "projects_may: 0 rows, projects_may_images: 0 rows"
  implication: "No data was ever inserted into projects_may"

- timestamp: 2026-05-03
  checked: "crawl_project() exception handling structure"
  found: "Has try/except around crawler.arun() returning None on failure. Quality score check returns None if <60. Both paths log and continue. BUT: if the crawler itself crashes (segfault, memory fault), no try/except in Python code catches it."
  implication: "A crash inside crawl4ai's native code could terminate the entire Python process without any Python exception being raised."

- timestamp: 2026-05-03
  checked: "Worker memory usage and VPS available memory"
  found: "5.6GB MemAvailable, 3.6GB cached. No dmesg OOM or kill signals. Memory should be sufficient."
  implication: "Memory exhaustion is unlikely cause."

- timestamp: 2026-05-03
  checked: "sync_full_run.log (earlier run at 18:42)"
  found: "Earlier run with MODE=3 also had 0 upserts due to 'relation fullrun_projects_live does not exist'. Projects were extracted (4) but DB write failed."
  implication: "Two different problems: (1) earlier run: wrong table name (MODE=3 instead of 5), (2) current run: process dies before upsert is called."

## Resolution
root_cause: "UNCONFIRMED - but strongest hypothesis: crawl4ai (Playwright) crash in crawl_project() causes unhandled exception or segfault that kills the Python process. Workers W0/W1 each log their [1/504] URL then the process terminates before any error is logged or next steps occur."
fix:
verification:
files_changed: []