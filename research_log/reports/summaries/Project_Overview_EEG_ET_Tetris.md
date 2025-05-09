# Project Overview – EEG Tetris Cognitive Load Study

This study explores **cognitive load dynamics during Tetris gameplay** by synchronizing **real-time gameplay events** with **EEG** and **eye-tracking (ET)** data using the **iMotions 10 platform**.

---

## Research Goals

* Investigate **how cognitive load fluctuates** during gameplay of different difficulty levels
* Understand **EEG frequency band activity** and **eye movement patterns** during high vs low load periods
* Use **real-time gameplay markers** (e.g., LineClear, StartGame) to improve data segmentation

---

## Modalities Used

| Modality     | Tool                             |
| ------------ | -------------------------------- |
| EEG          | Emotiv EPOC X                    |
| Eye-tracking | Tobii Pro Fusion                 |
| Events       | Python via UDP to iMotions (LSL) |

---

## Technical Stack

* **Game Logic**: Python (pygame, pygame\_menu)
* **Event Markers**: Custom `api.py` script to send UDP messages (M;1 and M;2 formats)
* **iMotions 10**: Receives markers, synchronizes signals, manages surveys (NASA-TLX)

---

## Experimental Blocks

* Gameplay Block
* Level Play: Easy → Medium → Hard
* NASA-TLX after each block
* Final Feedback

---

## Future Use: Machine Learning

...pending...

---

For implementation logs and setup instructions, see:

* `documentation/`
* `iMotionsSetup/`
* `research_log/`

---


