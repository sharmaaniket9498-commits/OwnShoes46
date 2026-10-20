# OwnSHoes — Shoe Sales Analytics

**Live Dashboard:** [Open OwnSHoes](https://ownshoes46-47d8u6bqxr8llpatrt9gxz.streamlit.app/)

OwnSHoes is a Python + Streamlit shoe-store dashboard featuring a modern interface, product catalogue, sales analytics, inventory management, reports, CSV downloads, and PDF report export.

## Live Website

Visit the deployed dashboard:

**https://ownshoes46-47d8u6bqxr8llpatrt9gxz.streamlit.app/**

## Features

- **Dashboard:** View key sales and business metrics.
- **Product Catalogue:** Browse shoe products and product details.
- **Sales Analytics:** Explore sales trends and visualizations.
- **Inventory Management:** Review and manage sample inventory data.
- **Reports:** Generate reports and export data.
- **CSV Downloads:** Download supported data tables as CSV files.
- **PDF Export:** Export supported reports to PDF.
- **Top Navigation:** Navigate through the dashboard without a left sidebar.
- **Product Photography:** Display real shoe product photos using image URLs.

## Run Locally on Windows

1. Download or clone this repository.
2. Extract the ZIP file if you downloaded one.
3. Open the `SoleVault_Updated` folder if your files are inside it.
4. Double-click `run.bat`.
5. Wait for dependencies to install and Streamlit to start.
6. Open the local URL shown in the terminal, usually:

   http://localhost:8501

## Run Manually

Open PowerShell in the folder containing `app.py` and `requirements.txt`, then run these commands separately:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Project Structure

```text
OwnSHoes/
├── app.py
├── requirements.txt
├── README.md
├── run.bat
├── assets/
├── data/
├── styles/
├── utils/
└── views/
```

## Data and Storage

- The project uses local CSV files in the `data/` directory.
- No separate backend server or database is required for the local version.
- Sample sales data is generated locally on first run.
- Local file changes may not automatically synchronize between different users or deployed instances.

## Product Images

The dashboard uses external product-image URLs. An internet connection is required to load these images. Some image providers may block direct image access, so an image may occasionally fail to display.

## Technology Stack

- Python
- Streamlit
- Pandas
- Plotly
- CSV-based local data storage

## Deployment

The dashboard is hosted on Streamlit Community Cloud and connected to GitHub.

**Live URL:** https://ownshoes46-47d8u6bqxr8llpatrt9gxz.streamlit.app/

## Disclaimer

This project uses sample data for demonstration. Sales figures and inventory values should not be treated as real business records.
