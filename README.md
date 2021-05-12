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

Wanke  
<div align=center><img width="550" alt="formula2" src="https://user-images.githubusercontent.com/78734848/117970583-669ea180-b35b-11eb-8fd3-8dd276266b2c.png"><div align=left>

Finally, we got the index as following:

<div align=center><img width="460" alt="系数" src="https://user-images.githubusercontent.com/78734848/117970903-d1e87380-b35b-11eb-9d06-1302862fed69.png"><div align=left>
  
Attribution analysis of individual stock income :
<div align=center><img width="840" alt="系数" src="https://user-images.githubusercontent.com/78734848/117971240-3572a100-b35c-11eb-8efc-6b8484d9cfb9.png"><div align=left>



  



  



