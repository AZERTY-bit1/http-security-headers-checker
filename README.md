# 🌐 HTTP Security Headers Checker

![tests](https://github.com/AZERTY-bit1/http-security-headers-checker/actions/workflows/tests.yml/badge.svg)
![python](https://img.shields.io/badge/python-3.8%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)

Checks if **your** website sends the recommended security headers and gives it a grade from **A to F**, with tips to fix what is missing.

## ✨ Features

- Checks HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP
- Detects version leaks (`Server: Apache/2.4.1`, `X-Powered-By`)
- One normal GET request, like a browser
- Pure Python standard library

## 🚀 Usage

No installation needed - only Python 3.8+.

```bash
git clone https://github.com/AZERTY-bit1/http-security-headers-checker.git
cd http-security-headers-checker
python headers_checker.py https://example.com
```

## 📸 Example output

```
Grade: C  (58%)

  [OK]      Strict-Transport-Security
  [MISSING] Content-Security-Policy
            -> Limits where scripts can load from (blocks XSS).
```

## 🧪 Tests

```bash
python -m unittest discover -s tests -v
```

## ⚠️ Disclaimer

This is a **defensive / educational** tool. Only use it on systems and data you own or are allowed to check.

## 📄 License

MIT - see [LICENSE](LICENSE).
