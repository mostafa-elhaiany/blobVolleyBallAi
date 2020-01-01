import pygame
import neat
import os
from blob import Blob
from ball import Ball
from wall import Wall

pygame.init()


windowWidth,windowHeight=1000,400
backGround= pygame.transform.scale( pygame.image.load( os.path.join( "imgs","bg.png" ) ),(windowWidth,windowHeight) )
pygame.font.init()
statFont=pygame.font.SysFont("comicsans",50)


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
        blob.follow(ball,windowWidth//2,False)
        
        if(keys[pygame.K_LEFT] and blob.x>blob.movement):
            blob.move(0)
        elif(keys[pygame.K_RIGHT] and blob.x<windowWidth//2-blob.movement-50):
                blob.move(1)
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
                genes[idx].fitness-=0.5
                
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
    
if __name__=="__main__":
    localDirectory= os.path.dirname(__file__)
    configPath= os.path.join(localDirectory,"config.txt")
    run(configPath)
