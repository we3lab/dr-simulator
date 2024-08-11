#I'm importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point 

#I'm opening and reading my data file 
data = pd.read_csv('us_program_parameters.csv')

#Viewing the first 10 rows of the data
print(data.head(10))

# Printing the column names to check for discrepancies
print("Column names in the CSV file:")
print(data.columns)

# Printing the program, company, state, region, and season columns
columns_for_season_histogram = ['program', 'comp', 'state', 'region', 'season']
print(data[columns_for_season_histogram].head(10))

#Counting the number of programs for each region 
region_counts = data['region'].value_counts()
print("Number of programs for each region:")
print(region_counts)

# Counting the number of programs for each season
season_counts = data['season'].value_counts()
print("Number of programs for each season:")
print(season_counts)

# Counting the number of programs for each season in each region
region_season_counts = data.groupby(['region', 'season']).size().reset_index(name='counts')
print("Number of programs for each season in each region:")
print(region_season_counts)

#set font default to arial
plt.rcParams['font.family'] = 'Arial'

# Plotting the histogram of prgrams per season 
plt.figure(figsize=(5, 5))
season_counts.plot(kind='bar', color='#8c1515')
plt.title('Number of Programs per Season', fontweight='bold', fontsize=16)
plt.xlabel('Season', fontsize=14)
plt.ylabel('Number of Programs', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
#plt.show()


# Calculating the total number of programs in each region
region_totals = region_season_counts.groupby('region')['counts'].sum().reset_index(name='total_counts')

# Merging the total counts back to the region_season_counts
region_season_counts = region_season_counts.merge(region_totals, on='region')

# Calculating the percentage of each season within each region
region_season_counts['percentage'] = (region_season_counts['counts'] / region_season_counts['total_counts']) * 100

# Pivoting the data for plotting
pivot_data = region_season_counts.pivot(index='region', columns='season', values='percentage').fillna(0)

# Plotting the stacked bar chart
pivot_data.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='tab20')
plt.title('Percentage of Programs per Season in Each Region')
plt.xlabel('Region')
plt.ylabel('Percentage of Programs')
plt.legend(title='Season', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
#plt.show()

#Table for seasons per state 
# Clean the data
data['season'] = data['season'].str.strip().str.lower().str.replace(r'\s+', ' ', regex=True)
data['state'] = data['state'].str.strip().str.upper()  # Ensure state abbreviations are uppercase

# Filter the data for the seasons you are interested in, including 'year_round'
seasons_of_interest = ['summer', 'winter', 'spring', 'fall', 'year_round']
filtered_data = data[data['season'].isin(seasons_of_interest)]

# Group and count the number of programs per state for each season
program_counts = filtered_data.groupby(['state', 'season']).size().reset_index(name='program_count')

# Pivot the data to create a table format
pivot_table = program_counts.pivot(index='state', columns='season', values='program_count').fillna(0)

# Display the table
print(pivot_table)

# Count the number of states to ensure none are missing
unique_states = data['state'].nunique()
print(f"Total number of unique states: {unique_states}")

# Plot the data
pivot_table.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='tab20')
plt.title('Percentage of Programs per Season in Each Region')
plt.xlabel('Region')
plt.ylabel('Percentage of Programs')
plt.legend(title='Season', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
#plt.show()

#Duration based on season
# Group by season and calculate the average minimum and maximum duration
avg_min_duration_by_season = filtered_data.groupby('season')['min_dur'].mean().reset_index()
avg_max_duration_by_season = filtered_data.groupby('season')['max_dur'].mean().reset_index()

# Display the tables
print("Average Minimum Duration by Season:")
print(avg_min_duration_by_season)
print("\nAverage Maximum Duration by Season:")
print(avg_max_duration_by_season)

# Plot the data for average minimum duration
plt.figure(figsize=(10, 6))
plt.bar(avg_min_duration_by_season['season'].str.capitalize(), avg_min_duration_by_season['min_dur'], color='lightcoral')
plt.title('Average Minimum Duration of Events by Season')
plt.xlabel('Season')
plt.ylabel('Average Minimum Duration (hours)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Plot the data for average maximum duration
plt.figure(figsize=(10, 6))
plt.bar(avg_max_duration_by_season['season'].str.capitalize(), avg_max_duration_by_season['max_dur'], color='skyblue')
plt.title('Average Maximum Duration of Events by Season')
plt.xlabel('Season')
plt.ylabel('Average Maximum Duration (hours)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#Duration based on region 
# Group by region and calculate the average minimum and maximum duration
avg_min_duration_by_region = filtered_data.groupby('region')['min_dur'].mean().reset_index()
avg_max_duration_by_region = filtered_data.groupby('region')['max_dur'].mean().reset_index()

# Display the tables
print("Average Minimum Duration by Region:")
print(avg_min_duration_by_region)
print("\nAverage Maximum Duration by Region:")
print(avg_max_duration_by_region)

# Plot the data for average minimum duration
plt.figure(figsize=(10, 6))
plt.bar(avg_min_duration_by_region['region'], avg_min_duration_by_region['min_dur'], color='lightcoral')
plt.title('Average Minimum Duration of Events by Region')
plt.xlabel('Region')
plt.ylabel('Average Minimum Duration (hours)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Plot the data for average maximum duration
plt.figure(figsize=(10, 6))
plt.bar(avg_max_duration_by_region['region'], avg_max_duration_by_region['max_dur'], color='skyblue')
plt.title('Average Maximum Duration of Events by Region')
plt.xlabel('Region')
plt.ylabel('Average Maximum Duration (hours)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


#Box and whisker plots for duration variables by region 
import seaborn as sns

# Combine min_dur and max_dur into a single DataFrame
duration_data = filtered_data[['region', 'min_dur', 'max_dur']]

# Melt the DataFrame to have a long format
melted_duration_data = duration_data.melt(id_vars=['region'], value_vars=['min_dur', 'max_dur'], 
                                          var_name='Duration Type', value_name='Duration')

# Create the box and whisker plot
plt.figure(figsize=(12, 8))
sns.boxplot(x='region', y='Duration', hue='Duration Type', data=melted_duration_data)
plt.title('Box and Whisker Plot of Durations by Region')
plt.xlabel('Region')
plt.ylabel('Duration (hours)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#Box and whisker plots for duration variables by season
# Ensure 'season' column is in the filtered_data DataFrame
# filtered_data['season'] should already exist or be created based on your data

# Combine min_dur and max_dur into a single DataFrame
duration_data = filtered_data[['season', 'min_dur', 'max_dur']]

# Melt the DataFrame to have a long format
melted_duration_data = duration_data.melt(id_vars=['season'], value_vars=['min_dur', 'max_dur'], 
                                          var_name='Duration Type', value_name='Duration')

# Create the box and whisker plot
plt.figure(figsize=(12, 8))
sns.boxplot(x='season', y='Duration', hue='Duration Type', data=melted_duration_data)
plt.title('Box and Whisker Plot of Durations by Season')
plt.xlabel('Season')
plt.ylabel('Duration (hours)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

