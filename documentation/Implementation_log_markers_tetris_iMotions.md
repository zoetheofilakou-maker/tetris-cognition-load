# Implementation Log: iMotions Event Marker Integration

This log documents exactly where and how gameplay events were integrated with iMotions event markers using Python and XML. It follows a modular pattern with `api.py`all communication with iMotions is handled with api.py.

---

## Goal

To send real-time markers for both discrete events (e.g., `ScoreUpdate`) and scene transitions (e.g., `EasyLevel`) from the Tetris game to iMotions using UDP protocol.

---

## 1. `api.py` Marker Functions

These are the centralized functions used to send markers:

```python
send_event_marker(label, description)
send_scene_start(label)
send_scene_end(label)
send_line_clear()
send_score_update(score)
send_level_update(level)
send_line_clear_summary(total_lines)
```

All messages follow iMotions format (`M;1;...` or `M;2;...`) and are sent to localhost on port 8089.

---

## 2. `main.py` Integration

* `send_event_marker("StartGame", ...)` → after waiting screen ends
* `send_scene_start("EasyLevel")` → at level start
* `send_scene_end("EasyLevel")` → at level end (e.g., game over or timeout)

---

## 3. `grid.py` Integration

* `send_line_clear()` → inside `is_row_full()`
* Called when a row is cleared and blocks drop

---

## 4. `game.py` Integration

* `send_score_update(score)` → inside `write_end_game_data()`
* `send_level_update(level)` → same as above
* `send_line_clear_summary(total_lines)` → same
* `send_scene_end(...)` → also in `write_end_game_data()`

---

## 5. `eventsource.xml` Notes

* All events (e.g., `StartGame`, `ScoreUpdate`) defined as `<Sample>` and `<Field>` elements
* Field ID limited to 20 chars (e.g., `LineClearsSum` instead of `LineClearsSummarySample`)

---

##  6. Testing & Fixes

* ✅ Fixed: `StartGame` not appearing → added call in `main.py`
* ✅ Added: `from api import send_event_marker` to import properly
* ✅ Verified: Markers show live in iMotions Sensor Preview

---

## To Do

* [ ] Confirm export of markers in iMotions CSV
* [ ] Add timestamps if needed
* [ ] Create custom export profile in iMotions

> This log supports reproducibility and serves as a coding reference.
