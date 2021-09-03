import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.max_columns', 8)

# Read the .csv files into dataframes
df1 = pd.read_csv('test/sports.csv',  encoding='utf-8')
df2 = pd.read_csv('test/prenatal.csv', encoding='utf-8')
df3 = pd.read_csv('test/general.csv',  encoding='utf-8')

# Renamed the columns so that they match
df1.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'}, inplace=True)
df2.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'}, inplace=True)

# Merged dataframes
merged = pd.concat([df3, df2, df1], ignore_index=True)

# Deleted Unnamed: 0 column and dropped all the empty rows
merged.drop(columns=['Unnamed: 0'], inplace=True)
merged.dropna(how='all', inplace=True)

# Replaced the gender values with 'f' or 'm'
merged.loc[merged['gender'] == 'female', 'gender'] = 'f'
merged.loc[merged['gender'] == 'male', 'gender'] = 'm'
merged.loc[merged['gender'] == 'woman', 'gender'] = 'f'
merged.loc[merged['gender'] == 'man', 'gender'] = 'm'

# Replaced the NaN values in the gender column of the prenatal hospital with f
merged.loc[merged.hospital == 'prenatal', 'gender'] = "f"

# Replaced the NaN values in other columns with zeros
merged.fillna({'bmi': 0, 'diagnosis': 0, 'blood_test': 0, 'ecg': 0, 'ultrasound': 0, 'mri': 0, 'xray': 0, 'children': 0, 'months': 0}, inplace=True)

# Count the number of patients in each hospital
general_count = merged.loc[merged.hospital == 'general', 'hospital'].count()
prenatal_count = merged.loc[merged.hospital == 'prenatal', 'hospital'].count()
sports_count = merged.loc[merged.hospital == 'sports', 'hospital'].count()

patients_dic = {general_count: 'general', prenatal_count: 'prenatal', sports_count: 'sports'}
patients = [general_count, prenatal_count, sports_count]

print(f'The answer to the 1st question is {patients_dic[max(patients)]}')

# Find the share of the patients that are diagnosed with stomach disorder in the general hospital
ans_2 = len(merged[(merged['hospital'] == 'general') & (merged['diagnosis'] == 'stomach')]) / len(merged[(merged['hospital'] == 'general')])
print(f'The answer to the 2nd question is {round(ans_2, 3)}')

# Find the share of patients that are diagnosed with dislocation in sports hospital
ans_3 = len(merged[(merged['hospital'] == 'sports') & (merged['diagnosis'] == 'dislocation')]) / len(merged[(merged['hospital'] == 'sports')])
print(f'The answer to the 3rd question is {round(ans_3, 3)}')

# Calculate the median of age in the general and sports hospitals
median_ages_general = merged.loc[merged.hospital == 'general', 'age'].median()
median_ages_sports = merged.loc[merged.hospital == 'sports', 'age'].median()
ans_4 = median_ages_general - median_ages_sports

print(f'The answer to the 4th question is {ans_4}')

# Find the hospital with the greatest number of blood tests and calculate the number.
blood_test_general = len(merged[(merged['hospital'] == 'general') & (merged['blood_test'] == 't')])
blood_test_prenatal = len(merged[(merged['hospital'] == 'prenatal') & (merged['blood_test'] == 't')])
blood_test_sports = len(merged[(merged['hospital'] == 'sports') & (merged['blood_test'] == 't')])
blood_tests_list = [blood_test_general, blood_test_prenatal, blood_test_sports]
blood_tests_dict = {blood_test_general: 'general', blood_test_prenatal: 'prenatal', blood_test_sports: 'sports'}
print(f'The answer to the 5th question is {blood_tests_dict[max(blood_tests_list)]}, {max(blood_tests_list)} blood tests')


# Create a histogram using matplotlib
bins = [0,15,35,55,70,80]
labels = ['0-15','15-35','35-55','55-70','70-80']
merged['AgeGroup'] = pd.cut(merged['age'], bins=bins, labels=labels, right=False)
y_val = [len(merged[(merged['AgeGroup'] == '0-15')]), len(merged[(merged['AgeGroup'] == '15-35')]),
         len(merged[(merged['AgeGroup'] == '35-55')]), len(merged[(merged['AgeGroup'] == '55-70')]),
         len(merged[(merged['AgeGroup'] == '70-80')])]
plt.bar(labels, y_val, align='center')  # A bar chart
plt.xlabel('Bins')
plt.ylabel('Frequency')
plt.show()

# Print the shape and 20 random rows
print(merged.shape)
print(merged.sample(n=20, random_state=30))

