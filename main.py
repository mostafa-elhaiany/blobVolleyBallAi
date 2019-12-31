import pygame
import os
from blob import Blob

backGround= pygame.transform.scale2x( pygame.image.load( os.path.join( "imgs","bg.png" ) ) )
windowWidth,windowHeight=500,400

pygame.init()
pygame.font.init()

statFont=pygame.font.SysFont("comicsans",50)


def drawWindow(window,blobs):
    window.blit(backGround,(0,0))
    for blob in blobs:
        blob.draw(window)

    pygame.display.update()

def main():
    blob=Blob(20,windowHeight-110)
    enemyBlob=Blob(windowWidth-60,windowHeight-110)
    run = True
    window=pygame.display.set_mode((windowWidth,windowHeight))
    while run:
        pygame.time.delay(20)
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                run=False
                pygame.quit()
                quit()
            keys=pygame.key.get_pressed()
            if(keys[pygame.K_LEFT]):
                blob.move(0)
            elif(keys[pygame.K_RIGHT]):
                blob.move(1)
            if(keys[pygame.K_SPACE] and not blob.isJumping ):
                blob.jump()
        blob.gravity(windowHeight)
        drawWindow(window,[blob,enemyBlob])
            
if __name__=='__main__':
    main()        
