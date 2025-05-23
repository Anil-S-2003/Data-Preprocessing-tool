#  Data Preprocessing Tool – Missing Value Detector

A web-based data cleaning utility that helps users detect and handle missing values in CSV and Excel datasets. Designed to assist data analysts and students in preparing datasets for analysis or machine learning pipelines.

---

##  Features

-  Upload CSV or Excel files via a simple web interface
-  Detect missing/null values across rows and columns
-  Gives Column name and cell number of the missing data 
---

##  Tech Stack

- **Frontend:** HTML, CSS
- **Backend:** Python (Flask)
- **Database:** MongoDB (for logging user uploads and activity)
- **Libraries:** Pandas, NumPy

---

##  How It Works

1. Upload a `.csv` or `.xlsx / .xls` file
2. Backend scans the dataset for missing/null values
3. Summary of null values per column is displayed
4. Tool gives output as column name and cell number of the missing data 
---

