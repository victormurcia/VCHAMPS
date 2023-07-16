def read_icd_codes(path):
    icd_codes = pd.read_csv(path + 'icd_codes_cc.csv').drop('Unnamed: 0', axis = 1)
    return icd_codes

# Function to split semicolon separated diagnoses into a list of diagnoses
def split_diagnoses(diagnoses):
    return [dx.lower().replace(",", "").strip() for dx in diagnoses.split(';')]

def process_diagnoses_dataframes(dataframes):
    final_df_list = []
    for idx, df in enumerate(dataframes):
        # Get the columns containing diagnoses (columns with 'icd10' in their name)
        diagnosis_columns = [col for col in df.columns if 'icd10' in col.lower()]
        print(idx, diagnosis_columns)
        df.compute()

        # Create a new column with a single list of diagnoses
        for i in range(len(diagnosis_columns)):
            if i == 0:
              df['diagnosis'] = df[diagnosis_columns[i]].apply(split_diagnoses)
            else:
              df['diagnosis'] = df['diagnosis'] + df[diagnosis_columns[i]].apply(split_diagnoses)

        # Explode the columns of lists so each row has a single diagnosis
        df = df.explode('diagnosis')
        df.reset_index(drop = True)
        # Merge to icd_codes csv
        df = df.merge(icd_codes, left_on='diagnosis', right_on='description', how='left')
        df = df.drop(columns = diagnosis_columns + ['description'])
        final_df_list.append(df)
    return final_df_list


