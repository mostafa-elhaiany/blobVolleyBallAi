import pygame
import os
from blob import Blob
from ball import Ball

pygame.init()
pygame.font.init()


backGround= pygame.transform.scale2x( pygame.image.load( os.path.join( "imgs","bg.png" ) ) )
windowWidth,windowHeight=500,400
statFont=pygame.font.SysFont("comicsans",50)


def drawWindow(window,blobs,balls):
    window.blit(backGround,(0,0))
    for blob in blobs:
        blob.draw(window)
    for ball in balls:
        ball.draw(window)

    pygame.display.update()

def main():
    blob=Blob(20,windowHeight-110)
    ball=Ball(20,windowHeight//2)
    enemyBlob=Blob(windowWidth-60,windowHeight-110)
    run = True
    window=pygame.display.set_mode((windowWidth,windowHeight))
    ballOn=False
    while run:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                run=False
                pygame.quit()
                return
        
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_LEFT]):
            blob.move(0)
        elif(keys[pygame.K_RIGHT]):
                blob.move(1)
       
        if(keys[pygame.K_UP] and not blob.isJumping):
            blob.jump()
        
        if(keys[pygame.K_SPACE]):
            ballOn= True
        
        blob.gravity(windowHeight)
        if(ballOn):
            ball.move()
            ball.gravity(windowHeight)
            print(ball.collide(blob) or ball.collide(enemyBlob) )
        drawWindow(window,[blob,enemyBlob],[ball])
            
main()
