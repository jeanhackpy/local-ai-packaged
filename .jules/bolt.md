## 2025-05-14 - Python Syntax Verification Artifacts
**Learning:** Running `python3 -m py_compile` or executing Python scripts (like unit tests) generates `__pycache__` directories even if `PYTHONDONTWRITEBYTECODE=1` is set in some environments or toolchains. These binary artifacts are strictly forbidden in PRs.
**Action:** Always manually verify and run `rm -rf __pycache__` before requesting code review or submitting, especially after running syntax checks or tests.
