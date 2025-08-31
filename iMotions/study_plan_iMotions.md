# Study Plan – EEG-ET Tetris Study (iMotions 10)

This document outlines the optimized study workflow for EEG Tetris study using iMotions 10. It leverages the **Survey Study** structure, LSL event markers, and the latest iMotions features.

---

## Study Type

**Survey Study** – Recommended for combining instructions, surveys, and screen-based gameplay blocks.

---

## Study Block Structure

1. **Welcome Screen (Survey)** – Welcome text, optional informed consent checkbox, participant ID input
2. **Informed Consent (Survey)** – Dedicated informed consent screen (optional separate block)
3. **Instructions (Survey)** – Describes full timeline (e.g., familiarization → gameplay → survey)
4. **Notes Before Familiarization (Survey)** – Optional clarifying instructions
5. **Controls (Survey)** – Shows image (`controls.png`) and gameplay keys
6. **Tetris Gameplay – Familiarization (Screen-Based)** – Intro session
7. **NASA-TLX Questionnaire (Survey)** – Measures perceived cognitive load
8. **Find Skill Level (Screen-Based)** – Player completes task for calibration
9. **Break (Web or Image)** – Optional mental rest period
10. **Tetris Gameplay – Easy/Medium (Screen-Based)** – Gameplay 
11. **NASA-TLX Questionnaire (Survey)** – Same scale repeated
12. **Tetris Gameplay – Medium/Hard (Screen-Based)** – Increasing difficulty
13. **NASA-TLX Questionnaire (Survey)** – Final rating of load
14. **Final Feedback & Thank You (Survey)** – Open comments + exit screen



## Tips for Setup in iMotions 10

* Use **LSL integration** for real-time marker syncing
* Manage stimuli via **Stimuli Overview Panel**

---

## Data Export & Analysis

After the session:

* Export EEG, eye-tracking, and LSL marker data (CSV or TSV)
* Analyze alongside NASA-TLX responses
* Correlate game events with EEG/ET patterns to estimate cognitive load
