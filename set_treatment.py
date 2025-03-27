import random


def agecat(age):
    # Define age limits and categories
    age_ranges = [
        (18, 24),
        (25, 34),
        (35, 44),
        (45, 54),
        (55, 65)
    ]

    # Standard category, if no suitable category is found
    cat = None

    # Check and assign age value
    for i, (lower, upper) in enumerate(age_ranges):
        if lower <= age <= upper:
            cat = i
            break

    return cat

def set_treatment(quota_type, done_treatments, max_treatments, gender, age):
    """
    Sets the treatment for a session based on various parameters.

    :param max_treatments: List in settings.py
    :param done_treatments: List in settings.py
    :param quota_type: The type of quota to apply when setting the treatment.
                       This can be one of the following:
                       - 'max_treatment': Set maximum per treatment (MAX_TREATMENTS3).
                       - 'gender_based': Quotas are set based on gender categories (MAX_TREATMENTS2).
                       - 'gender_age_based': Quotas are set based on gender and age categories (MAX_TREATMENTS1).
    :param gender: Gender
    :param age: Age
    :return: Treatment
    """
    total_treatment_filtered = {}

    # Show total observations per treatment
    total_treatment = {key: sum(sum(sublist) for sublist in value) for key, value in done_treatments.items()}

    summed_data = {}
    summed_data2 = {}
    for key, value in done_treatments.items():
        # Calculate the number of observations in each treatment for the participant's gender and age category
        summed_data[key] = value[gender][agecat(age)]

        # Calculate the total number of participants for each gender across treatments
        summed_list = [sum(sublist) for sublist in value]
        summed_data2[key] = summed_list

    # Set the pending treatments based on total observations
    pending_treatments = total_treatment

    if quota_type == 'max_treatment':
        # Create list --> Check if Treatment full (max_treatment)
        total_treatment_filtered = {key: value for key, value in pending_treatments.items() if value < max_treatments.get(key, 0)}
    elif quota_type == 'gender_based':
        # Extract observations specific to the participant's gender
        gender_treatment = {key: value[gender] for key, value in summed_data2.items()}

        # Filter treatments based on the maximum quota for the participant's gender
        total_treatment_filtered = {key: value for key, value in pending_treatments.items() if gender_treatment[key] < max_treatments[key][gender]}

    elif quota_type == 'gender_age_based':
        # Filter treatments that have not yet reached the quota for the participant's gender and age category
        total_treatment_filtered = {key: value for key, value in summed_data.items() if summed_data[key] < max_treatments[key][gender][agecat(age)]}

    if not total_treatment_filtered:
        # no treatment available
        return None
    else:
        # Filter summed_data to include only treatments available in total_treatment_filtered
        filtered_summed_data = {k: v for k, v in summed_data.items() if k in total_treatment_filtered}

        # Determine the maximum value among the filtered treatments
        max_value = max(filtered_summed_data.values())

        # Calculate weights for each treatment based on the difference to the maximum value
        weights = {key: (max_value - value + 1) for key, value in filtered_summed_data.items()}
        total_weight = sum(weights.values())

        # Perform a weighted random choice to select a treatment
        choices, relative_weights = zip(*[(key, weight / total_weight) for key, weight in weights.items()])
        selected_treatment = random.choices(choices, weights=relative_weights, k=1)[0]

        return selected_treatment
