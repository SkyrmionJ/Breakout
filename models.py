# models.py
# Jason Sze (jks255), Ya Xin Huang (yh398)
# 12-10-2014
"""Models module for Breakout

This module contains the model classes for the Breakout game. Anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, both paddle
and individual bricks can just be instances of GRectangle.  There is no need for a
new class in the case of these objects.

We only need a new class when we have to add extra features to our objects.  That
is why we have classes for Ball and BrickWall.  Ball is usually a subclass of GEllipse,
but it needs extra methods for movement and bouncing.  Similarly, BrickWall needs
methods for accessing and removing individual bricks.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything in any module other than
# constants.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Gameplay should pass it as a argument when it
# calls the method.


class BrickWall(object):
    """An instance represents the layer of bricks in the game.  When the wall is
    empty, the game is over and the player has won. This model class keeps track of
    all of the bricks in the game, allowing them to be added or removed.
    
    INSTANCE ATTRIBUTES:
        _bricks [list of GRectangle, can be empty]:
            This is the list of currently active bricks in the game.  When a brick
            is destroyed, it is removed from the list.
    
    As you can see, this attribute is hidden.  You may find that you want to access 
    a brick from class Gameplay. It is okay if you do that,  but you MAY NOT 
    ACCESS THE ATTRIBUTE DIRECTLY. You must use a getter and/or setter for any 
    attribute that you need to access in GameController.  Only add the getters and 
    setters that you need.
    
    We highly recommend a getter called getBrickAt(x,y).  This method returns the first
    brick it finds for which the point (x,y) is INSIDE the brick.  This is useful for
    collision detection (e.g. it is a helper for _getCollidingObject).
    
    You will probably want a draw method too.  Otherwise, you need getters in Gameplay
    to draw the individual bricks.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    def getBricks(self):
        """Getter that returns the attribute _bricks"""
        return self._bricks
    
    def __init__(self):
        """Initializes the brickwall object
        
        Will create all the bricks in the brickwall based on the BRICK_ROWS and
        BRICKS_IN_ROW constants"""
        self._bricks=[]
        for i in range(BRICK_ROWS):
            px=BRICK_SEP_H/2
            py=620 - BRICK_Y_OFFSET - i*(BRICK_HEIGHT + BRICK_SEP_V)
            for k in range(BRICKS_IN_ROW):
                self._bricks.append(GRectangle(x=px, y=py,
                                               width=GAME_WIDTH / BRICKS_IN_ROW - BRICK_SEP_H,
                                               height=8,  linecolor=ROW_COLORS[i%10],
                                               fillcolor=ROW_COLORS[i%10]))
                px += BRICK_WIDTH + BRICK_SEP_H
    
    def draw(self, view):
        """ Draws the Brickwall
        
        Precondition: view is an instance of GView"""
        for i in self._bricks:
            i.draw(view)
    
    def getBrickAt(self,x,y):
        """ Method used to return the brick, a GRectangle, at a specified coordinate
        
        Precondition: x is a number between 0 and GAME_WIDTH
                      y is a number between 0 and GAME_HEIGHT"""
        for i in self._bricks:
            if i.contains(x,y):
                return i

    def removeBrick(self, brick):
        """ Method used to remove a specific brick from _bricks
        
        Precondition: brick is an instance of GRectangle"""
        self._bricks.remove(brick)


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Gameplay will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    In addition you must add the following methods in this class: an __init__
    method to set the starting velocity and a method to "move" the ball.  The
    __init__ method will need to use the __init__ from GEllipse as a helper.
    The move method should adjust the ball position according to  the velocity.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    def getvx(self):
        """Getter that returns the attribute _vx"""
        return self._vx
    
    def getvy(self):
        """Getter that returns the attribute _vy"""
        return self._vy
    
    def __init__(self, center_x = GAME_WIDTH/2,
                          center_y = GAME_HEIGHT/2,
                          width = BALL_DIAMETER,
                          height = BALL_DIAMETER,
                          fillcolor = colormodel.WHITE):
        """ Initializes the ball object.
        
        Initiaizes a GEllipse and the ball's x and y velocities"""
        GEllipse.__init__(self, center_x = GAME_WIDTH/2,
                          center_y = GAME_HEIGHT/2,
                          width = BALL_DIAMETER,
                          height = BALL_DIAMETER,
                          fillcolor = colormodel.WHITE)
        self._vx = random.uniform(1.0, 5.0) * random.choice([-1,1])
        self._vy = -5.0

    def changePosition(self):
        """ Changes the position of the ball
        The x coordinate of the ball is changed by the velocity of x and
        the y coordinate of the ball is changed by the velocity of y."""
        self.x += self._vx
        self.y += self._vy

    def negate_vx(self):
        """ Helper method that negates _vx, the x velocity"""
        self._vx = -self._vx       

    def negate_vy(self):
        """ Helper method that negates _vy, the y velocity"""
        self._vy = -self._vy    

    def checkWall(self):
        """ Helper method that checks if the ball hits the border of the game.
        If the ball hits the left or right borders, then the ball's x velocity
        is negated. If the ball hits the top border, then the ball's y velocity
        is negated. If the ball hits the bottom border, then it returns 'end',
        signaling the end of a round"""
        if (self._vy > 0) and (self.y + BALL_DIAMETER >= GAME_HEIGHT):
            self.negate_vy()
        elif (self._vy < 0) and (self.y <= 0):
            return 'end'
        elif (self._vx > 0) and (self.x + BALL_DIAMETER >= GAME_WIDTH):
            self.negate_vx()
        elif (self._vx < 0) and (self.x <= 0):
            self.negate_vx()