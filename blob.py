import pygame
import os

        
BLOB_HEIGHT=100
BLOB_WIDTH=50
JUMP_HEIGHT=-12
BLOB_IMAGE = pygame.transform.scale( pygame.image.load( os.path.join( "imgs","blob.png" ) ), (BLOB_WIDTH,BLOB_HEIGHT) )

class Blob:
    def __init__(self,x,y): #the starting position of the bird
        self.x=x
        self.y=y
        self.tickCount=0 
        self.velocity=0
        self.movement=10
        self.height=BLOB_HEIGHT
        self.width=BLOB_WIDTH
        self.image=BLOB_IMAGE
        self.jumpCount=0
        self.jumpVel=0
        self.isJumping=False
        self.score=0
        
    def follow(self, ball,xBound,enemy):
        if(ball.x>xBound and enemy):
            self.x=ball.x+20
        if(ball.x<xBound and not enemy):
            self.x=ball.x-20
                
    
    def jump(self):
        self.jumpVel=JUMP_HEIGHT
        self.tickCount=0
        self.isJumping=True
        
    def gravity(self,windowHeight):
        self.tickCount+=1
        displacement = self.jumpVel*self.tickCount + 1.5*(self.tickCount**2)
        if(displacement>=16):
             displacement=16
        elif(displacement<0):
            displacement-=2
            
        self.y+=displacement
        if(self.y>windowHeight-self.height):
            self.isJumping=False
            self.y=windowHeight-self.height-10
            self.jumpVel=0
            
    def bounce(self,colliderVel,colliderUpVel):
        pass
    
    def move(self,direction):
        if(direction==0):
            self.x-=self.movement+self.velocity
        elif(direction==1):
            self.x+=self.movement+self.velocity
            
        self.velocity+=1
        
    def resetVelocity(self):
         self.velocity=0
       
                
        
    def draw(self, window):
        rectangle= self.image.get_rect(center=self.image.get_rect(topleft=(self.x,self.y)).center)
        window.blit(self.image,rectangle)
    
    
    def getMask(self):
        return pygame.mask.from_surface(self.image)

    
