# Roadmap — Count-Cups

Current release: **1.0.1** (desktop hydration tracker with local CV sip detection).

This roadmap stays near-term and realistic. Items move here only when they are next in line to ship.

## Near term (v1.1)

- Detection reliability: better calibration UX, fewer false positives under desk lighting
- Reminder polish: configurable quiet hours and smarter goal nudges
- Data: CSV import/export hardening and backup/restore of `~/.count-cups/`
- Platform: document and CI-guard OpenCV 4.x pin; keep Python 3.10–3.12 as supported matrix

## Next (v1.2)

- Optional MediaPipe engine usable on supported Python versions (still blocked on 3.13+)
- Stronger analytics: streaks, weekly trends, clearer dashboard charts
- Accessibility pass: keyboard navigation and high-contrast themes

## Later

- Local REST API for personal integrations
- Optional PWA companion for manual logging on phone
- Health platform export (Apple Health / Google Health Connect) behind explicit opt-in

## Explicitly not planned soon

- Cloud sync / accounts
- Team or multi-user SaaS features
- Mobile App Store apps
- “AI-powered” marketing claims beyond the existing local CV heuristics

---

*Living document — adjust based on real usage feedback.*

*Last Updated: October 5, 2026*
