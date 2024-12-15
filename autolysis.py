# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "numpy", "matplotlib", "seaborn", "requests", "Pillow", "python-dotenv"]
# ///

import os
import sys
import json
import warnings
import base64
import requests

import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
from dotenv import load_dotenv

# Suppress warnings globally
warnings.filterwarnings("ignore")
matplotlib.use('Agg')

class DataAnalysisConfig:
    """Configuration class for data analysis settings."""
    load_dotenv()
    api_key = os.getenv("AI_PROXY")
    if not api_key:
        print("Error: AI_PROXY environment variable not set.")
        sys.exit(1)

    API_ENDPOINT = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    REQUEST_HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    LANGUAGE_MODEL = "gpt-4o-mini"

class DataVisualization:
    """
    A class for creating visualizations and generating README narratives.
    """

    @staticmethod
    def create_visualizations(dataframe, output_dir):
        """
        Generate and save impactful data visualizations.

        Args:
            dataframe (pd.DataFrame): Input dataframe
            output_dir (str): Directory to save visualizations
        """
        sns.set_theme(style="whitegrid")  # Set consistent theme for all plots

        visualizations = 0

        # Histogram for the first numeric column
        numeric_columns = dataframe.select_dtypes(include=[np.number]).columns
        if numeric_columns.any() and visualizations < 3:
            column = numeric_columns[0]
            plt.figure(figsize=(10, 6))
            sns.histplot(dataframe[column].dropna(), bins=30, kde=True, color='cornflowerblue')
            plt.axvline(dataframe[column].mean(), color='red', linestyle='--', label='Mean')
            plt.title(f'Distribution of {column}')
            plt.xlabel(column)
            plt.ylabel('Frequency')
            plt.legend(title="Legend", loc="upper right")
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"{column}_histogram.png"))
            plt.close()
            visualizations += 1

        # Bar chart for the first categorical column
        categorical_columns = dataframe.select_dtypes(include=['category', 'object']).columns
        if categorical_columns.any() and visualizations < 3:
            column = categorical_columns[0]
            plt.figure(figsize=(10, 6))
            value_counts = dataframe[column].value_counts()
            sns.barplot(x=value_counts.index[:10], y=value_counts.values[:10], palette='viridis')
            plt.title(f'Top Categories of {column}')
            plt.xlabel(column)
            plt.ylabel('Counts')
            plt.xticks(rotation=45, ha='right')

            # Annotate the bars
            for i, val in enumerate(value_counts.values[:10]):
                plt.text(i, val, f"{val}", ha='center', va='bottom')

            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"{column}_bar.png"))
            plt.close()
            visualizations += 1

        # Pairplot for numeric columns if more than one exists
        if len(numeric_columns) > 1 and visualizations < 3:
            sns.pairplot(dataframe[numeric_columns])
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "pairplot.png"))
            plt.close()
            visualizations += 1

    @staticmethod
    def generate_readme(dataframe, output_dir, readme_filename="README.md"):
        """
        Generate a README file summarizing insights and visualizations.

        Args:
            dataframe (pd.DataFrame): Input dataframe
            output_dir (str): Directory to save README
            readme_filename (str): Name of the README file
        """
        readme_content = """
# Data Analysis and Visualizations

Welcome to the data analysis report! This document outlines key insights derived from the data and is supported by visualizations to provide an intuitive understanding of trends and patterns.

## Key Insights
"""

        numeric_columns = dataframe.select_dtypes(include=[np.number]).columns
        categorical_columns = dataframe.select_dtypes(include=['category', 'object']).columns

        if numeric_columns.any():
            column = numeric_columns[0]
            readme_content += f"""
### 1. Unveiling the Distribution of {column}
![Distribution of {column}](./{column}_histogram.png)
- **What we see**: The histogram showcases how values in {column} are distributed. A noticeable concentration can be observed, indicating common ranges.
- **Why it matters**: Understanding this distribution helps us identify typical values and spot any anomalies or outliers.
- **So what?**: This insight can guide decisions, such as focusing on optimizing for the most frequent ranges or investigating outliers further.
"""

        if categorical_columns.any():
            column = categorical_columns[0]
            readme_content += f"""
### 2. Exploring Top Categories of {column}
![Top Categories of {column}](./{column}_bar.png)
- **What we see**: The bar chart highlights the top 10 most frequent categories in {column}, revealing dominant trends or preferences.
- **Why it matters**: Recognizing dominant categories can guide priorities, such as addressing the needs of the majority.
- **So what?**: This enables targeted strategies that align with the most significant trends or patterns in the data.
"""

        if len(numeric_columns) > 1:
            readme_content += """
### 3. Discovering Relationships in the Data
![Pairplot](./pairplot.png)
- **What we see**: The pairplot visualizes how different numeric columns interact. Patterns, clusters, or correlations become apparent.
- **Why it matters**: Relationships between variables can provide predictive insights and inform data modeling.
- **So what?**: Leveraging these relationships can enhance predictions, strategies, or solutions derived from the data.
"""

        with open(os.path.join(output_dir, readme_filename), "w") as f:
            f.write(readme_content)

        

def main():
    """Main execution function for the data analysis script."""
    if len(sys.argv) < 2:
        print("Usage: python script.py <dataset.csv>")
        sys.exit(1)

    dataset_file = sys.argv[1]

    try:
        # Load dataset
        dataframe = pd.read_csv(dataset_file, encoding='ISO-8859-1')

        # Create output directory
        output_directory = os.path.splitext(os.path.basename(dataset_file))[0]
        os.makedirs(output_directory, exist_ok=True)

        # Create visualizations
        DataVisualization.create_visualizations(dataframe, output_directory)

        # Resize generated images
        for image_filename in os.listdir(output_directory):
            if image_filename.endswith('.png'):
                image_path = os.path.join(output_directory, image_filename)
                img = Image.open(image_path)
                img_resized = img.resize((512, 512))
                img_resized.save(image_path)

        # Generate README
        DataVisualization.generate_readme(dataframe, output_directory)

        

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
