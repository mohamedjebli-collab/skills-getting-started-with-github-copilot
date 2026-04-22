# API Reference

The Mergington High School Activities API is a REST API built with FastAPI.  
Base URL when running locally: `http://127.0.0.1:8000`

Interactive documentation is available at `/docs` (Swagger UI) and `/redoc`.

---

## Endpoints

### `GET /`

Redirects the browser to the static web UI.

| | |
|---|---|
| **Response** | `307 Temporary Redirect` → `/static/index.html` |

---

### `GET /activities`

Returns all extracurricular activities with their details and current participant list.

**Response — 200 OK**

```json
{
  "Chess Club": {
    "description": "Learn strategies and compete in chess tournaments",
    "schedule": "Fridays, 3:30 PM - 5:00 PM",
    "max_participants": 12,
    "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
  },
  "Programming Class": { ... },
  ...
}
```

The response is a JSON object where each **key** is the activity name and each **value** is an [Activity object](#activity-object).

---

### `POST /activities/{activity_name}/signup`

Registers a student for an activity.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `activity_name` | string | Name of the activity (URL-encoded if it contains spaces) |

**Query parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | string | ✅ | Student email address |

**Example request**

```http
POST /activities/Chess%20Club/signup?email=alice%40mergington.edu
```

**Response — 200 OK**

```json
{
  "message": "Signed up alice@mergington.edu for Chess Club"
}
```

**Error responses**

| Status | `detail` | Cause |
|--------|----------|-------|
| `404 Not Found` | `"Activity not found"` | `activity_name` does not exist |
| `400 Bad Request` | `"Student already signed up for this activity"` | `email` is already in the participants list |

---

### `DELETE /activities/{activity_name}/signup`

Removes a student from an activity.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `activity_name` | string | Name of the activity (URL-encoded if it contains spaces) |

**Query parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | string | ✅ | Student email address |

**Example request**

```http
DELETE /activities/Chess%20Club/signup?email=michael%40mergington.edu
```

**Response — 200 OK**

```json
{
  "message": "Unregistered michael@mergington.edu from Chess Club"
}
```

**Error responses**

| Status | `detail` | Cause |
|--------|----------|-------|
| `404 Not Found` | `"Activity not found"` | `activity_name` does not exist |
| `404 Not Found` | `"Student is not signed up for this activity"` | `email` is not in the participants list |

---

## Activity Object

Every activity value in the `/activities` response follows this schema:

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Short description of the activity |
| `schedule` | string | Human-readable meeting schedule |
| `max_participants` | integer | Maximum number of allowed participants |
| `participants` | array of strings | Email addresses of currently signed-up students |

---

## Pre-loaded Activities

The server starts with the following nine activities in memory:

| Activity | Schedule | Max participants |
|----------|----------|-----------------|
| Chess Club | Fridays, 3:30 PM – 5:00 PM | 12 |
| Programming Class | Tuesdays and Thursdays, 3:30 PM – 4:30 PM | 20 |
| Gym Class | Mon, Wed, Fri, 2:00 PM – 3:00 PM | 30 |
| Basketball Team | Mondays and Wednesdays, 4:00 PM – 5:30 PM | 15 |
| Tennis Club | Tuesdays and Thursdays, 3:30 PM – 5:00 PM | 16 |
| Art Studio | Wednesdays, 3:30 PM – 5:00 PM | 18 |
| Music Band | Mondays and Fridays, 3:45 PM – 4:45 PM | 25 |
| Debate Team | Thursdays, 4:00 PM – 5:30 PM | 10 |
| Science Club | Wednesdays, 4:00 PM – 5:30 PM | 22 |

> Data is stored in memory and resets to these defaults whenever the server restarts.

---

## URL encoding

Activity names that contain spaces must be URL-encoded when used in path parameters. Most HTTP clients handle this automatically.

| Activity name | URL-encoded form |
|---------------|-----------------|
| `Chess Club` | `Chess%20Club` |
| `Programming Class` | `Programming%20Class` |
| `Basketball Team` | `Basketball%20Team` |
