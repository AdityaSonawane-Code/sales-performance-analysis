# \# Sales Performance Analysis

# 

# An end-to-end data analytics project using Python, Pandas, data visualization, and Power BI to analyze sales performance, profitability, product categories, and regional trends.

# 

# \## Project Overview

# 

# The objective of this project is to transform raw Superstore sales data into useful business insights through data cleaning, exploratory data analysis (EDA), visualization, and an interactive Power BI dashboard.

# 

# \## Business Objectives

# 

# \- Measure overall sales and profitability.

# \- Identify high-performing and low-performing product categories.

# \- Compare sales and profit across regions.

# \- Analyze monthly sales patterns.

# \- Investigate the relationship between discounts and profit.

# \- Provide data-driven business recommendations.

# 

# \## Tools and Technologies

# 

# \- \*\*Python\*\* — analysis and data processing

# \- \*\*Pandas and NumPy\*\* — data cleaning and calculations

# \- \*\*Matplotlib and Seaborn\*\* — data visualization

# \- \*\*Power BI Desktop\*\* — interactive dashboard

# \- \*\*Git and GitHub\*\* — version control and project hosting

# 

# \## Project Structure

# 

# ```text

# sales-performance-analysis/

# ├── data/

# │   ├── raw/

# │   └── processed/

# ├── src/

# │   ├── clean\_data.py

# │   ├── inspect\_data.py

# │   └── eda\_analysis.py

# ├── reports/

# │   ├── visualizations/

# │   ├── Sales\_Performance\_Dashboard.pbix

# │   ├── business\_metrics.csv

# │   ├── category\_analysis.csv

# │   ├── region\_analysis.csv

# │   ├── monthly\_sales\_trend.csv

# │   └── other analysis reports

# ├── screenshots/

# ├── requirements.txt

# └── README.md

# ```

# 

# \## Data Cleaning and Preparation

# 

# The workflow includes inspecting dataset structure and data types, checking missing values, identifying exact duplicate records, examining numerical outliers, and preparing the processed dataset for analysis.

# 

# Potential outliers are investigated rather than automatically removed, since unusually large or small transactions may be valid business records.

# 

# \## Key Performance Indicators

# 

# | Metric | Result |

# |---|---:|

# | Total Sales | 2,326,534.35 |

# | Total Profit | 292,296.81 |

# | Unique Orders | 5,111 |

# | Total Quantity | 38,654 |

# | Average Order Value | 455.20 |

# | Overall Profit Margin | 12.56% |

# 

# \*Values are taken from the generated business metrics report.\*

# 

# \## Key Business Insights

# 

# \### 1. Category Performance

# 

# Technology recorded the highest sales, at approximately 839,893, and the highest profit, at approximately 146,543.

# 

# Office Supplies generated approximately 126,023 in profit. Furniture generated approximately 754,748 in sales but only 19,730 in profit, corresponding to a profit margin of about 2.61%.

# 

# \*\*Interpretation:\*\* Furniture deserves further investigation to identify whether particular products, discounts, or costs are reducing profitability.

# 

# \### 2. Regional Performance

# 

# The West region recorded the highest sales, at approximately 739,814, and the highest profit, at approximately 110,799.

# 

# The East generated approximately 691,828 in sales and 94,883 in profit. Central generated approximately 503,171 in sales and 39,865 in profit, while South generated approximately 391,722 in sales and 46,749 in profit.

# 

# \*\*Interpretation:\*\* Regional sales volume alone does not explain profitability. Product mix, discounting, and costs should also be considered.

# 

# \### 3. Discounting and Profitability

# 

# The exploratory analysis found a negative correlation of approximately -0.219 between discount and profit.

# 

# \*\*Interpretation:\*\* Higher discounts are associated with lower profit in this dataset, but correlation alone does not establish causation. Product and transaction-level analysis is needed before changing discount policies.

# 

# \### 4. Monthly Sales Trends

# 

# Monthly sales were grouped to support trend analysis and business planning.

# 

# \*\*Data-quality note:\*\* The generated monthly report contains dates through December 2026. These dates should be validated against the source dataset before drawing conclusions about future periods or seasonal patterns.

# 

# \## Business Recommendations

# 

# 1\. \*\*Review Furniture profitability:\*\* Analyze profit by product and discount level to identify low-margin items and opportunities to improve costs or pricing.

# 2\. \*\*Protect profitable sales:\*\* Investigate the products and transactions contributing to Technology's strong profit performance.

# 3\. \*\*Improve regional decisions:\*\* Compare product mix, discount levels, and profitability across Central and South rather than focusing on sales volume alone.

# 4\. \*\*Evaluate discount policies:\*\* Assess whether discounts improve sales enough to justify their impact on profit.

# 5\. \*\*Use validated monthly trends:\*\* Once date quality is confirmed, use seasonal patterns to inform inventory planning and promotions.

# 

# These recommendations are proposed actions based on descriptive analysis. Their financial impact should be measured before implementation.

# 

# \## Visualizations

# 

# The `reports/visualizations/` directory contains:

# 

# \- Sales by category

# \- Profit by category

# \- Monthly sales trend

# \- Sales by region

# \- Discount versus profit

# \- Correlation heatmap

# \- Profit distribution

# 

# \## Power BI Dashboard

# 

# The dashboard includes:

# 

# \- KPI cards for sales, profit, and order count

# \- Sales and profit by category

# \- Sales by region

# \- Monthly sales trends

# \- Interactive slicers for region, category, and order date

# 

# The dashboard enables users to explore performance across different business dimensions.

# 

# \## How to Run the Python Analysis

# 

# 1\. Install Python.

# 2\. Clone or download this repository.

# 3\. Install the required packages:

# 

# &#x20;  `pip install -r requirements.txt`

# 

# 4\. Run the analysis script from the project root:

# 

# &#x20;  `python src/eda\_analysis.py`

# 

# 5\. Open `reports/Sales\_Performance\_Dashboard.pbix` in Power BI Desktop to explore the dashboard.

# 

# \## Conclusion

# 

# This project demonstrates an end-to-end data analytics workflow, from data inspection and cleaning to exploratory analysis, visualization, and business recommendations.

# 

# It highlights how sales, profit, category performance, regional differences, and discounting can be examined to support better-informed business decisions.

# 

# \## Author

# 

# Aditya Sonawane

# 

# GitHub: https://github.com/AdityaSonawane-Code



