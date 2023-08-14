def categorical_analysis(var, **kwargs):
    fig, axes= plt.subplots(nrows=1, ncols=2, figsize=(15,5))
    axes[0].set_title(f'Variable {var}')
    sns.countplot(data=data, x=var, **kwargs, ax=axes[0])
    crossed=pd.crosstab(data[var], data.Revenue, normalize=0).unstack().reset_index().rename(columns={0:'Percentage'})
    crossed.loc[crossed.Revenue==False,'Percentage']=1
    sns.barplot(data=crossed, x=var, y='Percentage', hue='Revenue', ax=axes[1], **kwargs, dodge=False)
    axes[1].set_title(f'Revenue ~ {var}')
    plt.suptitle(f'Variable {var}')
    plt.show()   
    print('\n CHI SQUARE TEST \n')
    p_value=chi2_contingency(pd.crosstab(data[var], data.Revenue))[1]
    if p_value>0.05:
        print(f'The p_value is {p_value} and therefore we have to accept the null hypothesis that there is no significant relationship between {var} and Revenue')
    else:
        print(f'The p_value is {p_value} and therefore we can reject the null hypothesis that there is no significant relationship between {var} and Revenue')
        
        
def continuous_analysis(var,data=data, **kwargs):
    fig, axes= plt.subplots(nrows=1, ncols=2, figsize=(15,5))
    axes[0].set_title(f'Variable {var}')
    sns.histplot(data, x=var, **kwargs, ax=axes[0], bins=30, hue='Revenue', multiple='stack')
    sns.boxplot(data=data,y=var,x='Revenue', hue='Revenue' , ax=axes[1], **kwargs)
    plt.title(f'Revenue ~ {var}')
    plt.suptitle(f'Variable {var}')
    plt.show()
    print(f'\n The maximum value is {data[var].max()} \n The minimum value is {data[var].min()} ')

data.describe(include='category')

data=data.drop(data[(data.Administrative_Duration<0)&(data.Informational_Duration<0)&(data.ProductRelated_Duration<0)].index).reset_index(drop=True)

#This variable seems to be a good candidate to categoricals. It has only 6 different values (We have checked it at the beginning).
#Let's split it into two categories: 'yes' for 'Special day' days and 'no' for the others(0.2-> 1)

data['SpecialDay']=pd.cut(data['SpecialDay'], bins=[-1,0.1,1.1], labels=['Yes','No'])

categorical_analysis('SpecialDay')

mask = np.triu(np.ones_like(data.corr()))
plt.figure(figsize=(7,7))
sns.heatmap(data.corr(), annot=True, mask=mask, cmap='Blues', xticklabels=data.select_dtypes(exclude='category').columns[:-1]\
           ,yticklabels='auto', linewidths=.1, cbar=False)
np.fill_diagonal(mask, True)
plt.title('CORRELATION MATRIX')
plt.show()

numeric=data.select_dtypes(exclude='category')

VIF=pd.DataFrame()
VIF['variables']=numeric.columns
VIF['values']=[variance_inflation_factor(numeric.values, column) for column in range(len(numeric.columns))]
VIF