# Weekly Research Log – 2025-05-08

## What I Did This Week

* Created a new project structure to better organize all code, documentation, and reports
* Split files into subfolders: `tetris_code/`, `iMotionsSetup/`, `documentation/`, `research_log/`
* Cleaned up repo by removing build artifacts and `__pycache__` files
* Integrated real-time game markers using the iMotions Event API (UDP)
* Documented implementation of `api.py` marker functions
* Wrote `README.md` and added project description
* Used UDP protocol to send real-time markers like `StartGame`, `LineClear`, and `GameOver`
* Fixed marker display issues in iMotions (e.g., `StartGame` not appearing)
* Clarified scene vs standard markers (`M;1` and `M;2`)



##  Important Fixes & Adjustments

*  **Removed the `tetris-env/` folder from Git** using:

  ```bash
  git rm -r --cached tetris-env/
  ```

*  Saved current environment with:

  ```bash
  pip freeze > requirements.txt
  ```

  This ensures all dependencies are tracked in the project.

##  Questions or Issues

* Still troubleshooting why markers don’t show in CSV export

##  Next Steps / Goals

* Replaced old GitHub repo with updated sandbox version
*  Create clean export profile in iMotions

---

Notes:
Everything is now pushed to: https://github.com/ZoiTheofilakou/TetrisCognitionLab.git
