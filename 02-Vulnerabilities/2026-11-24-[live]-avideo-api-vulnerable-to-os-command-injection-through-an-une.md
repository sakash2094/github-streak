# [LIVE] AVideo API vulnerable to OS command injection through an une

**Severity:** HIGH

**Description:** ### Summary

The helper `listFFmpegProcesses($keyword)` in `plugin/API/standAlone/functions.php` builds a shell pipeline by interpolating `$keyword` inside single quotes and running it with `exec()`:

```php
$command .= " | grep '$keyword'";
exec($command, $output, $status);
```

The two callers in `plugin/API/standAlone/ffmpeg.json.php` (the `list` mode and the `isKeywordRunning` mode) pass the R

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-63492

---
*Generated on 2026-11-24*