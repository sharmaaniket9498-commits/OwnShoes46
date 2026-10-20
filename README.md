# OwnSHoes — Shoe Sales Analytics

A local Python + Streamlit shoe-store dashboard with top-only navigation, product catalogue, sales analytics, inventory management, reports, CSV downloads and PDF report export.

## Easiest way to run on Windows
1. Extract the ZIP fully.
2. Open the `SoleVault_Updated` folder.
3. Double-click `run.bat`. It creates a local virtual environment, installs dependencies and starts Streamlit.
4. Open the URL shown in the terminal (usually http://localhost:8501).

## Run manually
Open PowerShell inside this folder and run:
```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Notes
- The app uses local CSV files in `data/`; no backend server or database is required.
- The UI uses real product-photo URLs, not generated shoe illustrations. Internet access is required for the linked product photos to load. Some image providers may block direct hotlinking; if a photo is unavailable, use another direct product-image URL.
- Sample sales are generated locally on first run.
