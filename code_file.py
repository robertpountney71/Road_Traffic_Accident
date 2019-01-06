import os
import sqlite3
import pandas as pd
import database_checks
"""
This module will covert all the .csv files in current directory into one combined dataframe 
keyed on Accident_Index. It will then split the dataframe 80:20 into a training and testing 
sqlite database. These databases are then fed into mml.fit/test functions respectively
"""

conn = sqlite3.connect('final_data.db')  # Establish connection with sqlite database
cur = conn.cursor()  # Create cursor allowing us to execute sql commands


def df2sqlite(dataframe, tbl_name):
    """Converts pandas dataframe to sqlite table"""
    wildcards = ','.join(['?'] * len(dataframe.columns))
    data = [tuple(x) for x in dataframe.values]

    cur.execute("DROP TABLE IF EXISTS %s" % tbl_name)

    col_str = '"' + '","'.join(dataframe.columns) + '"'
    cur.execute("CREATE TABLE %s (%s)" % (tbl_name, col_str))

    cur.executemany("INSERT INTO %s VALUES(%s)" % (tbl_name, wildcards), data)
    conn.commit()  # Commit current transaction to database


# Build up a list of dataframes, one for each .csv file in current directory
dfs = []  # Array of dataframes
for file in os.listdir('.'):
    if os.path.isfile(os.path.join('.', file)):
        if file.endswith('csv'):
            df = pd.read_csv(file)  # Convert .csv to dataframe
            dfs.append(df)

# Merge all the dataframes created from each .csv file
merged_df = dfs[0]
for i in range(1, len(dfs)):
    merged_df = pd.merge(merged_df, dfs[i], on='Accident_Index')


# 80% of the merged dataframe to a training dataframe
training_df = merged_df.loc[:(len(merged_df.index) * 0.8)]
# Remaining 20% of merged dataframe to a testing dataframe
testing_df = merged_df.loc[(len(merged_df.index) * 0.8): len(merged_df.index)]

# Convert training and testing dataframes to sqlite databases
df2sqlite(training_df, 'training_data')
df2sqlite(testing_df, 'testing_data')

# Call functions outlined in mml.py as per instructions
database_checks.fit('final_data.db', 'training_data')
database_checks.test('final_data.db', 'testing_data')


conn.close()  # Close connection with sqlite database