# Assignment3
The assignment about Fama French Model for Algo Trading.
## Brief introduction
After the CAPM model has undergone a lot of empirical research and application, there is evidence that market risk premium cannot fully explain the rate of return of 
individual risky assets. So many researchers began to explore other factors, such as company market value. Fama and French extracted three important factors: market 
risk premium factor, market value factor and book-to-market value ratio factor, and constructed a linear model similar to CAPM, which is the famous  Fama and French Three-Factor Model. 

This article tried to use Fama French Model in Chinese market from Jan 1, 2018 to Mar 31, 2021.
## Principles of the three-factor model
The three factors in the three-factor model are the rate of return of the portfolio: the market risk premium factor corresponds to the rate of return of the market portfolio,
and the market value factor corresponds to the investment of long companies with smaller market capitalization and short companies with larger market capitalization. 
The rate of return brought by the portfolio, and the book-to-market value ratio factor corresponds to the rate of return brought by the investment portfolio of 
long BM companies and short BM companies. The form of the three-factor model is: 

<div align=center><img width="460" alt="formula" src="https://user-images.githubusercontent.com/78734848/117966796-eaa25a80-b356-11eb-9fbc-113f93db9ac3.png"><div align=left>

For the calculation of SMB and HML, this part needs to first divide the stocks into 1:1 large market capitalization (B) and small market capitalization (S) stocks according to the circulating market value; according to the BM data, divide the stocks into 3:4:3 high, medium and low ( H/M/L) three groups; in this way, we have a 2×3 total of 6 investment portfolios (SL/SM/SH/BL/BM/BH). Then we obtain the rate of return of each group through the weighted average of the market value, and finally find the SMB and HML: 

<div align=center><img width="377" alt="formula2" src="https://user-images.githubusercontent.com/78734848/117967183-584e8680-b357-11eb-9935-52e5e27ea49b.png"><div align=left>


## Picking stocks and the benchmark index 
We picked China Vanke(wanke), Ping An Insurance Company(pingan), Kweichow Moutai Company(maotai), Wanhua Chemical Group Company(wanhua) and iFLYTEK(keda) as our research stocks,
using China Securities A share index as the benchmark index.

### Time series graph of cumulative return
<div align=center><img width="640" alt="累计收益率时序图" src="https://user-images.githubusercontent.com/78734848/117968966-61405780-b359-11eb-9af9-9896e1c54900.png"><div align=left>

### Correlation coefficient graph
<div align=center><img width="640" alt="相关系数" src="https://user-images.githubusercontent.com/78734848/117969120-9a78c780-b359-11eb-83a5-9dda2e05b5f9.png"><div align=left>

## Model fitting 
Using OLS to fit the Fama French Model, we get servel result like the following :

                            OLS Regression Results                            
==============================================================================
Dep. Variable:                  wanke   R-squared:                       0.466
Model:                            OLS   Adj. R-squared:                  0.464
Method:                 Least Squares   F-statistic:                     228.1
Date:                Wed, 12 May 2021   Prob (F-statistic):          2.25e-106
Time:                        15:51:55   Log-Likelihood:                 2137.5
No. Observations:                 788   AIC:                            -4267.
Df Residuals:                     784   BIC:                            -4248.
Df Model:                           3                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
const          0.0019      0.001      3.137      0.002       0.001       0.003
x1             1.1044      0.045     24.781      0.000       1.017       1.192
x2            -0.7876      0.067    -11.682      0.000      -0.920      -0.655
x3             0.8861      0.073     12.204      0.000       0.744       1.029
==============================================================================
Omnibus:                       96.843   Durbin-Watson:                   1.829
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              232.976
Skew:                           0.671   Prob(JB):                     2.57e-51
Kurtosis:                       5.301   Cond. No.                         133.
==============================================================================

