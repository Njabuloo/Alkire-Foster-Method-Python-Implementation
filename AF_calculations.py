import pandas as pd
from typing import List


def get_deprivation_matrix(
    dimensions_matrix: pd.DataFrame, cutoff_matrix: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate the deprivation matrix (g0) based on dimensions and cutoff values.

    Args:
        dimensions_matrix (pd.DataFrame): DataFrame containing dimensions data.
        cutoff_matrix (pd.DataFrame): DataFrame containing cutoff values.

    Returns:
        pd.DataFrame: Deprivation matrix (g0).
    """
    # Get column names for the dataframes
    dimensions_column_names: List[str] = dimensions_matrix.columns

    # Create a copy of the dimensions matrix as the deprivation matrix
    deprivation_matrix: pd.DataFrame = dimensions_matrix.copy()

    # Generate values for the deprivation matrix based on dimensions and cutoff values
    for index, col_name in enumerate(dimensions_column_names):
        cutoff_value = cutoff_matrix.at[index, "Cutoff"]
        deprivation_matrix[col_name] = deprivation_matrix[col_name].apply(
            lambda value: 1 if value == cutoff_value else 0
        )

    return deprivation_matrix


def calculate_weighted_deprivation_matrix(
    deprivation_matrix: pd.DataFrame, weights_matrix: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate the weighted deprivation matrix based on the deprivation matrix and weights.

    Args:
        deprivation_matrix (pd.DataFrame): Deprivation matrix (g0).
        weights_matrix (pd.DataFrame): DataFrame containing weights.

    Returns:
        pd.DataFrame: Weighted deprivation matrix.
    """
    # Iterate through columns of the deprivation matrix
    for index, col_name in enumerate(deprivation_matrix.columns):
        # Get the weight corresponding to the column
        weight = weights_matrix.at[index, "Weight"]

        # Multiply the values in the column by the weight
        deprivation_matrix[col_name] = deprivation_matrix[col_name] * weight

    return deprivation_matrix


def calculate_deprevation_scores(
    weighted_deprivation_matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate deprivation scores based on the weighted deprivation matrix.

    Args:
        weighted_deprivation_matrix (pd.DataFrame): DataFrame containing weighted deprivation values.

    Returns:
        pd.DataFrame: DataFrame containing deprivation scores.
    """
    # Determine the number of rows in the weighted deprivation matrix
    number_of_rows = len(weighted_deprivation_matrix)

    # Initialize a DataFrame to store the deprivation scores
    data = {"Scores": [0] * number_of_rows}
    deprevation_scores = pd.DataFrame(data)

    # Calculate the deprivation score for each row in the weighted deprivation matrix
    for index in range(number_of_rows):
        deprevation_score = weighted_deprivation_matrix.iloc[index].sum()

        # Update the 'Scores' column in the deprivation scores DataFrame
        deprevation_scores.at[index, "Scores"] = deprevation_score

    return deprevation_scores


def get_censored_vector(
    deprevation_scores_vector: pd.DataFrame, cutoff_score: int
) -> pd.DataFrame:
    """
    Generate a censored vector based on deprivation scores and a cutoff score.

    Args:
        deprevation_scores_vector (pd.DataFrame): DataFrame containing deprivation scores.
        cutoff_score (int): Cutoff score used to censor deprivation scores.

    Returns:
        pd.DataFrame: Censored vector of deprivation scores.
    """
    # Create a copy of the deprivation scores vector
    censored_vector = deprevation_scores_vector.copy()

    # Iterate through the rows of the vector and apply censoring
    for index in range(len(censored_vector)):
        deprivation_score = censored_vector.at[index, "Scores"]

        # Apply censoring: If the deprivation score is below the cutoff, set it to 0
        censored_vector.at[index, "Scores"] = (
            deprivation_score if deprivation_score >= cutoff_score else 0
        )

    return censored_vector


def get_head_count_ratio(censored_vector: pd.DataFrame) -> float:
    """
    Calculate the headcount ratio (H) based on a censored vector.

    The headcount ratio (H) represents the percentage of the population with a positive score in the censored vector.

    Args:
        censored_vector (pd.DataFrame): DataFrame containing censored deprivation scores.

    Returns:
        float: The headcount ratio as a percentage.
    """
    # Calculate the count of individuals with a positive score
    positive_count = len(censored_vector.loc[censored_vector["Scores"] > 0])

    # Calculate the total count of individuals in the censored vector
    total_count = len(censored_vector)

    # Calculate the headcount ratio as a percentage
    headcount_ratio = 100 * (positive_count / total_count)

    return headcount_ratio


def get_average_deprivation_score(
    censored_vector: pd.DataFrame, number_of_dimensions: int
) -> float:
    """
    Calculate the average deprivation score for the Alkire-Foster method.

    The average deprivation score is the weighted average of deprivation scores for individuals classified as poor.

    Args:
        censored_vector (pd.DataFrame): DataFrame containing censored deprivation scores.
        number_of_dimensions (int): Total number of dimensions or indicators.

    Returns:
        float: The average deprivation score as a percentage.
    """
    # Calculate the sum of deprivation scores for individuals classified as poor
    scores_sum = censored_vector["Scores"].sum()

    # Calculate the total count of poor individuals
    total_poor_people = len(censored_vector.loc[censored_vector["Scores"] > 0])

    # Calculate the average deprivation score
    average_deprivation_score = (scores_sum / number_of_dimensions) / total_poor_people

    # Convert the average deprivation score to a percentage
    average_deprivation_score_percentage = 100 * average_deprivation_score

    return average_deprivation_score_percentage


def get_adjusted_head_count_ratio(
    average_deprivation_score: float, headcount_ratio: float
) -> float:
    """
    Calculate the adjusted headcount ratio for the Alkire-Foster method.

    The adjusted headcount ratio represents the product of the headcount ratio and the average deprivation score.

    Args:
        average_deprivation_score (float): The average deprivation score as a percentage.
        headcount_ratio (float): The headcount ratio as a percentage.

    Returns:
        float: The adjusted headcount ratio as a percentage.
    """
    # Convert percentages to ratios (divide by 100)
    average_deprivation_score /= 100
    headcount_ratio /= 100

    # Calculate the adjusted headcount ratio
    adjusted_headcount_ratio = 100 * headcount_ratio * average_deprivation_score

    return adjusted_headcount_ratio


def calculate_subgroup_data(
    demographics_matrix: pd.DataFrame, censored: pd.DataFrame
) -> list:
    """
    Calculate subgroup data based on the demographics matrix and censored data.

    Args:
        demographics_matrix (pd.DataFrame): DataFrame containing demographic information.
        censored (pd.DataFrame): DataFrame containing censored data.

    Returns:
        list: List of subgroups along with their corresponding data.
    """
    sub_groups_data = []

    for col in demographics_matrix.columns:
        sub_group_name = col
        sub_group_data = {}
        total_censored = len(censored[censored["Scores"] > 0])

        for value in demographics_matrix[col].unique():
            subgroup_censored_count = len(
                demographics_matrix[
                    (demographics_matrix[col] == value) & (censored["Scores"] > 0)
                ]
            )
            percentage = subgroup_censored_count / total_censored
            sub_group_data[value] = percentage

        sub_groups_data.append([sub_group_name, sub_group_data])

    return sub_groups_data

def calculate_products(subgroup_data):
    """
    Calculate products of subgroups based on pre-calculated subgroup data.

    Args:
        subgroup_data (list): List of pre-calculated subgroup data.

    Returns:
        dict: A dictionary containing the calculated products for different subgroups.
    """
    # Prepare data for product calculation
    demographics = []
    for result in subgroup_data:
        name = result[0]
        percentages = result[1]
        for key, value in percentages.items():
            demographics.append([name, key, value])

    # Calculate products for different subgroups
    products = {}
    for i in range(len(demographics)):
        for j in range(i + 1, len(demographics)):
            if demographics[i][0] != demographics[j][0]:
                demograph = demographics[i][0] + "-" + demographics[j][0]
                names = demographics[i][1] + "-" + demographics[j][1]
                product = demographics[i][2] * demographics[j][2]
                products.setdefault(demograph, []).append([names, product])

    return products
