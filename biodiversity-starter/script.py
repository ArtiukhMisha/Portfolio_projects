import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
from itertools import chain
import string


def remove_punctuations(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, "")
    return text


"""
- What is the distribution of conservation status for species?
- Are certain types of species more likely to be endangered?
- Are the differences between species and their conservation status significant?
- Which animal is most prevalent and what is their distribution amongst parks?
"""

species_data = pd.read_csv("../biodiversity-starter/species_info.csv", encoding="utf-8")
obs_data = pd.read_csv("../biodiversity-starter/observations.csv", encoding="utf-8")

# explore dfs
print(species_data.head(10))
print(obs_data.head(10))

species_data.info()
species_data.describe()
species_data.columns
species_data.conservation_status.unique()

obs_data.info()
obs_data[["scientific_name", "park_name"]].describe()
obs_data["observations"].sum()
obs_data.columns

species_data.groupby("category").count()
species_data.conservation_status.fillna("No Intervention", inplace=True)
species_data.groupby("conservation_status").count()
"""
- What is the distribution of conservation status for species?
"""
cat_status = (
    species_data[species_data.conservation_status != "No Intervention"]
    .groupby(["conservation_status", "category"])["scientific_name"]
    .count()
    .unstack()
)
cat_status.sum().sum()


ax = cat_status.plot(kind="bar", stacked=True, figsize=(8, 6))
ax.set_xlabel("Conservation Status")
ax.set_ylabel("Number of Species")
plt.show()
plt.clf()

"""
- Are certain types of species more likely to be endangered?
"""
palette = sns.color_palette("colorblind6")
endanger = (
    species_data[species_data.conservation_status == "Endangered"]
    .groupby(["category"])["scientific_name"]
    .count()
)
ax = endanger.plot(kind="bar", figsize=(8, 6), rot=15, color=palette[: len(endanger)])
ax.set_xlabel("Conservation Status")
ax.set_ylabel("Number of Species")
plt.show()
plt.clf()

species_data["is_protected"] = species_data.conservation_status != "No Intervention"

protected = (
    species_data.groupby(["category", "is_protected"])
    .scientific_name.nunique()
    .reset_index()
    .pivot(columns="is_protected", index="category", values="scientific_name")
    .reset_index()
)
protected.columns = ["category", "not_protected", "protected"]
protected["persentage"] = (
    protected.protected / (protected.protected + protected.not_protected) * 100
)

ax = sns.barplot(data=protected, x="category", y="persentage", hue="category")
ax.set_xticklabels(protected.category, rotation=20)
ax.set_ylabel("Persentage of Protected species")
plt.show()
plt.clf()
# _________________________chi-test
"""
- Are the differences between species and their conservation status significant?
"""
# bird-mammal
contingency1 = [[30, 146], [75, 413]]
chi2_contingency(contingency1)
"""
Chi2ContingencyResult(statistic=np.float64(0.1617014831654557), 
pvalue=np.float64(0.6875948096661336), dof=1,xxxx
expected_freq=array([[ 27.8313253, 148.1686747],
       [ 77.1686747, 410.8313253]]))"""
# fish-mamml
contingency1 = [[30, 146], [11, 115]]
chi2_contingency(contingency1)
"""Chi2ContingencyResult(statistic=np.float64(3.647651024981415), 
pvalue=np.float64(0.0561483484489001), dof=1, 
expected_freq=array([[ 23.89403974, 152.10596026],
                    [ 17.10596026, 108.89403974]]))
       """

"""
- Which animal is most prevalent and what is their distribution amongst parks?
"""
species_data.category.unique()
animal_names = (
    species_data[species_data.category.apply(lambda x: "Plant" not in x)]
    .common_names.apply(remove_punctuations)
    .str.split()
    .tolist()
)

no_copies = []
for item in animal_names:
    item = list(dict.fromkeys(item))
    no_copies.append(item)
no_copies

animal_names = list(
    chain.from_iterable(i if isinstance(i, list) else [i] for i in no_copies)
)

words_counted = {}

for i in animal_names:
    words_counted[i] = words_counted.get(i, 0) + 1

pd.DataFrame.from_dict(
    words_counted, orient="index", columns=["Count"]
).reset_index().rename(columns={"index": "Word"}).sort_values(
    "Count", ascending=False
).head()

species_data["is_warbler"] = species_data.common_names.str.contains(
    r"\bWarbler\b", regex=True
)

science_names = dict(
    zip(
        species_data[species_data.is_warbler].common_names,
        species_data[species_data.is_warbler].scientific_name,
    )
)

warbler_obs = obs_data.merge(species_data[species_data.is_warbler])
df = warbler_obs.groupby("park_name").observations.sum().reset_index()

sns.barplot(data=df, x="park_name", y="observations", hue="park_name")
plt.xticks(rotation=15)

obs_by_park = (
    warbler_obs.groupby(["park_name", "is_protected"]).observations.sum().reset_index()
)

sns.barplot(
    x=obs_by_park.park_name, y=obs_by_park.observations, hue=obs_by_park.is_protected
)
plt.xticks(rotation=15)
plt.xlabel("National Parks")
plt.ylabel("Number of Observations")
plt.title("Observations of Warbler per Week")
plt.show()

"""## Conclusions

The project was able to make several data visualizations and inferences about the various species in four of the National Parks that comprised this data set.

This project was also able to answer some of the questions first posed in the beginning:

- What is the distribution of conservation status for species?
    - The vast majority of species were not part of conservation.(5,633 vs 191)
- Are certain types of species more likely to be endangered?
    - Mammals and Birds had the highest percentage of being in protection.
- Are the differences between species and their conservation status significant?
    - While mammals and Birds did not have significant difference in conservation percentage, mammals and fish exhibited a statistically significant difference.
- Which animal is most prevalent and what is their distribution amongst parks?
    - the study found that warblers occurred the most number of times and they were most likely to be found in Yellowstone National Park(it seems to be the bigest park)
    """
