import random


def agecat(age):
    if age < 35:
        cat = 0
    elif age < 50:
        cat = 1
    else:
        cat = 2
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

    pending_treatments = total_treatment
    if quota_type == 'max_treatment':
        # Create list --> Check if Treatment full (max_treatment)
        total_treatment_filtered = {key: value for key, value in pending_treatments.items() if value < max_treatments.get(key, 0)}
    elif quota_type == 'gender_based':
        # check how many observations are already in Treatment depending on gender
        summed_data = {}
        for key, value in done_treatments.items():
            # Sum each sublist individually
            summed_list = [sum(sublist) for sublist in value]
            # Add the summed list to the new dictionary
            summed_data[key] = summed_list
        gender_treatment = {key: value[gender] for key, value in summed_data.items()}
        total_treatment_filtered = {key: value for key, value in pending_treatments.items() if gender_treatment[key] < max_treatments[key][gender]}
    elif quota_type == 'gender_age_based':
        summed_data = {}
        for key, value in done_treatments.items():
            summed_data[key] = value[gender][agecat(age)]
        total_treatment_filtered = {key: value for key, value in summed_data.items() if summed_data[key] < max_treatments[key][gender][agecat(age)]}

    if not total_treatment_filtered:
        # no treatment available
        return None
    else:
        # Max value
        max_value = max(total_treatment_filtered.values())

        # Calculate weights based on the difference to the maximum value
        weights = {key: (max_value - value + 1) for key, value in total_treatment_filtered.items()}
        total_weight = sum(weights.values())

        # Weighted choice
        choices, relative_weights = zip(*[(key, weight / total_weight) for key, weight in weights.items()])
        selected_treatment = random.choices(choices, weights=relative_weights, k=1)[0]

        return selected_treatment
