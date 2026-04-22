# Frontend Guide

The frontend is a single-page vanilla web application served as static files directly by the FastAPI backend. No frontend build step, bundler, or framework is required.

---

## File Locations

```
src/static/
├── index.html   # Page structure and layout
├── app.js       # All dynamic behaviour (fetch, render, events)
└── styles.css   # All CSS rules
```

The static directory is mounted by FastAPI at `/static`:

```python
# src/app.py
app.mount("/static", StaticFiles(directory=...), name="static")
```

Navigating to `http://localhost:8000/` automatically redirects to `/static/index.html`.

---

## index.html — Page Structure

The page has three main regions:

| HTML element | `id` | Purpose |
|--------------|------|---------|
| `<header>` | — | School name and subtitle |
| `<section>` | `activities-container` | Dynamically rendered activity cards |
| `<section>` | `signup-container` | Sign-up form (email + activity selector) |
| `<footer>` | — | Copyright line |

All dynamic content is injected by `app.js`; the initial HTML contains only placeholder text.

---

## app.js — JavaScript Flow

### Initialisation

```
DOMContentLoaded → fetchActivities()
```

On page load, `fetchActivities()` is called immediately, which:
1. Calls `GET /activities` with `cache: "no-store"`.
2. Clears the loading placeholder.
3. Renders one **activity card** per activity (see below).
4. Populates the `<select>` dropdown with activity names.

### Activity Card

Each card is a `<div class="activity-card">` injected into `#activities-list`, containing:

- Activity name (`<h4>`)
- Description (`<p>`)
- Schedule (`<p>`)
- Availability: spots left = `max_participants - participants.length` (`<p>`)
- Participants list (`<ul class="participants-list">`) with a 🗑 remove button per participant

### Signup Flow

1. User fills in their email and selects an activity.
2. Form submission is intercepted (`preventDefault`).
3. `POST /activities/{activity}/signup?email={email}` is sent.
4. On success: success message shown, form reset, `fetchActivities()` re-called to refresh.
5. On error: error message shown (uses `detail` from the JSON error response).

### Unregister Flow

1. User clicks the 🗑 (trash) button next to a participant's email.
2. The button is disabled immediately to prevent double-clicks.
3. `DELETE /activities/{activity}/signup?email={email}` is sent.
4. On success: success message shown, `fetchActivities()` re-called.
5. On error: error message shown; button re-enabled.

### Message display

`showMessage(text, type)` sets `#message` content and applies a CSS class (`success`, `error`, or `info`).  
The message auto-hides after **5 seconds** via `setTimeout`.

---

## styles.css — CSS Conventions

- **Reset**: `box-sizing: border-box`, zeroed margins/padding globally.
- **Colour palette**: deep blue `#1a237e` (header, headings, buttons), medium blue `#0066cc` (activity card titles).
- **Layout**: `<main>` uses `flexbox` with `flex-wrap: wrap` and centres the two sections side by side on wider screens.
- **Activity cards**: white background with a subtle blue gradient, rounded corners, box shadow.
- **Participant items**: each rendered as a flex row with the email on the left and the remove button on the right.
- **Status messages**: colour-coded — green for success, red for error, teal for info.
- **Responsive**: sections stack vertically on narrow screens (flexbox wrapping).

---

## Adding a New UI Feature

1. Update `index.html` only if you need a new static element or form field.
2. Add event listeners or fetch calls in `app.js`.
3. Add styles to `styles.css` following the existing naming conventions (BEM-like class names such as `.activity-card`, `.participant-item`).
4. There is no linting or build step — changes are reflected immediately on page refresh.
