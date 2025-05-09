# 📤 Export Tips – iMotions Data Export Guide

This guide helps ensure accurate and complete export of all EEG, eye-tracking, and LSL event marker data after running your Tetris study in iMotions.

---

## Before Export

* Verify that **all markers appear** in **Sensor Preview** during gameplay
* Ensure **Stimuli are labeled** correctly — for example, events like `LineClear` should appear under their exact label, not as `Unknown`
* Confirm **participant ID** is saved
* Preview the **timeline** to ensure all blocks ran

---

## Export Settings

....Pending additions

1. Go to `Study → Export Data`
2. Choose format: **CSV** (or TSV)
3. Export:

   * EEG (Emotiv)
   * Eye-tracking (Tobii)
   * LSL Event Markers
   * Survey responses (NASA-TLX, feedback)
4. Ensure:

   * Headers included
   * Split files per participant
   * Timestamps or system clock data included

---

## Common Issues & Fixes (Simplified)

* **Missing `StartGame`**:

  * *Cause:* Function is called too late in `main.py`
  * *Fix:* Move the `send_event_marker("StartGame")` call earlier

* **Marker label mismatch**:

  * *Cause:* Label not defined in `eventsource.xml`
  * *Fix:* Add label to XML and reload the file in iMotions

* **Empty markers**:

  * *Cause:* API call missing a label or description
  * *Fix:* Check `api.py` function and provide valid arguments

* **Misaligned timestamps**:

  * *Cause:* System clock drift between EEG/ET and Python
  * *Fix:* Use Python preprocessing to align based on timestamps or offsets

---

## Output Folder

```
exports/
├── participant_001/
│   ├── eeg.csv
│   ├── eyetracking.csv
│   ├── markers.csv
│   ├── surveys.csv
├── participant_002/
│   └── ...
```

This structure improves organization and supports clean pipelines for preprocessing or ML workflows.
Additions relevant to exporting process should be added in this file. 
