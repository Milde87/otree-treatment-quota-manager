import pandas as pd
from set_treatment import *
from settings import *

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

gender_list = {
    'female': 0,
    'male': 1,
    'non_binary': 2
}

# Number of requests
ITERATION = 800

# __init__.py (Last Page)

genders = ['female', 'male', 'non_binary']
probabilities = [0.5, 0.5, 0]

var = []
screened_out_participants = 0

for i in range(ITERATION):

    # Gender
    gender = random.choices(genders, probabilities)[0]
    # Age
    age = random.randint(18, 65)

    # Set treatment based on quota type:
    # treatment = set_treatment('max_treatment', DONE_TREATMENTS, MAX_TREATMENTS3, gender_list[gender], age)
    # treatment = set_treatment('gender_based', DONE_TREATMENTS, MAX_TREATMENTS2, gender_list[gender], age)
    treatment = set_treatment('gender_age_based', DONE_TREATMENTS, MAX_TREATMENTS1, gender_list[gender], age)

    if treatment is not None:
        DONE_TREATMENTS[treatment][gender_list[gender]][agecat(age)] += 1
    else:
        screened_out_participants += 1

df = pd.DataFrame.from_dict(DONE_TREATMENTS, orient='index')
df.columns = ['Female', 'Male', 'Non-binary']
df['Row Sum'] = df.apply(lambda row: sum(sum(sublist) for sublist in row), axis=1)
column_sums = df.iloc[:, :-1].apply(lambda col: sum(sum(item) for item in col))
df.loc['Column Sum'] = list(column_sums) + [column_sums.sum()]
print(df)

print()
print('Screened out participants:', screened_out_participants)
