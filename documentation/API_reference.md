# API Reference – Marker Functions (api.py)

This file documents the key marker-sending functions defined in `api.py`. These functions send formatted UDP messages to iMotions, and are used across the Tetris gameplay codebase to tag events in real time.

---

## Functions

### 1. `send_event_marker(label, description)`

* **Purpose:** Sends a single M;1 event marker with a label and description
* **Used for:** `StartGame`, `GameOver`, etc.
* **Example:**

  ```python
  send_event_marker("StartGame", "Player started the game")
  # Sends: M;1;;;StartGame;Player started the game;D;

  ```

### 2. `send_scene_start(label)`

* **Purpose:** Begins a scene marker (M;2)
* **Used for:** `EasyLevel`, `HardLevel`, etc.
* **Example:**

  ```python
  send_scene_start("EasyLevel")
  # Sends: M;2;;;EasyLevel;Scene start;B;

  ```

### 3. `send_scene_end(label)`

* **Purpose:** Ends a scene marker (M;2)
* **Used for:** Called when level ends or timeout happens
* **Example:**

  ```python
  send_scene_end("EasyLevel")
  # Sends: M;2;;;EasyLevel;Scene end;E;

  ```

### 4. `send_score_update(score)`

* **Purpose:** Sends current score as an M;1 marker
* **Example:**

  ```python
  send_score_update(400)
  # Sends: M;1;;;ScoreUpdate;400;D;

  ```

### 5. `send_level_update(level)`

* **Purpose:** Sends current level as an M;1 marker
* **Example:**

  ```python
  send_level_update("Medium")
  # Sends: M;1;;;LevelUpdate;Medium;D;

  ```

### 6. `send_line_clear()`

* **Purpose:** Sends a marker when a row is cleared
* **Used in:** `grid.py` inside `is_row_full()`
* **Example:**

  ```python
  send_line_clear()
  # Sends: M;1;;;LineClear;;D;

  ```

### 7. `send_line_clear_summary(total_lines)`

* **Purpose:** Sends a summary of cleared lines at game end
* **Example:**

  ```python
  send_line_clear_summary(8)
  # Sends: M;1;;;LineClearsSum;8;D;

  ```

---

## UDP Transmission Details

* Messages are sent to: `localhost:8089`
* Format follows iMotions standard: `M;<type>;;;<label>;<value>;<status>;
  \n`
* `M;1` = single momentary event
* `M;2` = scene (begin/end)

---

> This file will be updated as new marker functions are added or modified.
