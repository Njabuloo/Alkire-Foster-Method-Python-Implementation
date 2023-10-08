# Alkire-Foster Method ReadMe

## Overview
The Alkire-Foster method is a widely used approach for measuring multidimensional poverty. This method assesses poverty by considering various dimensions of well-being and their associated cutoff values. This ReadMe file provides a concise explanation of the key components and steps involved in using the Alkire-Foster method.

## Key Components

1. **Persons and Dimensions Matrix (x)**
   - This is a two-dimensional matrix that contains data about individuals and their well-being across different dimensions.

2. **Cutoff Matrix (z)**
   - The cutoff matrix contains values that indicate whether a person is deprived in a specific dimension.
   - For numerical dimensions, a person is deprived if their value is less than the cutoff value.
   - For categorical dimensions, the cutoff indicates which category signifies deprivation.

3. **Deprivation Matrix (g0)**
   - A two-dimensional matrix (2D) where 1 represents deprivation, and 0 represents non-deprivation for each person and dimension.

4. **Weights Matrix (w)**
   - A one-dimensional matrix (1D) that assigns weights to each dimension based on their importance in the poverty assessment.

5. **Weighted Deprivation Matrix (gprime0)**
   - This matrix is obtained by multiplying each column of the deprivation matrix (g0) with the corresponding weight (same index for the column).

6. **Deprivation Score (d)**
   - A deprivation score is calculated by summing all the dimensions from the weighted deprivation matrix (gprime0).
   - A column containing the deprivation scores is added to the weighted deprivation matrix.

7. **Cutoff Score for Deprivation (k)**
   - The cutoff score (k) determines the threshold for identifying individuals as poor.
   - Users can interactively adjust the value of k in the front-end to explore different poverty thresholds.

8. **Censored Deprivation Matrix**
   - Individuals are considered censored if their deprivation score (d) falls below the cutoff score (k).

9. **Headcount Ratio (H)**
   - The headcount ratio (H) indicates the percentage of the population that is considered poor.
   - It is calculated as the ratio of the total number of individuals with a deprivation score greater than 0 to the total population, multiplied by 100.

10. **Average Between the Poor (A)**
    - The average between the poor (A) is calculated by summing all the 1s in the deprivation matrix (g0) and dividing by the total number of dimensions.
    - Afterward, this sum is further divided by the total number of poor individuals (where d is greater than 0).

11. **Adjusted Headcount Ratio (Mo)**
    - The adjusted headcount ratio (Mo) is computed as the product of H and A.
    - Alternatively, it can be calculated by summing all the 1s in the deprivation matrix (g0) and dividing by the total number of entries (rows * columns), resulting in the mean of the matrix.

## Front-End Interaction
Starting from step 7, the calculations, particularly the adjustment of the cutoff score (k), should be implemented in the front-end to allow users to explore different poverty thresholds interactively.

Please refer to the Alkire-Foster method documentation and relevant software tools for detailed instructions on implementing this method in your specific application.

For any further inquiries or assistance, please contact our support team.

---
**Note:** This ReadMe provides a high-level overview of the Alkire-Foster method. For detailed implementation guidelines and code examples, consult the appropriate documentation and resources.