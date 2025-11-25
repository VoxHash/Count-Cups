# Security Policy

## Supported Versions

We actively support the following versions of Count-Cups with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do NOT** open a public issue

Security vulnerabilities should be reported privately to protect users until a fix is available.

### 2. Report via Email

Send an email to **contact@voxhash.dev** with the following information:

- **Subject**: `[SECURITY] Brief description of the vulnerability`
- **Description**: Detailed description of the vulnerability
- **Impact**: Potential impact if exploited
- **Steps to Reproduce**: Clear steps to reproduce the issue
- **Suggested Fix**: If you have a suggested fix (optional)
- **Your Contact Information**: So we can reach out if we need more information

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity, typically 30-90 days

### 4. Disclosure Policy

- We will acknowledge receipt of your report within 48 hours
- We will provide regular updates on the status of the vulnerability
- We will notify you when the vulnerability is fixed
- We will credit you in the security advisory (unless you prefer to remain anonymous)

## Security Best Practices

### For Users

1. **Keep Count-Cups Updated**: Always use the latest version
2. **Camera Permissions**: Only grant camera access to trusted applications
3. **Data Privacy**: All data is stored locally - review your data directory permissions
4. **Network**: Count-Cups does not transmit data by default (telemetry is opt-in)

### For Developers

1. **Dependencies**: Keep all dependencies up to date
2. **Code Review**: All code changes are reviewed before merging
3. **Testing**: Security testing is part of our development process
4. **Reporting**: Report any security concerns immediately

## Known Security Considerations

### Camera Access

- Count-Cups requires camera access for sip detection
- All video processing happens locally - no video is recorded or transmitted
- Camera permissions are requested explicitly by the operating system

### Data Storage

- All data is stored locally in SQLite database
- Database location: `~/.count-cups/data/count_cups.db`
- No cloud sync or external data transmission by default
- Users should secure their data directory appropriately

### Telemetry (Optional)

- Telemetry is disabled by default
- If enabled, only anonymous usage statistics are collected
- No personal data or hydration data is transmitted
- Telemetry can be disabled in Settings > Advanced

### Dependencies

- We regularly update dependencies to address security vulnerabilities
- Security advisories for dependencies are monitored
- Critical security updates are released promptly

## Security Updates

Security updates are released as patch versions (e.g., 1.0.1, 1.0.2). Critical security fixes may be backported to previous versions.

## Security Credits

We thank security researchers who responsibly disclose vulnerabilities. Contributors will be credited in security advisories (unless they prefer to remain anonymous).

## Contact

For security-related inquiries:
- **Email**: contact@voxhash.dev
- **Organization**: VoxHash Technologies

---

**Last Updated**: 2025-01-01

