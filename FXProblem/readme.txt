This is the solution for problem statement
2. Problem Statement: FX problem

Step 1:
We first crawl www.google.com to get the relevant websites for each of the entries provided in the dataset of 500 companies and store it in the csv against each company name. Each link is crawled for textual data.

Step 2:
We fetch forex terms/keywords that are likely to be found in a website which requires a foreign exchange service from http://www.investopedia.com/categories/forex.asp

Step 3:
We crawl each of the links from Step 1. 
We eliminate stop words and find the relevant terms ( relevant in terms of similarity of the concepts from Step 2. We use word2vector to find the similarity )
Each of these words from the forex terminology becomes a feature in the final dataset.
Given these features and the labels(Forex or non Forex), we fit find the propensity score and fit a LogisticRegression Classifier to develop the model, which will eventually be the basis, to determine whether a company can be a potential customer for ForEx.