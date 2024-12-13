# Automated Data Analysis and Visualization Using GPT-4o-Mini for Advanced Insights

## Project Overview
This project automates the process of data analysis, visualization, and insight generation from any given dataset using Python. By integrating a Large Language Model (LLM) with advanced data processing and visualization techniques, the system generates detailed Markdown reports complemented by high-quality charts. It is designed to work seamlessly with a wide variety of CSV datasets, providing flexible analysis options for different use cases.

## Key Features

### 1. Comprehensive Automated Analysis
- Automatically performs statistical summaries, identifies missing data, and detects anomalies.
- Conducts advanced correlation studies and clustering analyses to uncover patterns in data.
- Uses GPT-4o-Mini to provide advanced insights, suggest new analytical techniques, and recommend improvements.

### 2. Dynamic Visualization Generation
- Automatically generates 1–3 charts in PNG format tailored to the dataset.
- Supports a range of visualizations, including heatmaps and bar charts, to best represent the data's features and analysis outcomes.

### 3. Narrative and Insight Generation
- The LLM crafts detailed narratives about the dataset, analysis methods, key findings, and broader implications.
- Generates a cohesive Markdown report (README.md) that integrates the narrative and visualizations for clear communication.

### 4. Efficient LLM Resource Utilization
- Preprocesses and summarizes data to reduce reliance on direct dataset transfers when querying the LLM.
- Optimizes token usage to ensure efficient and precise analyses.

### 5. Universal CSV Dataset Compatibility
- Adapts to various CSV datasets with different column types, distributions, and complexities, ensuring robust performance for a wide range of use cases.

### 6. Self-Contained and Independent Execution
- Operates as a standalone Python script (`autolysis.py`) requiring only standard Python libraries, with no external dependencies.

### 7. Ease of Use and Integration
- Simple execution with the `uv` CLI tool for end-to-end functionality:
  ```bash
  uv run autolysis.py dataset.csv

# Workflow for Data Analysis and Report Generation

## 1. Data Preprocessing
- **Reads the CSV file** and extracts metadata such as column names, data types, and sample values.  
- **Identifies missing data, anomalies, and outliers** for further examination.

## 2. Exploratory Data Analysis (EDA)
Performs a full suite of exploratory analyses, including:
- **Statistical summaries** for all variables.
- **Correlation matrices** to evaluate relationships between variables.
- **Anomaly detection** and outlier identification.
- **Clustering** to identify groups of similar data points.

## 3. LLM Integration
- **Transmits dataset metadata and EDA results** to `GPT-4o-Mini` to obtain deeper insights.
- **Incorporates LLM-suggested Python code** or additional analyses into the workflow.

## 4. Visualization Creation
- **Generates high-quality charts** using Seaborn and Matplotlib.
- **Saves visualizations** as PNG files in the working directory for easy integration into reports.

## 5. Narrative Report Generation
The LLM generates a structured Markdown report that includes:
- **Dataset overview.**
- **Methodology and analysis techniques.**
- **Key findings and their implications.**
- **Embedded visualizations** to support the narrative.

## 6. Output Files
The script produces the following output files:
- `README.md`: The detailed Markdown report with analysis results and visualizations.
- `*.png`: PNG files containing the generated visualizations.

---

## Sample Datasets
The system has been tested with the following datasets:
1. **goodreads.csv**: A dataset of 10,000 books from GoodReads, including genres, ratings, and other metadata.
2. **happiness.csv**: Global data from the World Happiness Report, focusing on happiness indices and contributing factors.
3. **media.csv**: Faculty evaluations of movies, TV series, and books, blending subjective ratings with objective data.

---

## Usage Instructions
1. Clone the repository and navigate to the project directory.
2. Set up the environment variable for LLM authentication:
   ```bash
   export AI_PROXY=your-token-here



