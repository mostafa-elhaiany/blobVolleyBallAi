import pygame
import neat
import os
import numpy as np
from blob import Blob
from ball import Ball
from wall import Wall
from agent import DQNAgent

pygame.init()


windowWidth,windowHeight=1000,400
backGround= pygame.transform.scale( pygame.image.load( os.path.join( "imgs","bg.png" ) ),(windowWidth,windowHeight) )
pygame.font.init()
statFont=pygame.font.SysFont("comicsans",50)


EPISODES = 500

# Exploration settings
epsilon = 1  # not a constant, going to be decayed
EPSILON_DECAY = 0.99975
MIN_EPSILON = 0.001


class Env:
    LOSE_PENALTY=-25
    BALL_REWARD = 25
    OBSERVATION_SPACE_VALUES = 3
    ACTION_SPACE_SIZE = 3
    
    def reset(self):
        self.blob=Blob(20,windowHeight-110)
        self.ball=Ball(20,windowHeight//2)
        self.wall=Wall(windowWidth//2-20,windowHeight-250)
        self.enemyBlob=Blob(windowWidth-60,windowHeight-110)
   
        self.episode_step = 0

        observation = [self.ball.x,self.ball.y,self.blob.x,self.ball.velocity]
        return observation

    def step(self, action):
        self.episode_step += 1
        self.blob.move(action,0,windowWidth//2)
        
        
        self.enemyBlob.follow(self.ball,windowWidth//2,True)
        
        self.ball.move()
        self.ball.gravity(windowHeight)
        self.ball.collide(self.blob)
        self.ball.collide(self.enemyBlob)

        new_observation = [self.ball.x,self.ball.y,self.blob.x,self.ball.velocity]

        if(self.ball.y>=windowHeight-self.ball.height-10 and self.ball.x<windowWidth//2-30):
            reward=self.LOSE_PENALTY
        elif(self.ball.y>=windowHeight-self.ball.height-10 and self.ball.x>=windowWidth//2-30 and self.ball.x<windowWidth):
            reward=self.BALL_REWARD
        elif(self.ball.x<=10):
            reward=self.LOSE_PENALTY
        elif(self.ball.x>=windowWidth-10):
            reward=self.BALL_REWARD
        elif(abs(self.ball.x-self.blob.x)>(windowWidth//2%10)):
            reward=5
        else:
            reward=1

        done = False
        if reward == self.BALL_REWARD or reward == self.LOSE_PENALTY or self.episode_step >= 200:
            done = True

        return new_observation, reward, done

    

  

env = Env()




def drawWindow(window,blobs,balls,wall):
    window.blit(backGround,(0,0))
    wall.draw(window)
    for blob in blobs:
        blob.draw(window)
    for ball in balls:
        ball.draw(window)

    pygame.display.update()

def play():
    blob=Blob(20,windowHeight-110)
    ball=Ball(20,windowHeight//2)
    wall=Wall(windowWidth//2-20,windowHeight-250)
    enemyBlob=Blob(windowWidth-60,windowHeight-110)
    run = True
    window=pygame.display.set_mode((windowWidth,windowHeight))
    ballOn=False
    while run:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if(event.type==pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]):
                run=False
                pygame.quit()
                return
        
        keys=pygame.key.get_pressed()
        enemyBlob.follow(ball,windowWidth//2,True)
        #blob.follow(ball,windowWidth//2,False)
        
        if(keys[pygame.K_LEFT] and blob.x>blob.movement):
            blob.move(0,0,windowWidth//2)
        elif(keys[pygame.K_RIGHT] and blob.x<windowWidth//2-blob.movement-50):
                blob.move(1,0,windowWidth//2)
        else:
            blob.resetVelocity()
        if(keys[pygame.K_UP] and not blob.isJumping):
            blob.jump()
        
        if(keys[pygame.K_TAB]):
            ballOn=False
            ball=Ball(50,windowHeight//2)

        
        if(keys[pygame.K_SPACE]):
            ballOn= True
        
        blob.gravity(windowHeight)
        if(ballOn):
            ball.move()
            ball.gravity(windowHeight)
            ball.collide(blob)
            ball.collide(enemyBlob)
        wall.collide(blob)
        wall.collide(enemyBlob)
        wall.collide(wall)
        
        drawWindow(window,[blob,enemyBlob],[ball],wall)
def NEAT(genomes,config):
    networks=[]
    genes=[]
    blobs=[]
    balls=[]
    enemyBlobs=[]
    for _,g in genomes:
        net=neat.nn.FeedForwardNetwork.create(g,config)
        networks.append(net)
        blobs.append(Blob(20,windowHeight-110))
        balls.append(Ball(windowWidth-80,windowHeight//2))
        enemyBlobs.append(Blob(windowWidth-50,windowHeight-110))
        g.fitness=0
        genes.append(g)
    wall=Wall(windowWidth//2-20,windowHeight-250)
    run = True
    
    window=pygame.display.set_mode((windowWidth,windowHeight))
    while run:
        #pygame.time.delay(50)
        for event in pygame.event.get():
            if(event.type==pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]):
                run=False
                return
        for idx,enemyBlob in enumerate(enemyBlobs):
            enemyBlob.follow(balls[idx],windowWidth//2,True)
        if(len(blobs)==0):
            run= False
            break
        for idx,blob in enumerate(blobs):
            enemyBlobs[idx].gravity(windowHeight)
            ball=balls[idx]
            ball.move()
            ball.gravity(windowHeight)
            if(ball.collide(blob)):
                genes[idx].fitness+=5  
            ball.collide(enemyBlobs[idx])
            genes[idx].fitness+=0.1
            output=networks[idx].activate((ball.x,ball.y,blob.x,blob.velocity))
            if(output[0]>0.5):
                blob.move(0,0,windowWidth//2-40)
            elif(output[1]>0.5):
                blob.move(1,0,windowWidth//2-40)
            else:
                blob.resetVelocity()
            if(blob.x>=windowWidth//2-20 or blob.x<=0):
                genes[idx].fitness-=5
                
                
            blob.gravity(windowHeight)
        newNets=[]
        newGenes=[]
        newBlobs=[]
        newEnemies=[]
        newBalls=[]
        for idx,ball in enumerate(balls):
            if(abs(ball.x-blobs[idx].x)>(windowWidth//2%10)):
                genes[idx].fitness-=15

            
            if(ball.y>=windowHeight-ball.height-10 and ball.x<windowWidth//2-30):
                genes[idx].fitness-=5
                blobs[idx].score-=10
            elif(ball.y>=windowHeight-ball.height-10 and ball.x>windowWidth//2-30 and ball.x<windowWidth):
                genes[idx].fitness+=10
                newNets.append(networks[idx])
                newGenes.append(genes[idx])
                newBlobs.append(blobs[idx])
                newEnemies.append(enemyBlobs[idx])
                newBalls.append(Ball(50,windowHeight//2))
                blobs[idx].score+=20
            elif(ball.x<0 or ball.x>=windowWidth-40 ):
                genes[idx].fitness-=5
                
            else:
                genes[idx].fitness+=0.5
                blobs[idx].score+=10
                newNets.append(networks[idx])
                newGenes.append(genes[idx])
                newBlobs.append(blobs[idx])
                newEnemies.append(enemyBlobs[idx])
                newBalls.append(ball)
        
        bestBlobIdx=-1
        bestFitness=genes[0].fitness
        for idx,gene in enumerate(genes):
            if(gene.fitness>bestFitness):
                bestBlobIdx=idx
        
        
       
        drawWindow(window,[blobs[bestBlobIdx],enemyBlobs[bestBlobIdx]],[balls[bestBlobIdx]],wall)
        networks=newNets
        genes=newGenes
        blobs=newBlobs
        balls=newBalls
        enemyBlobs=newEnemies
        print(len(blobs))
        
        
                
                

def run(configPath):
    config= neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            configPath)
    population = neat.Population(config)
    
    population.add_reporter(neat.StdOutReporter(True))
    stats=neat.StatisticsReporter()
    population.add_reporter(stats)

    winner= population.run(NEAT,10)
    
    pygame.quit()
    #print(winner)
   
    
    
    
def DQN(episodes,epsilon,epsilonDeca):
    env=Env()
    agent= DQNAgent()
    #window=pygame.display.set_mode((windowWidth,windowHeight))
    episodeRewards=[]
    for episode in range(episodes):
        episode_reward = 0
        step = 1
        current_state = env.reset()
        done = False
        while not done:

        # This part stays mostly the same, the change is to query a model for Q values
            if np.random.random() > epsilon:
                # Get action from Q table
                
                action = np.argmax(agent.getQs(np.array(current_state)))
            else:
                # Get random action
                action = np.random.randint(0, env.ACTION_SPACE_SIZE)
    
            new_state, reward, done = env.step(action)
            episode_reward += reward

        
           #drawWindow(window,[env.blob,env.enemyBlob],[env.ball],env.wall)
    
            # Every step we update replay memory and train main network
            agent.updateReplyMemory((current_state, action, reward, new_state, done))
            agent.train(done, step)
            current_state = new_state
            step += 1
        episodeRewards.append(episode_reward)
        if episode % 10==0:
            averageReward = sum(episodeRewards)/len(episodeRewards)
            minReward = min(episodeRewards)
            maxReward = max(episodeRewards)
            print(f"replayMemo:{len(agent.replayMemory)}  avg:{averageReward} \n  min:{minReward}  \n  max:{maxReward} ")
        if epsilon > MIN_EPSILON:
            epsilon *= EPSILON_DECAY
            epsilon = max(MIN_EPSILON, epsilon)
    
    pygame.quit()
    
    
    
if __name__=="__main__":
    #localDirectory= os.path.dirname(__file__)
    #configPath= os.path.join(localDirectory,"config.txt")
    #run(configPath)
    play()
    
    #DQN(EPISODES,epsilon,EPSILON_DECAY)
    
