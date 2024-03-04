import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

day_df = pd.read_csv("https://raw.githubusercontent.com/fadhalfaiz/bikesharing/main/day.csv")

day_df.season.replace(1, "springer", inplace=True)
day_df.season.replace(2, "summer", inplace=True)
day_df.season.replace(3, "fall", inplace=True)
day_df.season.replace(4, "winter", inplace=True)
day_df["atemp"] = day_df["atemp"] * 41
day_df["temp"] = day_df["temp"] * 50
day_df["hum"] = day_df["hum"] * 100
day_df["windspeed"] = day_df["windspeed"] * 67

datetime_columns = ["dteday"]
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

day_df.workingday.replace(1, "workingday", inplace=True)
day_df.workingday.replace(0, "holiday", inplace=True)
day_df.mnth.replace(1, "January", inplace=True)
day_df.mnth.replace(2, "February", inplace=True)
day_df.mnth.replace(3, "March", inplace=True)
day_df.mnth.replace(4, "April", inplace=True)
day_df.mnth.replace(5, "May", inplace=True)
day_df.mnth.replace(6, "June", inplace=True)
day_df.mnth.replace(7, "July", inplace=True)
day_df.mnth.replace(8, "August", inplace=True)
day_df.mnth.replace(9, "September", inplace=True)
day_df.mnth.replace(10, "October", inplace=True)
day_df.mnth.replace(11, "November", inplace=True)
day_df.mnth.replace(12, "Desember", inplace=True)

st.header('Registered Dashboard')

monthly_registered_df = day_df.resample(rule='M', on='dteday').agg({
    "registered": "sum"
})
monthly_registered_df.index = monthly_registered_df.index.strftime('%B %Y')
monthly_registered_df = monthly_registered_df.reset_index()

fig, axes = plt.subplots(2, 1, figsize=(15, 15), gridspec_kw={'hspace': 0.5})  # Adding space between subplots

# Plot 1: Line plot
ax1 = axes[0]
ax1.plot(monthly_registered_df["dteday"], monthly_registered_df["registered"], marker='o', linewidth=2, color="#72BCD4") 
ax1.set_title("Number of Registered per Month (2011-2012)", loc="center", fontsize=20) 
ax1.set_xticklabels(monthly_registered_df["dteday"], fontsize=10, rotation=45) 
ax1.set_yticklabels(monthly_registered_df["registered"], fontsize=10) 

# Plot 2: Bar plot
byseason_df = day_df.groupby(by="workingday").registered.sum().reset_index()
ax2 = axes[1]
colors = ["#72BCD4", "#D3D3D3"]
sns.barplot(
    y="registered", 
    x="workingday",
    data=byseason_df.sort_values(by="registered", ascending=False),
    palette=colors,
    ax=ax2
)
ax2.set_title("Number of Registered by Working Day", loc="center", fontsize=20)
ax2.set_ylabel(None)
ax2.set_xlabel(None)
ax2.tick_params(axis='x', labelsize=15)
ax2.tick_params(axis='y', labelsize=15)

plt.xticks(rotation=45)  # Rotate x ticks for the bar plot
st.pyplot(fig)