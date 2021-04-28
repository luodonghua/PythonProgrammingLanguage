import pandas as pd
import matplotlib.pyplot as plt

data = [['2021-04-03', 88.1], ['2021-04-09', 86.9],['2021-04-10', 86.5],['2021-04-11', 86.4],['2021-04-12', 85.9],
        ['2021-04-13', 85.7],['2021-04-14', 85.2],['2021-04-15', 85.1],['2021-04-16', 84.4],['2021-04-17', 84.4],
        ['2021-04-18', 85.1],['2021-04-19', 85.0],['2021-04-20', 84.6],['2021-04-21', 84.3],['2021-04-22', 84.4],
        ['2021-04-23', 84.0],['2021-04-24', 84.0],['2021-04-25', 84.2],['2021-04-26', 84.6],['2021-04-27', 83.8],
        ['2021-04-28', 83.4]]

df = pd.DataFrame(data, columns=['Date','Weight'])

df['Date']= pd.to_datetime(df['Date'])

fig, axs = plt.subplots(figsize=(10, 7)) 
df.plot.line(x='Date', y='Weight', ylim=[80,90], ax=axs, rot=90, legend=True, grid = True, title="Weight Chart")
axs.set_ylabel('Weight (kg)', fontsize=14)
axs.set_xlabel('Date', fontsize=14)
plt.tight_layout()
plt.show()
fig.savefig("Weight_chart.png",bbox_inches='tight')     
