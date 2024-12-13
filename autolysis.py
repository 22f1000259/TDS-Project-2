# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx",
#   "pandas",  # Or another stable version
#   "numpy",  # Ensure compatibility between numpy and pandas
#   "seaborn",
#   "matplotlib",
#   "chardet",
#   "python-dotenv"
# ]
# ///

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import httpx
import chardet
from dotenv import load_dotenv, dotenv_values

# Force non-interactive matplotlib backend
matplotlib.use('Agg')

# Load environment variables
load_dotenv()

# Constants
API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AI_PROXY = os.getenv("AI_PROXY")

if not AI_PROXY:
    raise ValueError("API token not set. Please set AI_PROXY in the environment.")

def load_data(file_path):
    """Load CSV data with encoding detection."""
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']
        return pd.read_csv(file_path, encoding=encoding)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

def analyze_data(df):
    """Perform basic data analysis."""
    numeric_df = df.select_dtypes(include=['number'])  # Select only numeric columns
    analysis = {
        'summary': df.describe(include='all').to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'correlation': numeric_df.corr().to_dict()  # Compute correlation only on numeric columns
    }
    return analysis

def visualize_data(df, output_dir, base_name):
    """Generate and save visualizations."""
    sns.set(style="whitegrid")
    
    # Select only numeric columns for the correlation matrix
    numeric_df = df.select_dtypes(include=['number'])
    
    if not numeric_df.empty:
        # Generate correlation heatmap if there are numeric columns
        correlation_matrix = numeric_df.corr()  # Only numeric columns are included
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
        plt.title('Correlation Heatmap')
        plt.savefig(os.path.join(output_dir, f'{base_name}_heatmap.png'))
        plt.close()
    else:
        print("No numeric columns to compute correlation.")

    # Generate histograms for numeric columns, but limit to only 2
    numeric_columns = df.select_dtypes(include=['number']).columns
    if len(numeric_columns) >= 2:  # Ensure there are at least 2 numeric columns for histograms
        for column in numeric_columns[:2]:  # Limit to 2 charts (after the heatmap)
            plt.figure()
            sns.histplot(df[column].dropna(), kde=True)
            plt.title(f'Distribution of {column}')
            plt.savefig(os.path.join(output_dir, f'{base_name}_{column}_distribution.png'))
            plt.close()

def generate_narrative(analysis, base_name):
    """Generate narrative using LLM."""
    headers = {
        'Authorization': f'Bearer {AI_PROXY}',
        'Content-Type': 'application/json'
    }
    prompt = f"Provide a detailed analysis based on the following data summary: {analysis}"
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = httpx.post(API_URL, headers=headers, json=data, timeout=30.0)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return "Narrative generation failed due to an error."

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Analyze datasets and generate insights.")
    parser.add_argument("file_path", nargs="?", default=None, help="Path to the dataset CSV file.")
    parser.add_argument("-o", "--output_dir", default="output", help="Directory to save outputs.")
    args = parser.parse_args()

    # If file_path is not provided as an argument, prompt the user for the file path
    if not args.file_path:
        args.file_path = input("Please enter the file path to the dataset CSV file: ")

    # Extract the base name from the file path (without extension)
    base_name = os.path.splitext(os.path.basename(args.file_path))[0]

    # Ensure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Load data
    df = load_data(args.file_path)

    # Analyze data
    analysis = analyze_data(df)

    # Visualize data (generate 3 PNGs, including heatmap)
    visualize_data(df, args.output_dir, base_name)

    # Generate narrative
    narrative = generate_narrative(analysis, base_name)

    # Save narrative with dynamic name
    with open(os.path.join(args.output_dir, f'{base_name}_README.md'), 'w') as f:
        f.write(narrative)

if __name__ == "__main__":
    main()


