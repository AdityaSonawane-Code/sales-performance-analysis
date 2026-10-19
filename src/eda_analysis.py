
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore", category=FutureWarning)

# ============================================================
#  SALES PERFORMANCE ANALYSIS - COMPLETE EDA
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_FILE = (
    BASE_DIR / "data" / "processed" / "superstore_cleaned.csv"
)

REPORT_DIR = BASE_DIR / "reports"
CHART_DIR = REPORT_DIR / "visualizations"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.bbox"] = "tight"


def save_chart(filename):
    """Save the current chart and close the figure."""
    output_path = CHART_DIR / filename
    plt.tight_layout()
    plt.savefig(output_path, dpi=160, facecolor="white")
    plt.close()
    print(f"Saved chart: {output_path}")


def main():
    print("=" * 65)
    print("       SALES PERFORMANCE ANALYSIS - EDA")
    print("=" * 65)

    # --------------------------------------------------------
    # 1. LOAD DATASET
    # --------------------------------------------------------

    print("\n1. DATASET INSPECTION")

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{DATA_FILE}\n"
            "Check that the CSV file exists at this location."
        )

    df = pd.read_csv(DATA_FILE)

    # Normalize column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )

    # Parse dates safely
    for col in ["order_date", "ship_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    print("Dataset:", DATA_FILE)
    print("Dataset shape:", df.shape)
    print("Number of rows:", len(df))
    print("Number of columns:", len(df.columns))

    print("\nFirst 5 records:")
    print(df.head().to_string(index=False))

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nColumn data types:")
    print(df.dtypes.to_string())

    # --------------------------------------------------------
    # 2. DATA QUALITY CHECKS
    # --------------------------------------------------------

    print("\n2. DATA QUALITY CHECKS")

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    print("\nMissing values by column:")
    if missing.empty:
        print("No missing values found.")
    else:
        print(missing.to_string())

    missing_report = pd.DataFrame({
        "column": df.columns,
        "missing_count": [int(df[col].isnull().sum()) for col in df.columns],
        "missing_percentage": [
            round(df[col].isnull().mean() * 100, 2)
            for col in df.columns
        ]
    })
    missing_report.to_csv(
        REPORT_DIR / "missing_values_report.csv", index=False
    )

    duplicate_count = int(df.duplicated().sum())
    print("\nExact duplicate rows:", duplicate_count)

    # Remove only exact duplicate rows
    if duplicate_count > 0:
        df = df.drop_duplicates().copy()
        print("Removed exact duplicate rows.")
    else:
        print("No duplicate rows needed removal.")

    print("Shape after duplicate check:", df.shape)

    # Report invalid numeric values; do not silently change them
    numeric_cols = [
        col for col in ["sales", "quantity", "discount", "profit"]
        if col in df.columns
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    print("\nMissing values after numeric conversion:")
    print(df.isnull().sum().to_string())

    # Save the cleaned version.
    # Missing values are retained for review rather than filled blindly.
    df.to_csv(
        BASE_DIR / "data" / "processed" / "superstore_eda_cleaned.csv",
        index=False
    )

    # --------------------------------------------------------
    # 3. DESCRIPTIVE STATISTICS
    # --------------------------------------------------------

    print("\n3. DESCRIPTIVE STATISTICS")

    if numeric_cols:
        descriptive_stats = df[numeric_cols].describe().round(2)
        print(descriptive_stats.to_string())
        descriptive_stats.to_csv(
            REPORT_DIR / "descriptive_statistics.csv"
        )
    else:
        descriptive_stats = pd.DataFrame()
        print("No expected numeric columns found.")

    # --------------------------------------------------------
    # 4. KEY BUSINESS METRICS
    # --------------------------------------------------------

    print("\n4. KEY BUSINESS METRICS")

    total_sales = (
        float(df["sales"].sum())
        if "sales" in df.columns else 0.0
    )
    total_profit = (
        float(df["profit"].sum())
        if "profit" in df.columns else 0.0
    )
    total_orders = (
        int(df["order_id"].nunique())
        if "order_id" in df.columns else 0
    )
    total_quantity = (
        int(df["quantity"].sum())
        if "quantity" in df.columns else 0
    )
    average_order_value = (
        total_sales / total_orders if total_orders else 0.0
    )
    profit_margin = (
        total_profit / total_sales * 100 if total_sales else 0.0
    )

    print(f"Total Sales:          {total_sales:,.2f}")
    print(f"Total Profit:         {total_profit:,.2f}")
    print(f"Unique Orders:        {total_orders:,}")
    print(f"Total Quantity:       {total_quantity:,}")
    print(f"Average Order Value:  {average_order_value:,.2f}")
    print(f"Profit Margin:        {profit_margin:.2f}%")

    metrics = {
        "metric": [
            "Total Sales",
            "Total Profit",
            "Unique Orders",
            "Total Quantity",
            "Average Order Value",
            "Profit Margin (%)"
        ],
        "value": [
            total_sales,
            total_profit,
            total_orders,
            total_quantity,
            average_order_value,
            profit_margin
        ]
    }

    pd.DataFrame(metrics).to_csv(
        REPORT_DIR / "business_metrics.csv", index=False
    )

    # --------------------------------------------------------
    # 5. CATEGORY ANALYSIS
    # --------------------------------------------------------

    category_summary = pd.DataFrame()

    if "category" in df.columns and "sales" in df.columns:
        print("\n5. SALES AND PROFIT BY CATEGORY")

        agg_dict = {"sales": "sum"}
        if "profit" in df.columns:
            agg_dict["profit"] = "sum"

        category_summary = (
            df.groupby("category", dropna=False)
            .agg(agg_dict)
            .sort_values("sales", ascending=False)
        )

        print(category_summary.round(2).to_string())
        category_summary.to_csv(
            REPORT_DIR / "category_analysis.csv"
        )

    # --------------------------------------------------------
    # 6. REGIONAL ANALYSIS
    # --------------------------------------------------------

    region_summary = pd.DataFrame()

    if "region" in df.columns and "sales" in df.columns:
        print("\n6. SALES AND PROFIT BY REGION")

        agg_dict = {"sales": "sum"}
        if "profit" in df.columns:
            agg_dict["profit"] = "sum"

        region_summary = (
            df.groupby("region", dropna=False)
            .agg(agg_dict)
            .sort_values("sales", ascending=False)
        )

        print(region_summary.round(2).to_string())
        region_summary.to_csv(
            REPORT_DIR / "region_analysis.csv"
        )

    # --------------------------------------------------------
    # 7. MONTHLY SALES TREND
    # --------------------------------------------------------

    monthly_summary = pd.DataFrame()

    if "order_date" in df.columns and "sales" in df.columns:
        print("\n7. MONTHLY SALES TREND")

        monthly_df = df.dropna(subset=["order_date"]).copy()
        monthly_df["order_month"] = (
            monthly_df["order_date"].dt.to_period("M").astype(str)
        )

        monthly_summary = (
            monthly_df.groupby("order_month")["sales"]
            .sum()
            .sort_index()
        )

        print(monthly_summary.head(12).round(2).to_string())
        monthly_summary.to_csv(
            REPORT_DIR / "monthly_sales_trend.csv"
        )

    # --------------------------------------------------------
    # 8. CORRELATION ANALYSIS
    # --------------------------------------------------------

    print("\n8. CORRELATION ANALYSIS")

    valid_numeric_cols = [
        col for col in numeric_cols
        if df[col].notna().sum() > 1
        and df[col].nunique(dropna=True) > 1
    ]

    if len(valid_numeric_cols) >= 2:
        correlation = df[valid_numeric_cols].corr()
        print(correlation.round(3).to_string())
        correlation.to_csv(
            REPORT_DIR / "correlation_matrix.csv"
        )
    else:
        correlation = pd.DataFrame()
        print("Not enough numeric columns for correlation analysis.")

    # --------------------------------------------------------
    # 9. OUTLIER ANALYSIS USING IQR
    # --------------------------------------------------------

    print("\n9. OUTLIER ANALYSIS (IQR METHOD)")

    outlier_rows = []

    for col in numeric_cols:
        series = df[col].dropna()

        if series.empty:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        count = int(((series < lower) | (series > upper)).sum())

        outlier_rows.append({
            "column": col,
            "q1": q1,
            "q3": q3,
            "lower_bound": lower,
            "upper_bound": upper,
            "outlier_count": count,
            "outlier_percentage": round(
                count / len(series) * 100, 2
            )
        })

        print(
            f"{col}: {count} potential outliers "
            f"({count / len(series) * 100:.2f}%)"
        )

    outlier_df = pd.DataFrame(outlier_rows)
    outlier_df.to_csv(
        REPORT_DIR / "outlier_analysis.csv", index=False
    )

    # --------------------------------------------------------
    # 10. VISUALIZATION 1 - SALES BY CATEGORY
    # --------------------------------------------------------

    print("\n10. GENERATING VISUALIZATIONS")

    if not category_summary.empty:
        plt.figure(figsize=(9, 6))

        category_summary["sales"].sort_values().plot(
            kind="barh", color=sns.color_palette("deep")[0]
        )

        plt.title("Total Sales by Product Category",
                  fontsize=15, fontweight="bold")
        plt.xlabel("Total Sales")
        plt.ylabel("Product Category")
        save_chart("01_sales_by_category.png")

    # --------------------------------------------------------
    # 11. VISUALIZATION 2 - PROFIT BY CATEGORY
    # --------------------------------------------------------

    if (
        not category_summary.empty
        and "profit" in category_summary.columns
    ):
        plt.figure(figsize=(9, 6))

        category_summary["profit"].sort_values().plot(
            kind="barh", color=sns.color_palette("deep")[2]
        )

        plt.title("Total Profit by Product Category",
                  fontsize=15, fontweight="bold")
        plt.xlabel("Total Profit")
        plt.ylabel("Product Category")
        plt.axvline(0, linewidth=0.8, color="black")
        save_chart("02_profit_by_category.png")

    # --------------------------------------------------------
    # 12. VISUALIZATION 3 - MONTHLY SALES TREND
    # --------------------------------------------------------

    if not monthly_summary.empty:
        plt.figure(figsize=(12, 6))

        plt.plot(
            monthly_summary.index,
            monthly_summary.values,
            marker="o",
            linewidth=2
        )

        plt.title("Monthly Sales Trend",
                  fontsize=15, fontweight="bold")
        plt.xlabel("Order Month")
        plt.ylabel("Total Sales")
        plt.xticks(rotation=60, ha="right")
        save_chart("03_monthly_sales_trend.png")

    # --------------------------------------------------------
    # 13. VISUALIZATION 4 - SALES BY REGION
    # --------------------------------------------------------

    if not region_summary.empty:
        plt.figure(figsize=(9, 6))

        region_summary["sales"].sort_values().plot(
            kind="bar", color=sns.color_palette("deep")
        )

        plt.title("Total Sales by Region",
                  fontsize=15, fontweight="bold")
        plt.xlabel("Region")
        plt.ylabel("Total Sales")
        plt.xticks(rotation=0)
        save_chart("04_sales_by_region.png")

    # --------------------------------------------------------
    # 14. VISUALIZATION 5 - DISCOUNT VS PROFIT
    # --------------------------------------------------------

    if {"discount", "profit"}.issubset(df.columns):
        scatter_df = df[["discount", "profit"]].dropna()

        if not scatter_df.empty:
            plt.figure(figsize=(10, 6))

            sns.scatterplot(
                data=scatter_df,
                x="discount",
                y="profit",
                alpha=0.45,
                s=35
            )

            plt.title("Relationship Between Discount and Profit",
                      fontsize=15, fontweight="bold")
            plt.xlabel("Discount")
            plt.ylabel("Profit")
            plt.axhline(0, color="red", linestyle="--", linewidth=1)
            save_chart("05_discount_vs_profit.png")

    # --------------------------------------------------------
    # 15. VISUALIZATION 6 - CORRELATION HEATMAP
    # --------------------------------------------------------

    if not correlation.empty:
        plt.figure(figsize=(8, 6))

        sns.heatmap(
            correlation,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            linewidths=0.5
        )

        plt.title("Correlation Heatmap of Numerical Variables",
                  fontsize=14, fontweight="bold")
        save_chart("06_correlation_heatmap.png")

    # --------------------------------------------------------
    # 16. VISUALIZATION 7 - PROFIT DISTRIBUTION
    # --------------------------------------------------------

    if "profit" in df.columns:
        profit_values = df["profit"].dropna()

        if not profit_values.empty:
            plt.figure(figsize=(10, 6))

            sns.histplot(
                profit_values,
                bins=50,
                kde=True
            )

            plt.title("Distribution of Sales Profit",
                      fontsize=15, fontweight="bold")
            plt.xlabel("Profit")
            plt.ylabel("Number of Records")
            save_chart("07_profit_distribution.png")

    # --------------------------------------------------------
    # 17. AUTOMATIC BUSINESS INSIGHTS
    # --------------------------------------------------------

    print("\n11. PRELIMINARY BUSINESS INSIGHTS")

    insights = []

    if not category_summary.empty:
        top_category = category_summary["sales"].idxmax()
        top_sales = category_summary["sales"].max()

        insights.append(
            f"Highest-sales category: {top_category} "
            f"({top_sales:,.2f} in sales)."
        )

        if "profit" in category_summary.columns:
            top_profit_category = category_summary["profit"].idxmax()
            lowest_profit_category = category_summary["profit"].idxmin()

            insights.append(
                f"Highest-profit category: {top_profit_category}."
            )
            insights.append(
                f"Lowest-profit category: {lowest_profit_category}; "
                "review its costs, discounts and product mix."
            )

    if not region_summary.empty:
        top_region = region_summary["sales"].idxmax()
        insights.append(
            f"Highest-sales region: {top_region}."
        )

    if (
        not correlation.empty
        and "discount" in correlation.columns
        and "profit" in correlation.columns
    ):
        discount_profit_corr = correlation.loc["discount", "profit"]

        insights.append(
            f"Discount-profit correlation: "
            f"{discount_profit_corr:.3f}. "
            "Correlation does not by itself prove causation."
        )

    if not monthly_summary.empty:
        best_month = monthly_summary.idxmax()
        insights.append(
            f"Highest-sales month: {best_month} "
            f"({monthly_summary.max():,.2f})."
        )

    if insights:
        for i, insight in enumerate(insights, start=1):
            print(f"{i}. {insight}")
    else:
        print("Insufficient data to generate category or region insights.")

    # --------------------------------------------------------
    # 18. SAVE EDA SUMMARY REPORT
    # --------------------------------------------------------

    report_file = REPORT_DIR / "eda_summary.txt"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("SALES PERFORMANCE ANALYSIS - EDA SUMMARY\n")
        f.write("=" * 55 + "\n\n")

        f.write(f"Dataset: {DATA_FILE.name}\n")
        f.write(f"Final dataset shape: {df.shape}\n")
        f.write(f"Exact duplicate rows found: {duplicate_count}\n")
        f.write(f"Total sales: {total_sales:.2f}\n")
        f.write(f"Total profit: {total_profit:.2f}\n")
        f.write(f"Unique orders: {total_orders}\n")
        f.write(f"Total quantity: {total_quantity}\n")
        f.write(f"Average order value: {average_order_value:.2f}\n")
        f.write(f"Profit margin: {profit_margin:.2f}%\n\n")

        f.write("Missing values before duplicate removal:\n")
        if missing.empty:
            f.write("No missing values found.\n")
        else:
            f.write(missing.to_string() + "\n")

        f.write("\nDescriptive statistics:\n")
        f.write(
            df[numeric_cols].describe().round(2).to_string()
            if numeric_cols else "No numeric columns."
        )

        f.write("\n\nCorrelation matrix:\n")
        f.write(
            correlation.round(3).to_string()
            if not correlation.empty else "Not available."
        )

        f.write("\n\nPotential outliers:\n")
        if not outlier_df.empty:
            f.write(outlier_df.to_string(index=False))
        else:
            f.write("Not available.")

        f.write("\n\nPreliminary business insights:\n")
        for i, insight in enumerate(insights, start=1):
            f.write(f"{i}. {insight}\n")

        f.write("\n\nVisualizations saved:\n")
        for chart in sorted(CHART_DIR.glob("*.png")):
            f.write(f"{chart.name}\n")

    # --------------------------------------------------------
    # 19. FINAL STATUS
    # --------------------------------------------------------

    chart_count = len(list(CHART_DIR.glob("*.png")))

    print("\n" + "=" * 65)
    print("EDA COMPLETED SUCCESSFULLY")
    print("=" * 65)
    print("Cleaned dataset:")
    print(BASE_DIR / "data" / "processed" / "superstore_eda_cleaned.csv")
    print("\nEDA summary:")
    print(report_file)
    print("\nReports folder:")
    print(REPORT_DIR)
    print("\nCharts folder:")
    print(CHART_DIR)
    print(f"\nCharts generated: {chart_count}")
    print("\nNext step: Review findings and build the Power BI dashboard.")


if __name__ == "__main__":
    main()
