from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from collections import deque
import numpy as np
import random


REPLAY_MEMORY_SIZE= 64
BATCH_SIZE= 64
UPDATE_TARGET_EVERY=5
DISCOUNT=0.95
class DQNAgent:
    def __init__(self):
        #main  get trained evert step
        self.model=self.createModel()
        
        #target predicts every step
        self.targetModel= self.createModel()
        self.targetModel.set_weights(self.model.get_weights())
        
        self.replayMemory= deque(maxlen=REPLAY_MEMORY_SIZE)
        
        self.targetUpdateCounter=0
        

        
    def createModel(self):
        model = Sequential()
        model.add(Dense(units=64, activation='relu', input_dim=4))
        model.add(Dropout(0.3))
        model.add(Dense(64,activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(64,activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(64,activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(64,activation='relu'))
        model.add(Dense(3, activation="softmax"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=['accuracy'])
        return model
    
    def updateReplyMemory(self, trainsition):
        self.replayMemory.append(trainsition)
    
    def getQs(self, state):
        self.model.predict(np.array(state).reshape(-1,*state.shape)/255)[0]
    
    def train(self,terminalState,step):
        if(len(self.replayMemory) < REPLAY_MEMORY_SIZE):
            return
        
        minibatch= random.sample(self.replayMemory, BATCH_SIZE)
        
        currentState= np.array([transition[0] for transition in minibatch])
        
        currentQsList= self.model.predict(currentState)
        newCurrentStates= np.array([transition[3] for transition in minibatch])
        
        futureQsList = self.targetModel.predict(newCurrentStates)
        x=[]
        y=[]
        for index,(currentState,action, reward,newCurrentState,done) in enumerate(minibatch):
            if not done:
                maxFututeQ= np.max(futureQsList[index])
                newQ= reward+ DISCOUNT * maxFututeQ
            else:
                newQ= reward
            
            currentQs= currentQsList[index]
            currentQs[action]= newQ
            
            x.append(currentState)
            y.append(currentQs)
        self.model.fit(np.array(x), np.array(y),batch_size=BATCH_SIZE,verbose=0,epochs=1000,shuffle=False)
        print("done fitting model \n")
        
        
        if terminalState:
            self.targetUpdateCounter+=1
            
            
        if self.targetUpdateCounter>UPDATE_TARGET_EVERY:
            self.targetModel.set_weights(self.model.get_weights())
            self.targetUpdateCounter=0
            
    