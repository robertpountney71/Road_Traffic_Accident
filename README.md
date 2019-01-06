# Road_Traffic_Accident
Using python pandas library, combining data from all .csv files in a directory and creating an SQLite database consisting of the full dataset. 

## The following outlines the functionality of script “code_file.py”:

  •	The script will convert all the .csv files in current directory into one combined Pandas DataFrame.
  
  •	This combined DataFrame is keyed on “Accident_Index”.
  
  •	The script will then split the data from this combined DataFrame in two:
  
    o	80% of the data will be written to a training SQLite table.
    
    o	20% of the data will be written to a testing SQLite table.
    
  •	Both of these tables will exist in a newly created database “final_data.db”
