import pandas as pd
import numpy as np
from sklearn import svm, preprocessing
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(font_scale=1.2)
from mpl_toolkits import mplot3d
from sklearn.model_selection import train_test_split
from sklearn import metrics

import numpy as np

#copied as is from kaggle; authored by:Intel & MobileODT Cervical Cancer Screening
def plot_confusion_matrix(cm,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=True):
    """
    given a sklearn confusion matrix (cm), make a nice plot

    Arguments
    ---------
    cm:           confusion matrix from sklearn.metrics.confusion_matrix

    target_names: given classification classes such as [0, 1, 2]
                  the class names, for example: ['high', 'medium', 'low']

    title:        the text to display at the top of the matrix

    cmap:         the gradient of the values displayed from matplotlib.pyplot.cm
                  see http://matplotlib.org/examples/color/colormaps_reference.html
                  plt.get_cmap('jet') or plt.cm.Blues

    normalize:    If False, plot the raw numbers
                  If True, plot the proportions

    Usage
    -----
    plot_confusion_matrix(cm           = cm,                  # confusion matrix created by
                                                              # sklearn.metrics.confusion_matrix
                          normalize    = True,                # show proportions
                          target_names = y_labels_vals,       # list of names of the classes
                          title        = best_estimator_name) # title of graph

    Citiation
    ---------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    """
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools

    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")


    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()

data=pd.read_csv("/Users/Sunny/Desktop/expirement-dummylabel/labelled-dummy-Stops-C1415.csv")

dataN=data[['Speed Variance','Duration','Distance from previous stop(in kms)', 'Time travelled before stop']] #for normalized features
dataS=data[['Speed Variance','Duration','Distance from previous stop(in kms)', 'Time travelled before stop']] #for standardized features

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
model=svm.SVC(kernel='rbf', C=2**5, gamma='scale', probability=True) #C adjusted for hard-limits

#calculating classification accuracy
#X_train, X_test, y_train, y_test = train_test_split(featuresM, target, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(featuresM, target, random_state=0, stratify=target)
model.fit(X_train, y_train)
y_pred_class = model.predict(X_test)
print('Classification Accuracy of trained model: ' + str(metrics.accuracy_score(y_test, y_pred_class)))

#some stats using confusion matrix
cm=metrics.confusion_matrix(y_test, y_pred_class)
#plot_confusion_matrix(cm, target_names=['Delivery Stop', 'Maintenance Stop'], title='', normalize=True)
pD= cm[0][0]/(cm[0][0]+cm[1][0]) #precision of delivery stops
pM= cm[1][1]/(cm[0][1]+cm[1][1]) #precision of maintenance stops
rD= cm[0][0]/(cm[0][0]+cm[0][1])#recall of delivery stops
rM= cm[1][1]/(cm[1][0]+cm[1][1])#recall of maintenance stops
print('Heads up: Precision for a class defines the reliability of a True Positive, while recall of a class defines the ability to detect True Postive')
print('Precision Delivery: ' + str(pD))
print('Precision Maintenance: ' + str(pM))
print('Recall Delivery: ' + str(rD))
print('Recall Maintenance: ' + str(rM))


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
# X=dataN[['Duration', 'Speed Variance', 'Distance from previous stop(in kms)']]
# y=target
# r = np.exp(-(X ** 2).sum(1))
# ax = plt.subplot(projection='3d')
# ax.scatter3D(X['Duration'], X['Speed Variance'], X['Distance from previous stop(in kms)'], c=y, s=50, cmap='autumn')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')

#('StopID', 'VehicleID', 'StartRow', 'StopRow', 'StartTime', 'EndTime', 'Latitude', 'Longitude', 'Average Speed before stop', 'Distance from previous stop(in kms)', 'Time travelled before stop', 'Speed Variance', 'Duration', 'Label')
