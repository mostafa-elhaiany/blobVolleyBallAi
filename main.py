import pygame
import os
from blob import Blob
from ball import Ball
from wall import Wall

pygame.init()


windowWidth,windowHeight=500,400
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
        
        if(keys[pygame.K_LEFT]):
            blob.move(0)
        elif(keys[pygame.K_RIGHT]):
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
 
if __name__=="__main__":           
    play()
