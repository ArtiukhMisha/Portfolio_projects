import numpy as np
import pandas as pd
import scipy.stats as st
import seaborn as sns
import matplotlib.pyplot as plt

country_data = pd.read_csv("../Life_Expectancy_and_GDP/data/all_data.csv")
print(country_data.head(15))
print(country_data.info())


country_data["Country"] = country_data["Country"].replace(
    "United States of America", "USA"
)
country_data = country_data.rename(
    {"Life expectancy at birth (years)": "LEABY"}, axis="columns"
)
median_gdp_by_country = country_data.groupby("Country")["GDP"].median().reset_index()


median_gdp = country_data["GDP"].median()
high_GDP_countries = median_gdp_by_country[median_gdp_by_country["GDP"] > median_gdp][
    "Country"
].to_list()
low_GDP_countries = median_gdp_by_country[median_gdp_by_country["GDP"] < median_gdp][
    "Country"
].to_list()

low_GDP_data = country_data[country_data["Country"].isin(low_GDP_countries)]
high_GDP_data = country_data[country_data["Country"].isin(high_GDP_countries)]

dfMeans = country_data.groupby("Country").mean().reset_index()
# ________________________________________________________________________________________________________________

plt.figure(figsize=(8, 6))
sns.barplot(x="LEABY", y="Country", data=dfMeans, palette="Set2")
plt.xlabel("Life expectancy at birth (years)")
plt.show()
plt.clf()

plt.figure(figsize=(8, 6))
sns.barplot(x="GDP", y="Country", data=dfMeans, palette="Set2")
plt.xlabel("GDP")
plt.show()
plt.clf()

# _________________________________________________________________________________________________
# GDP-YEAR in each country

sns.lineplot(
    data=high_GDP_data, x="Year", y="GDP", hue="Country", marker="o", palette="Set2"
)
plt.title("GDP by Country Over the Years (Low GDP Countries)", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("GDP (log scale)", fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", title="Country")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

sns.lineplot(
    data=low_GDP_data, x="Year", y="GDP", hue="Country", marker="o", palette="Set2"
)
plt.title("GDP by Country Over the Years (Low GDP Countries)", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("GDP (log scale)", fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", title="Country")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# ______________________________________________________________________________________________
# Life expentancy - GDP in each country

g = sns.FacetGrid(
    country_data, col="Country", col_wrap=3, hue="Country", sharex=False, sharey=False
)
g = (
    g.map(sns.lineplot, "LEABY", "GDP")
    .add_legend()
    .set_axis_labels("Life expectancy", "GDP in trillions")
)


g = sns.FacetGrid(
    country_data, col="Country", col_wrap=3, hue="Country", sharex=False, sharey=False
)
g = g.map(sns.lineplot, "Year", "LEABY").add_legend().set_axis_labels("Year", "LEABY")

plt.show()

sns.scatterplot(
    x=country_data.LEABY, y=country_data.GDP, hue=country_data.Country
).legend(loc="center left", bbox_to_anchor=(1, 0.5), ncol=1)
# ______________________________________________________________________________________________
# Closer look on Zimbabwe
zim_df = country_data[country_data["Country"] == "Zimbabwe"]


fig, axes = plt.subplots(1, 3, sharex=False, sharey=False, figsize=(25, 5))
axes[0] = sns.lineplot(ax=axes[0], data=zim_df, x="LEABY", y="GDP")
axes[0].set_title("Life expectancy by GDP")
axes[0].set_xlabel("Life expectancy")
axes[1] = sns.lineplot(ax=axes[1], data=zim_df, x="Year", y="LEABY")
axes[1].set_title("Life expectancy by Yea")
axes[1].set_xlabel("Year")
axes[2] = sns.lineplot(ax=axes[2], data=zim_df, x="Year", y="GDP")
axes[2].set_title("GDP by Year")
axes[2].set_xlabel("YEAR")
