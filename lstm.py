import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)

def differencing(ts):
    ts_diff = ts - ts.shift()
    ts_diff.dropna(inplace=True)
    return ts_diff

# fix random seed for reproducibility
np.random.seed(7)
# load the dataset
dataframe = pd.read_csv('aaa.txt', sep='\t', usecols=[1])
dataset = dataframe.values
dataset = dataset.astype('float32')
#dataset = np.log(dataset)
# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

# split into train and test sets
train_size = int(len(dataset) * 0.90)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
# reshape into X=t and Y=t+1
look_back = 14
num_epoch = 50
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))
#trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
#testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

# create and fit the LSTM network
batch_size = 1
model = Sequential()
#model.add(LSTM(4, input_length=look_back, input_dim=1))
model.add(LSTM(4, batch_input_shape=(batch_size, look_back, 1), stateful=True, return_sequences=True))
model.add(LSTM(4, batch_input_shape=(batch_size, look_back, 1), stateful=True))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
#model.fit(trainX, trainY, nb_epoch=100, batch_size=1, verbose=2)
for i in xrange(num_epoch):
    print 'Epoch %s/%s' % (str(i+1), num_epoch)
    model.fit(trainX, trainY, nb_epoch=1, batch_size=batch_size, verbose=2, shuffle=False)
    model.reset_states()

# Estimate model performance
trainScore = model.evaluate(trainX, trainY, batch_size=batch_size, verbose=0)
model.reset_states()
trainScore = np.sqrt(trainScore)
trainScore = scaler.inverse_transform(np.array([[trainScore]]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = model.evaluate(testX, testY, batch_size=batch_size, verbose=0)
model.reset_states()
testScore = np.sqrt(testScore)
testScore = scaler.inverse_transform(np.array([[testScore]]))
print('Test Score: %.2f RMSE' % (testScore))

# generate predictions for training
trainPredict = model.predict(trainX, batch_size=batch_size)
#trainPredict = np.exp(trainPredict)
model.reset_states()
testPredict = model.predict(testX, batch_size=batch_size)
#testPredict = np.exp(testPredict)
model.reset_states()

# shift train predictions for plotting
trainPredictPlot = np.empty_like(dataset)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

# shift test predictions for plotting
testPredictPlot = np.empty_like(dataset)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(look_back*2):len(dataset), :] = testPredict
print 'dataset:', len(dataset)
print 'trainY:', len(trainY)
print 'trainPredict:', len(trainPredict)

print 'testPredictPlot:', (len(dataset) - (len(trainPredict)+(look_back*2)))
print 'testPredict:', len(testPredict)
print 'testY:', len(testY)

# plot baseline and predictions
#dataset = np.exp(dataset)
#dataset = scaler.inverse_transform(dataset)
#trainPredictPlot = scaler.inverse_transform(trainPredictPlot)
#testPredictPlot = scaler.inverse_transform(testPredictPlot)
plt.plot(dataset)
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()
