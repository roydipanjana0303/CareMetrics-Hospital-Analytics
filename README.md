# 🩺 CareMetrics — Hospital Patient Data Analytics Dashboard

**CareMetrics** is an interactive web-based analytics dashboard built using **Python, Pandas, NumPy, Matplotlib, Seaborn, and Streamlit**. It allows hospitals and healthcare administrators to upload raw patient CSV records, perform automated data preprocessing, explore statistical summaries, and generate interactive visual reports without complex database setups.

---

## ✨ Key Features

- **CSV Data Ingestion:** Upload a hospital patient CSV from the Home page or explore the included sample dataset.
- **Guided Navigation:** Open Home, Dashboard, Preprocessing, Analysis, Visualisations, and Dataset from the top navigation. Native Streamlit page links support browser routing and direct section URLs.
- **Automated Data Preprocessing:** 
  - Audits missing values using `isnull()`.
  - Removes duplicate entries using `drop_duplicates()`.
  - Drops incomplete critical records using `dropna()`.
  - Imputes missing age, treatment cost, and gender values using `fillna()`.
- **Pandas Data Manipulation:** Implements label-based (`loc`) and integer-position (`iloc`) indexing, slicing, boolean filtering, multi-column sorting, and `groupby()` aggregations.
- **Interactive Dashboard Filters:** Dynamically slice KPIs and charts by hospital branch, medical condition, and patient age range.
- **Visual Analytics Suite:**
  - **Bar Chart:** Patient admission volume across hospitals.
  - **Pie Chart:** Patient gender demographic distribution.
  - **Line Chart:** Monthly patient admission trends.
  - **Histogram + KDE:** Patient age distribution.
  - **Box Plot:** Treatment cost distribution and outliers across medical conditions.
- **Data Export:** One-click CSV download of the cleaned and filtered dataset.

---

## 📂 Project Structure

```text
CareMetrics/
│
├── app.py                  # Landing page, navigation, upload flow, dashboard, and analysis views
├── data_processor.py       # Pandas preprocessing, indexing, slicing, and analytics functions
├── visualizer.py           # Matplotlib & Seaborn visualization functions
├── generate_sample_data.py # Script to generate a realistic hospital CSV for testing
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 🚀 Run Locally

Install the dependencies and start the Streamlit app:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

From the Home page, upload a patient CSV or choose **Explore Dashboard** to load the sample data. Dashboard filters are available in the sidebar.