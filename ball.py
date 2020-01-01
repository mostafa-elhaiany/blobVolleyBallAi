import pygame
import os

ballImage= pygame.transform.scale( pygame.image.load( os.path.join( "imgs","ball.png" ) ), (50,50) )
RADIUS=10
class Ball:
    velocity=15
    
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.r=RADIUS
        self.height=0
        self.top=0
        self.bottom=0
        self.image=ballImage
        self.deltaX=0
        self.deltaY=0
        self.tickCount=0
        
        self.onTheLeft=True
        
        
    def move(self):
        self.x+=self.deltaX
        self.y+=self.deltaY
        
    
    def gravity(self,windowHeight):
        self.deltaY+=2
        self.tickCount+=1
        displacement = self.deltaY*self.tickCount + 1.5*(self.tickCount**2)
        if(displacement>=16):
             displacement=16
        elif(displacement<0):
            displacement-=2
            
        self.y+=displacement
        if(self.y>windowHeight-self.height):
            self.y=windowHeight-self.height-10
            self.deltaX=0
            
            
    def bounce(self,intersectionX):
        self.y+=self.velocity
        self.deltaY=-self.velocity
        if(intersectionX>=20):
            self.deltaX+=self.velocity
        elif(intersectionX<=18):
            self.deltaX-=self.velocity
        else:
            self.deltaX=0
        self.tickCount=0
        
    
    def draw(self, window):
        window.blit(self.image,(self.x,self.y))
        
    def getMask(self):
        return pygame.mask.from_surface(self.image)
        
    def collide(self,blob):
        blobMask=blob.getMask()
        ballMask= self.getMask()
        
        offset = ( round(self.x)-round(blob.x) , round(self.y) - round(blob.y)-10 )
        
        point=ballMask.overlap(blobMask,offset)
        if(point):
            self.bounce(point[0])
            return True
        
        return False
        
 