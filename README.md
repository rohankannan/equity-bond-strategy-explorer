# Fund Allocation to Equity and Bonds
*A tool to explore diversification strategies for leveraged portfolios, as described by Clifford S. Asness*

## Introduction
I recently spent some time exploring the topic of allocation to equity and bonds. I spent most of my time looking at two particular publications: *College and University Endowment Funds: Why Not 100% Equities?* by Richard H. Thaler and J. Peter Williamson, and *Why **Not** 100% Equities* by Clifford S. Asness, an analysis made in response to the former paper. In evaluating both positions, I agreed more with Asness's analysis: firstly, that crafting a set of efficient portfolios with varying risks is a separate part of developing a portfolio than actually deciding which portfolio to choose (i.e. what risk/return ratio to assume). Secondly, that a 60:40 ratio of equities to bonds, levered to match the same volatility, is the better option, matching risk according to standard deviation while outperforming the other portfolio in compound return. Additionally, Asness makes a compelling argument that the 60:40 portfolio is superior in both the worst cases and in the probability of outperformance. 

Asness then continues his analysis by looking at when you cannot or will not lever, or if you have a long time horizon, and brings up a sidenote regarding equilibrium. While these are certainly interesting, I was more interested in exploring the numerical side of his analysis through two main data-driven lenses: annualized total returns and worst case analysis. Asness's analysis brought up one major question for me. What is the optimal ratio of equities to bonds? The paper was written in 1996, and in reading it almost 30 years later, I had access to computational tools that were not present back then. So, I developed this tool to explore levered portfolio strategies with varying ratios using similar analytical methods. 

## Findings
Using a dataset of corporate bonds to populate monthly rate changes for bonds, and a dataset of the S&P 500 to populate monthly rate changes for equity, I was able to come up with a sample from 2016-2024. In Asness's analysis, he uses the same markets to make his analysis, but over a much longer time frame. The short period is one of the major limitations of my sample. That being said, the program still yields meaningful conclusions. Over 1000 simulations, almost all strategies yield a net positive, and the majority earn between 12%-13% in annualized return. 

![Figure 1](https://raw.githubusercontent.com/rohankannan/equity-bond-strategy-explorer/refs/heads/main/Figure_1.png) 
*The above chart depicts the value of the funds of all 1000 strategies*

The best strategy had a ratio of 13.9% equities to 86.1% bonds, which is very different to Asness's suggested 60:40 ratio. This can potentially be explained by the fact that a significant portion of the sample period was during the coronavirus pandemic, which negatively affected equities more than corporate bonds. However, certain portfolios that depended too much on corporate bonds were not able to meet the yield required to pay back the interest rate on the leverage, which resulted in them underperforming. The strategy also leveraged at a rate of 679% in order to match the volatility of the 100% equity portfolio at 12.33%. 

![Figure 2](https://raw.githubusercontent.com/rohankannan/equity-bond-balancing/refs/heads/main/Figure_2.png) 
*The above chart depicts the sample distribution of annualized return across all strategies*


## Using the Tool
The tool I built relies on 4 major user-specified variables and additionally includes an option to adjust the initial funds (although this does not impact the evaluation of the strategies). The four variables include:
1. FILEPATH - specify the filepath to a csv with relevant data.
2. SIMULATION_GRANULARITY - adjust the number of strategies to be tested.
3. LEVERED - boolean specifying whether or not to lever funds in simulated strategies. Leverage amount will be selected to match the volatility of the most volatile strategy.
4. LEVERAGE_INTEREST_RATE - rate of interest on loans. By default, this is set to the annualized benchmark interest rate of 1.97% adjusted to compound monthly.

To run the tool, install the latest version of python and install the pandas, numpy, and matplotlib libraries. The program will then generate a command line summary of the best portfolio and provide two charts similar to those seen above. To change the dataset, follow the same formatting of the csv provided as a sample.

## Limitations
The most significant drawdown of this tool is that the dataset is extremely limited. This is because I only had access to free datasets and could only compile accurate data from 2016 to 2024, which reduces confidence in any conclusions regarding long run strategy. It goes without saying that this is a personal project to further explore two interesting finance papers and should not be used to inform any real-world financial decisions.
