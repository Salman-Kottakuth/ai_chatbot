import pandas as pd
import matplotlib.pyplot as plt
from langchain_core.tools import tool

# DataFrame
df = pd.DataFrame({
    "country": [
        "United States",
        "United Kingdom",
        "France",
        "Germany",
        "Italy",
        "Spain",
        "Canada",
        "Australia",
        "Japan",
        "China",
    ],
    "gdp": [
        19294482071552,
        2891615567872,
        2411255037952,
        3435817336832,
        1745433788416,
        1181205135360,
        1607402389504,
        1490967855104,
        4380756541440,
        14631844184064,
    ],
    "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.4, 7.23, 7.22, 5.87, 5.12],
})

# Function to plot bar plot or pie chart based on chart_type parameter
def plot_gdp_by_country(df, chart_type="bar"):
    if chart_type == "bar":
        # Bar plot
        plt.figure(figsize=(12, 6))
        plt.bar(df["country"], df["gdp"], color='skyblue')
        plt.xticks(rotation=45, ha='right')
        plt.title("GDP by Country", fontsize=16)
        plt.xlabel("Country", fontsize=14)
        plt.ylabel("GDP (in Trillions USD)", fontsize=14)
        plt.tight_layout()
        plt.show()
    
    elif chart_type == "pie":
        # Pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(df["gdp"], labels=df["country"], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title("GDP Distribution by Country", fontsize=16)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()
    
    else:
        print("Invalid chart_type. Please choose 'bar' or 'pie'.")

# Tool function for Graph Plotting
@tool
def graph_plot_tool(chart_type: str) -> str:
    """
    Plots a graph (bar or pie) based on GDP by country.

    Args:
        chart_type (str): Type of chart to plot - 'bar' or 'pie'.
    
    Returns:
        str: Confirmation message that the chart has been plotted.
    """
    try:
        # Call the plot function with the user's chosen chart type
        plot_gdp_by_country(df, chart_type)
        return f"Graph plotted successfully as a {chart_type} chart."
    except Exception as e:
        return f"Error while plotting the graph: {str(e)}"
