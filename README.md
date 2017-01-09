# Taiwan stock datafrme

all date read from taiwan stock exchange center(www.tse.com.tw).



### Key terms / Dataframe column

open price      = OP
close price     = CP
highest price   = HP
lowest price    = LP
trading volume  = TV
trading count   = TC
turnover        = TO
rise drop       = RD
differential    = DF
price earning   = PE


## Example

```python
import pandas as pd
df = pd.DataFrame.from_csv('bystock/' + stockid + '.csv')
print df
```
