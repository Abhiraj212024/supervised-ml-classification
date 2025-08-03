import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from scipy import stats

#Load dataset
df = pd.read_csv('./data/delhi_air_quality.csv')



df["Year"] = df["Year"].astype(str)
df["Month"] = df["Month"].astype(str)
df["Date"] = df["Date"].astype(str)


df["Date"] = df["Year"] + "-" + df["Month"] + "-" + df["Date"]

df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")

df.drop(columns=["Year", "Month"], inplace=True, axis=1)
df["CO"] = df["CO"].apply(lambda x: x/1000)

lockdown_data = df[(df["Date"] >= "2020-3-24") & (df["Date"] <= "2022-12-31")]
non_lockdown_data = df[(df["Date"] < "2020-3-24") | (df["Date"] > "2022-12-31")]

metrics = df.columns[3:].tolist()

fig, axes = plt.subplots(nrows=6, ncols=2, figsize=(20, 20))

for i in range(6):
    sns.lineplot(data=lockdown_data, x="Date", y=metrics[i], ax=axes[i, 0])
    axes[i, 0].set_title(f"{metrics[i]} during lockdown")
    axes[i, 0].set_xlabel("Date")
    axes[i, 0].set_ylabel(metrics[i])

    sns.lineplot(data=non_lockdown_data, x="Date", y=metrics[i], ax=axes[i, 1])
    axes[i, 1].set_title(f"{metrics[i]} before and after lockdown")
    axes[i, 1].set_xlabel("Date")
    axes[i, 1].set_ylabel(metrics[i])


plt.savefig("./figures/air_quality_lockdown.png")

#Perform Hypothesis Testing with H0 of same population mean for each metric

result = {}

for metric in metrics:
    lockdown_values = lockdown_data[metric]
    non_lockdown_values = non_lockdown_data[metric]

    t_stat, p_value = stats.ttest_ind(lockdown_values, non_lockdown_values, equal_var=False)
    result[metric] = {"t_statistic" : round(float(t_stat), 4), "p_value" : round(float(p_value), 4), "significant" : p_value < 0.05}
    if( p_value < 0.05):
        if( t_stat > 0):
            print(f"{metric} is significantly higher during lockdown")
        else:
            print(f"{metric} is significantly lower during lockdown")

    else:
        print(f"{metric} is not significantly different during lockdown")

y1 = lockdown_data["AQI"]
y2 = non_lockdown_data["AQI"]
x1 = lockdown_data["Date"]
x2 = non_lockdown_data["Date"]
fig1, axes1 = plt.subplots(figsize=(20, 10), nrows=1, ncols=1)

axes1.plot(x1, y1, label="Lockdown AQI", color="blue")
axes1.plot(x2, y2, label="Non-lockdown AQI", color="red")

print(y1.mean(), y2.mean())
print(y1.std(), y2.std())
print("Hello World!")