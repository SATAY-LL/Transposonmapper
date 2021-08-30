# From reads and insertions to essentiality prediction using a Regression Model

import pandas as pd
import numpy as np
import seaborn as sns
import scipy.optimize as opt
from sklearn import preprocessing
%matplotlib inline 
import matplotlib.pyplot as plt

import os
script_dir = os.path.dirname('__file__') #<-- absolute dir the script is in
rel_path_data_insertions="Python_scripts/Data_Files/wt-truncated-insertions-per-gene.txt"
rel_path_data_reads="Python_scripts/Data_Files/wt-truncated-reads-per-gene.txt"


abs_path_data_reads = os.path.join(script_dir, rel_path_data_reads)
abs_path_data_insertions = os.path.join(script_dir, rel_path_data_insertions)

# os.chdir('../') #<-- for binder os.chdir('../')



data_insertions = pd.read_csv(abs_path_data_insertions, sep="\t", header=0)

data_reads = pd.read_csv(abs_path_data_reads, sep="\t", header=0)

data_reads_pd=data_reads.iloc[:,0:3]
data_reads_pd.columns=['Gene_name','Essentiality','reads-truncated']
data_reads_pd.head()

data_insertions_pd=data_insertions.iloc[:,0:3]
data_insertions_pd.columns=['Gene_name','Essentiality','insertions-truncated']
data_insertions_pd.head()

data=data_reads_pd.copy()
data['insertions']=data_insertions_pd['insertions-truncated']


data.head()

## Visualising how the input data is distributed regarding the type of essentiality of the genes

fig, axes=plt.subplots(1,2)
plt.subplots_adjust(wspace=0.5)
sns.boxplot(x='Essentiality',y='insertions',data=data,ax=axes[0],fliersize=0.5)
# sns.boxplot(x='Essentiality',y='insertions-non-truncated',data=data,ax=axes[0])
# axes[0].set_ylim([0,100])
sns.boxplot(x='Essentiality',y='reads-truncated',data=data,ax=axes[1],fliersize=0.5)
axes[1].set_ylim([0,500])
axes[0].set_title('Outliers-viz')
axes[1].set_title('Outliers-viz')

## Remove outliers 

# fig, axes=plt.subplots(1,2)
# plt.subplots_adjust(wspace=0.5,right=1.2)
# sns.scatterplot(y='insertions',x=np.arange(0,len(data)),data=data,hue='Essentiality',ax=axes[0])
# # plt.ylim([0,20])
# sns.scatterplot(y='reads-truncated',x=np.arange(0,len(data)),data=data,hue='Essentiality',ax=axes[1])
# axes[0].set_title('Outliers-viz')
# axes[1].set_title('Outliers-viz')

### Make use of the IQR to remove the outliers

- IQR is part of Descriptive statistics and also called as midspead , middle 50%

- IQR is first Quartile minus the Third Quartile (Q3-Q1)

y_insert_non_essential=data[data['Essentiality']==0]['insertions']
removed_outliers_insertions_nE = y_insert_non_essential.between(y_insert_non_essential.quantile(.05), y_insert_non_essential.quantile(.95)) # any value bellow  Q1-0.05*IQR or above Q3+0.95*IQR is an outl

y_insert_essential=data[data['Essentiality']==1]['insertions']
removed_outliers_insertions_E = y_insert_essential.between(y_insert_essential.quantile(.05), y_insert_essential.quantile(.9)) # any value bellow  Q1-0.05*IQR or above Q3+0.95*IQR is an outl

y_reads_non_essential=data[data['Essentiality']==0]['reads-truncated']
removed_outliers_reads_nE = y_reads_non_essential.between(y_reads_non_essential.quantile(.05), y_reads_non_essential.quantile(.9)) # any value bellow  Q1-0.05*IQR or above Q3+0.95*IQR is an outl

y_reads_essential=data[data['Essentiality']==1]['reads-truncated']
removed_outliers_reads_E = y_reads_essential.between(y_reads_essential.quantile(.05), y_reads_essential.quantile(.9)) # any value bellow  Q1-0.05*IQR or above Q3+0.95*IQR is an outl

fig, axes=plt.subplots(1,4)
plt.subplots_adjust(wspace=0.5,right=2)

axes[0].plot(y_insert_non_essential,alpha=0.3)
axes[0].plot(y_insert_non_essential[removed_outliers_insertions_nE],label='removed-outliers-nE',color='black')
axes[0].legend()
axes[0].set_ylabel('Insertions after truncation')
axes[1].plot(y_insert_essential,alpha=0.3)
axes[1].plot(y_insert_essential[removed_outliers_insertions_E],label='removed-outliers-E',color='black')
axes[1].legend()
axes[1].set_ylabel('Insertions after truncation')

axes[2].plot(y_reads_non_essential,alpha=0.3,color='purple')
axes[2].plot(y_reads_non_essential[removed_outliers_reads_nE],label='removed-outliers-nE',color='black')
axes[2].legend()
axes[2].set_ylabel('Reads after truncation-nE')

axes[3].plot(y_reads_essential,alpha=0.3,color='purple')
axes[3].plot(y_reads_essential[removed_outliers_reads_E],label='removed-outliers-E',color='black')
axes[3].legend()
axes[3].set_ylabel('Reads after truncation-E')

index_nE=y_insert_non_essential[removed_outliers_insertions_nE].index
index_E=y_insert_essential[removed_outliers_insertions_E].index

data.loc[index_nE,'insertions-non-outliers']=y_insert_non_essential[removed_outliers_insertions_nE] 
data.loc[index_nE,'reads-non-outliers']=y_reads_non_essential[removed_outliers_reads_nE]
data.loc[index_E,'insertions-non-outliers']=y_insert_essential[removed_outliers_insertions_E]
data.loc[index_E,'reads-non-outliers']=y_reads_essential[removed_outliers_reads_E]




data.head()

fig, axes=plt.subplots(1,4)
plt.subplots_adjust(wspace=2.6,right=1.5)

data.fillna(0,inplace=True)
sns.boxplot(x='Essentiality',y='insertions-non-outliers',data=data,ax=axes[0],fliersize=0.5)
axes[0].set_title('With the outliers removed')
sns.boxplot(x='Essentiality',y='insertions',data=data,ax=axes[1],fliersize=0.5)
axes[1].set_title('Original')
sns.boxplot(x='Essentiality',y='reads-non-outliers',data=data,ax=axes[2],fliersize=0.5)
axes[2].set_title('With the outliers removed')
sns.boxplot(x='Essentiality',y='reads-truncated',data=data,ax=axes[3],fliersize=0.5)
axes[3].set_title('original')


data_remove_outliers=data.copy()
# data_remove_outliers=data_remove_outliers.drop(columns=['reads-non-truncated','insertions-non-truncated'])
data_remove_outliers.fillna(0,inplace=True)

data_remove_outliers.head()

data_remove_outliers.groupby('Essentiality').describe()

sns.pairplot(data=data_remove_outliers,hue='Essentiality',vars=['reads-non-outliers','insertions-non-outliers'])

### Features and output variable for the regression model

X = np.asarray(data_remove_outliers[['insertions-non-outliers', 'reads-non-outliers']])
y = np.asarray(data['Essentiality'])



from sklearn import preprocessing
X = preprocessing.StandardScaler().fit(X).transform(X)
X[0:5]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.1, random_state=4)
print ('Train set:', X_train.shape,  y_train.shape)
print ('Test set:', X_test.shape,  y_test.shape)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
LR = LogisticRegression(C=0.01, solver='liblinear').fit(X_train,y_train)
LR

yhat = LR.predict(X_test)
yhat[0:4]

from sklearn.metrics import classification_report, confusion_matrix
import itertools
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
print(confusion_matrix(y_test, yhat, labels=[1,0]))

cnf_matrix = confusion_matrix(y_test, yhat, labels=[1,0])
np.set_printoptions(precision=2)


# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=['Essential','Non essential'],normalize= False,  title='Confusion matrix')

print (classification_report(y_test, yhat))

### Predicting the probabilities for each gene to be essential or not

yprob=LR.predict_proba(X)# probability of cdc24 to be essential according this model
yprob[35]

data_remove_outliers['probability of being essential']=yprob[:,1]

sns.distplot(data_remove_outliers[data_remove_outliers['Essentiality']==0]['probability of being essential'],label='non-essentials',norm_hist=True)
sns.distplot(data_remove_outliers[data_remove_outliers['Essentiality']==1]['probability of being essential'],label='true-essentials',norm_hist=True)
plt.vlines(x=0.3,ymin=0,ymax=80,linewidth=2,alpha=0.5)
plt.vlines(x=0.42,ymin=0,ymax=80,linewidth=2,alpha=0.5)
plt.hlines(y=80,xmin=0.3,xmax=0.42,linewidth=2,alpha=0.5)
plt.fill_between(x=[0.3, 0.42],y1=80,color='black',alpha=0.2,label='88% of changes to be essential')
plt.legend()

ratio_essentials=[]
ratio_nonessentials=[]
prob=np.arange(0,1,0.01)
for i in prob:
    ratio_essentials.append(np.sum(y[np.where(yprob[:,1]>i)[0]])/len(yprob[:,1]>i)) # the sum symbolizes the number of 1's which are the true essential proteins 
    ratio_nonessentials.append(1-np.sum(y[np.where(yprob[:,0]>i)[0]])/len(y[np.where(yprob[:,0]>i)[0]]))

plt.scatter(prob,ratio_nonessentials,alpha=0.3,label= 'Class 0 Probab')
plt.scatter(prob,ratio_essentials,alpha=0.3,label='Class I Probab')
plt.xlabel('Probabilities')
plt.ylabel('ratio of true classification')
plt.legend()

index_prone2essential=[]
bound=0.3
for i in np.arange(0,len(yprob)):
    if yprob[i,1] > bound : 
        index_prone2essential.append(i)
ratio_true_essentials=np.sum(data_remove_outliers.iloc[index_prone2essential,:]['Essentiality'])/data_remove_outliers['Essentiality'].value_counts()[1]

### Summary from the model

print('- The essential genes represents a ',data_remove_outliers['Essentiality'].value_counts()[1]/len(data_remove_outliers) * 100,'%', 'of the population of genes.')

print('- The ratio of true essentials contained in the genes that have more than',bound,'probability of being essential is =', ratio_true_essentials *100,'%.','This represents',(len(index_prone2essential))/len(data_remove_outliers) * 100,'%', 'of all genes. In other words, with this regression model we can trust that a gene has', ratio_true_essentials *100,'%' ,'changes of being essential if the probability given by the model is higher than',bound)


print('- For the genes that has less than ',bound,'Pr to be essential , then I can assure they are non essential, which are ', len(data_remove_outliers)-len(index_prone2essential),'genes. That represents the',(len(data_remove_outliers)-len(index_prone2essential))/data_remove_outliers['Essentiality'].value_counts()[0] * 100,'%','of the total number of non essential genes.')


plt.hist(y[np.where(yprob[:,1]<0.3)]);

sns.distplot(yprob[:,0])
sns.distplot(yprob[:,1])

