\# Game Protocol \& Study Flow



\## Phases



\### 1) Base Level — Familiarity

\- Explain controls and rules to the participant.

\- Slowest level; \*\*no speed increases\*\*.

\- After the participant learns the controls, proceed to the next phase.



\### 2) Find Skill Level (3 minutes)

\- Play on Base Level for 3 minutes.

\- Instruction: \*“Clear as many lines as you can within the time limit.”\*

\- Lines cleared → assigned skill level:

&nbsp; - `< 10` → \*\*Easy\*\*

&nbsp; - `10–19` → \*\*Medium\*\*

&nbsp; - `≥ 20` → \*\*Hard\*\*

\- \*\*Important:\*\* Tell the participant which level they were assigned.



\### 3) Mental Workload Blocks

If the assigned level is \*\*Easy\*\* or \*\*Medium\*\* during Find-Skill-Level:

\- \*\*Easy\*\* — 10 min → then fill \*\*Survey 1\*\*

\- \*\*Medium\*\* — 10 min → then fill \*\*Survey 2\*\*



If the assigned level is \*\*Hard\*\* during Find-Skill-Level:

\- \*\*Medium\*\* — 10 min → then fill \*\*Survey 1\*\*

\- \*\*Hard\*\* — 10 min → then fill \*\*Survey 2\*\*



---



\## Data \& Logging



\- Each level creates/append a log file named `"<Level>\_Level\_Data.txt"`, e.g. `Hard\_Level\_Data.txt`.

\- Fields are \*\*semicolon-separated JSON blobs\*\* on one line:

{"game\_data": "value"};{"end\_data": {"Level": "easy", "speed": 120}}







\### Collected signals



\*\*Quit events\*\*

\- Game interruption (key press). Indicates phase: start screen / gameplay / game over / time over.

\- Includes `game\_end\_data`.



\*\*On game start\*\*

\- Timestamp \& day

\- Game type: Base, Find Skill, Easy, Medium, Hard

\- Starting speed, selected settings:

\- Overall time limit

\- Starting speeds (easy/medium/hard)

\- Maximum speeds (easy/medium/hard)

\- Speed increment value

\- Increase speed after N line clears

\- Level change times (if any)

\- Toggles: show score / line clears / next block / timer / lock movement



\*\*While playing\*\*

\- \*\*Block events\*\*

\- `timestamp`

\- `current\_block` (piece after previous was placed)

\- \*\*Key press events\*\*

\- `timestamp`

\- `key`

\- `action`: `"happened"` or `"nothing"`

\- \*\*Speed changes\*\*

\- `timestamp`

\- Trigger: `line\_clears` or `level\_change` (or `"nothing"` if at max)

\- `new\_speed` (+ `new\_level` if applicable)



\*\*On game end\*\*

\- `timestamp`

\- `game`

\- `cause`: `game\_over` | `time\_over` | `quit`

\- `last\_level`

\- `time\_played\_ms`

\- `current\_speed`

\- `score`

\- `lines\_cleared`



\### Example log snippet

```text

{"Game started":"Fri 18/10/2024 10:05:51.697","Game":"Hard Level","Start level":"Hard","Starting speed":200,

"Selected settings":{"Time Limit":"10m","Starting level speeds":{"Hard":200},"Maximum level speeds":{"Hard":200},

"Speed increases by":20,"Increase speed after line clears":1,"Show score":true,"Show line clears":true,

"Show next block":true,"Show timer":true,"Lock block movement":false};

{"Time":50,"Current block":"I Block"};

{"Time":695,"KeyDown":"Up\_Key","Action":"happened"};

{"Time":181955,"Game was":"Hard Level","Cause":"Game Over","Level":"Hard","Time played (ms)":100173,

"Current speed":200,"Score":1713,"Lines cleared":14};

{"Time":183221,"Game was":"Hard Level","Cause":"Quit","Level":"Hard","Time played (ms)":784,

"Current speed":200,"Score":0,"Lines cleared":0}











