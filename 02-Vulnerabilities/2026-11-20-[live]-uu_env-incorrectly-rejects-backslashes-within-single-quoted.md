# [LIVE] uu_env incorrectly rejects backslashes within single-quoted 

**Severity:** LOW

**Description:** In `env -S`, GNU keeps backslashes literal inside single quotes (except `\\` and `\'`); uutils errors on sequences like `\a`. This is the backslash-handling issue of the broader `-S`/`--split-string` parsing divergence.
```
env -S"printf %s '\''\\x'\''"   # GNU prints \x ; uutils: invalid sequence '\x' in -S (125)
```

---
_Zellic private finding (zellic-ext/coreutils-private PR #117). Reported in

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-35377

---
*Generated on 2026-11-20*