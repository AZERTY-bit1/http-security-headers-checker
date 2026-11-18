#!/usr/bin/env python3
"""HTTP Security Headers Checker.

Checks whether a website YOU own or manage sends the recommended
security headers (HSTS, CSP, X-Frame-Options...) and gives a grade
from A to F with tips to fix what is missing. Sends a single normal
GET request - like a browser visiting the home page.
"""
import argparse
import sys
import urllib.request

CHECKS = {
    "Strict-Transport-Security": (20, "Forces HTTPS. Add: max-age=31536000; includeSubDomains"),
    "Content-Security-Policy": (25, "Limits where scripts can load from (blocks XSS)."),
    "X-Frame-Options": (10, "Prevents clickjacking. Add: DENY or SAMEORIGIN"),
    "X-Content-Type-Options": (10, "Stops MIME sniffing. Add: nosniff"),
    "Referrer-Policy": (10, "Controls leaked URLs. Add: strict-origin-when-cross-origin"),
    "Permissions-Policy": (10, "Restricts camera, micro, geolocation... access."),
    "Cross-Origin-Opener-Policy": (5, "Isolates your page. Add: same-origin"),
}
LEAKY = ("Server", "X-Powered-By", "X-AspNet-Version")


def grade(headers: dict) -> dict:
    h = {k.lower(): v for k, v in headers.items()}
    score, present, missing, leaks = 0, [], [], []
    for name, (pts, tip) in CHECKS.items():
        if name.lower() in h:
            score += pts
            present.append(name)
        else:
            missing.append((name, tip))
    for name in LEAKY:
        val = h.get(name.lower())
        if val and any(ch.isdigit() for ch in val):
            leaks.append(f"{name}: {val}")
    score = max(0, score - 5 * len(leaks))
    pct = round(score * 100 / sum(p for p, _ in CHECKS.values()))
    letter = "A" if pct >= 90 else "B" if pct >= 75 else "C" if pct >= 55 else "D" if pct >= 35 else "F"
    return {"percent": pct, "grade": letter, "present": present, "missing": missing, "leaks": leaks}


def fetch_headers(url: str, timeout: int = 10) -> dict:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    req = urllib.request.Request(url, headers={"User-Agent": "headers-checker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return dict(resp.headers.items())


def main():
    p = argparse.ArgumentParser(description="Grade the HTTP security headers of your website")
    p.add_argument("url")
    args = p.parse_args()
    try:
        headers = fetch_headers(args.url)
    except Exception as e:  # noqa: BLE001
        sys.exit(f"Could not reach {args.url}: {e}")
    r = grade(headers)
    print(f"Grade: {r['grade']}  ({r['percent']}%)\n")
    for name in r["present"]:
        print(f"  [OK]      {name}")
    for name, tip in r["missing"]:
        print(f"  [MISSING] {name}\n            -> {tip}")
    for leak in r["leaks"]:
        print(f"  [LEAK]    {leak}  (hide version numbers)")


if __name__ == "__main__":
    main()
