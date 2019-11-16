import pandas as pd
import numpy as np
from sklearn import svm, preprocessing
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(font_scale=1.2)
from mpl_toolkits import mplot3d
from sklearn.model_selection import train_test_split
from sklearn import metrics

data=pd.read_csv("/Users/Sunny/Desktop/expirement-dummylabel/labelled-dummy-Stops-C1415.csv")

dataN=data[['Speed Variance','Duration','Distance from previous stop(in kms)']] #for normalized features
dataS=data[['Speed Variance','Duration','Distance from previous stop(in kms)']] #for standardized features

preprocessing.normalize(X=dataN, copy=False, axis=0)
preprocessing.normalize(X=dataN, copy=False, axis=0)


preprocessing.scale(dataS, copy=False, axis=0)
preprocessing.scale(dataS, copy=False, axis=0)

dataN['Label']=data.Label
dataS['Label']=data.Label

#getting a 2D view of data
#sns.lmplot('Duration', 'Speed Variance', data=dataN, hue='Label', palette='Set1', fit_reg=False, scatter_kws={"s":70})

featuresM=dataN[['Duration', 'Speed Variance', 'Distance from previous stop(in kms)']].as_matrix() #creating a matrix of feature to include
target=np.where(dataN['Label']=='D', 0,1) #marking delivery stops as 0
model=svm.SVC(kernel='rbf', C=2**5, gamma='scale')

#calculating classification accuracy
#X_train, X_test, y_train, y_test = train_test_split(featuresM, target, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(featuresM, target, random_state=0, stratify=target)
model.fit(X_train, y_train)
y_pred_class = model.predict(X_test)
print('Accuracy: ' + str(metrics.accuracy_score(y_test, y_pred_class)))

#trying to visualize in 3D to create rbf hyperplane
# X=dataN[['Duration', 'Speed Variance']]
# y=target
# r = np.exp(-(X ** 2).sum(1))
# ax = plt.subplot(projection='3d')
# ax.scatter3D(X['Duration'], X['Speed Variance'], r, c=y, s=50, cmap='autumn')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('r')

#trying to visualize in 3D to create rbf hyperplane
X=dataN[['Duration', 'Speed Variance', 'Distance from previous stop(in kms)']]
y=target
r = np.exp(-(X ** 2).sum(1))
ax = plt.subplot(projection='3d')
ax.scatter3D(X['Duration'], X['Speed Variance'], X['Distance from previous stop(in kms)'], c=y, s=50, cmap='autumn')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

