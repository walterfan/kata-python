import matplotlib.pyplot as plt
import pandas as pd

# 构造数据
data = {'year': [2010, 2011, 2012, 2013, 2014, 2015, 2016],
        'sales': [12, 18, 23, 15, 17, 21, 19]}
df = pd.DataFrame(data)

# 绘制拆线图
plt.plot(df['year'], df['sales'], marker='o')
plt.xlabel('Year')
plt.ylabel('Sales')
plt.title('Sales Trend')

# 绘制数据表格
fig, ax = plt.subplots()
ax.axis('off')
ax.axis('tight')
ax.table(cellText=df.values, colLabels=df.columns, loc='center')

# 显示图表
plt.show()
#plt.savefig('sales_over_time.png')
