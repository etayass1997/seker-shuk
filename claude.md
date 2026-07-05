# סקר שוק — סוכן ניתוח שוק

## תיאור
PWA לניתוח שוק — frontend בלבד (ללא backend). המשתמש מזין API key של Claude ישירות ב-UI, ושואל שאלות ניתוח שוק. Claude מחפש באינטרנט ומנתח. עיצוב כהה, RTL מלא.

## סטאק
- **Frontend בלבד**: `index.html` — HTML+CSS+JS קובץ יחיד
- **AI**: Claude API (מפתח מצד הלקוח, localStorage)
- **PWA**: `manifest.json` + `sw.js`
- **אין Backend** — כל הלוגיקה בדפדפן

## קבצים
| קובץ | תפקיד |
|------|--------|
| `index.html` | כל ה-App (HTML+CSS+JS) |
| `manifest.json` | PWA manifest |
| `sw.js` | Service Worker |
| `icon-192.png` / `icon-512.png` | אייקוני PWA |

## עיצוב
- כהה (dark mode): `--bg: #0d0d0d`
- פונט: Heebo (Google Fonts)
- RTL מלא
- מעברי מסך עם opacity/transform animations

## פריסה
אפשר להגיש ישירות מ-GitHub Pages / Netlify — אין צורך בשרת.
