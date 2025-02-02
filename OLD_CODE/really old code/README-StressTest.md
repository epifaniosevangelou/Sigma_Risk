#SigmaInvestments
#StressTest
The code's primary purpose is to assess how different stress scenarios impact the risk (standard deviation) of a given portfolio of assets. It does so by applying each scenario to the portfolio, calculating the risk for each stressed portfolio, and presenting the results in a tabular format. 

The python file itself has explanations for each step of the way but here is an even more detailed explanation of the happenings:


Imports two important libraries: NumPY (`numpy`) and Pandas (`pandas`). 
`stress_test_scenario` Function:
    it takes two arguments, `portfolio` and `scenario`. It creates a copy of the `portfolio` to avoid modifying the original one. It applies the given `scenario` to each asset in the `portfolio` by multiplying the asset's weight by the scenario value. Then, it returns the modified (stressed) portfolio. 
`portfolio_risk` function:
    Calculates the risk of a portfolio based on its returns. It takes two arguments `portfolio` and `returns`. It Calculates the weighted returns of the portfolio by multiplying each asset's return by its weight and then computes the covariance matrix of these weighted returns.
    The portfolio's variance is calculated using matrix operations, and then the standard deviation (risk) of the portfolio is obtained by taking the square root of the portoflio variance. 
`portfolio_stress_test` function:
    This function performs a stress test on a portoflio considering various scenarios, taking arguments: `portfolio`, `returns`, and `scenarios`. 
    It then creates an empty Pandas DataFrame called `stress_test_results`.
    It iterates over the `scenarios` and does the following for each scenario:
        Calculates the stressed portfolio using the `stress_test_scenario` function.
        Computes the risk of the stressed portfolio using the `portfolio_risk` function. 
        Stores the risk value in the `stress_test_results` DataFrame, using the scenario value as the column name. 
    Finally, it returns the `stress_test_results` DataFrame containing the risk values for each scenario. 
Sample Portfolio, Returns, and Scenarios:
    A sample portfolio is defined as a dictionary (`portfolio`) with asset names as keys and their weights as values. 
    A sample set of returns for each asset is defined as a Pandas DataFrame (`returns`), where each row represents a time period, and each column represents an asset. 
    Sample stress test scenarios are defined as a list (`scenarios`) containing different numerical values representing the stress scenarios. 
Calculating the Stress Test:
    The `portfolio_stress_test` function is called with the sample `portfolio`, `returns`, and `scenarios`.
    The results are stored in the `stress_test_results` DataFrame.
Printing the results.