import pygame
import os

WALL_WIDTH=50
WALL_HEIGHT=250
wallImage= pygame.transform.scale( pygame.image.load( os.path.join( "imgs","wall.png" ) ),(WALL_WIDTH,WALL_HEIGHT) )
class Wall:
    def __init__(self,x,y):
        self.x=x
        self.width=WALL_WIDTH
        self.y=y
        self.height=WALL_HEIGHT
        self.image = wallImage
        self.passed=False
        
    def draw(self, window):
        window.blit(self.image,(self.x,self.y))
        
    def getMask(self):
        return pygame.mask.from_surface(self.image)
        
    def collide(self,collider):
        colliderMask=collider.getMask()
        myMask= self.getMask()
        
        offset = ( round(self.x-collider.x) , round(self.y - collider.y)-collider.height )
        
        point=colliderMask.overlap(myMask,offset)
        
        if(point):
            collider.bounce(point[0],0,0)
            print('collided')
            return True
        
        return False
        