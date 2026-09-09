# Public schedule deployment

GitHub Pages uses GitHub Actions as its deployment source (enabled September 9, 2026).
The refresh workflow tests and fetches the public Entertune schedule before publishing it.

Public feed: https://pasie15.github.io/entertune-park-schedule/show-schedule.json

This repository mirrors confirmed Eventbrite listings; it does not create events.
Daily event maintenance is configured separately to retain a future rotation, preserve existing bookings, and avoid duplicate artist/start times. Only successfully published events may appear in the source feed.

If deployment fails, inspect the Actions run and the Pages environment. Enabling Pages after a failed run requires a fresh workflow run.
