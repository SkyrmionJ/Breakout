# gameplay.py
# Jason Sze (jks255), Ya Xin Huang (yh398)
# 12-10-2014
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Gameplay represent a single game.  If you want to restart a new game,
you are expected to make a new instance of Gameplay.

The subcontroller Gameplay manages the paddle, ball, and bricks.  These are model
objects.  The ball and the bricks are represented by classes stored in models.py.
The paddle does not need a new class (unless you want one), as it is an instance
of GRectangle provided by game2d.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Gameplay can only access attributes in models.py via getters/setters
# Gameplay is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Gameplay(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It
    animates the ball, removing any bricks as necessary.  When the game is
    won, it stops animating.  You should create a NEW instance of 
    Gameplay (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.
    
    INSTANCE ATTRIBUTES:
        _wall   [BrickWall]:  the bricks still remaining 
        _paddle [GRectangle]: the paddle to play with 
        _ball [Ball, or None if waiting for a serve]: 
            the ball to animate
        _last [GPoint, or None if mouse button is not pressed]:  
            last mouse position (if Button pressed)
        _playerlives  [int >= 0]:   the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in call Breakout. It is okay if you do, but
    you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or
    setter for any attribute that you need to access in Breakout.  Only add
    the getters and setters that you need for Breakout.
    
    You may change any of the attributes above as you see fit. For example, you
    might want to make a Paddle class for your paddle.  If you make changes,
    please change the invariants above.  Also, if you add more attributes,
    put them and their invariants below.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _points [int>=0]: the number of points the player has accumulated
        _score  [Instance of GLabel]: Used to display the _points of the player
    """
    
    def getPlayerLives(self):
        """Getter that returns the attribute _playerlives"""
        return self._playerlives
    
    def getWall(self):
        """Getter that returns the attribute _wall"""
        return self._wall
    
    def __init__(self):
        """Initializes a game.
        
        Will initialize all attributes pertaining to a single round of Breakout"""
        self._wall = BrickWall()
        self._paddle = GRectangle(center_x=  GAME_WIDTH/2, y = PADDLE_OFFSET,
                                  width = PADDLE_WIDTH, height = PADDLE_HEIGHT,
                                  linecolor = colormodel.WHITE,
                                  fillcolor = colormodel.WHITE)
        self._ball = Ball(GEllipse())
        self._last = None
        self._playerlives = NUMBER_TURNS
        self._points = 0
        self._score = GLabel(text='Score: 0', x=2, y=2,
                             fillcolor = colormodel.BLACK,
                             linecolor = colormodel.WHITE)
    
    def draw(self,view):
        """Draws gameplay attributes into view
        
        Precondition: view is an instance of GView
        """
        self._score.draw(view)
        self._wall.draw(view)
        self._paddle.draw(view)
        self._ball.draw(view)
    
    def updatePaddle(self, touch):
        """Method used to check how much the paddle should move and move the paddle
        
        Checks for a click and drag movement and changes the position of the paddle
        by exactly how much the mouse position changes.
        Ensures that the paddle will not move beyond the game borders.
        
        Precondition: touch is a tuple within the game borders"""
        if (touch is not None) and (self._last is not None):
            px=self._paddle.x+touch.x-self._last.x
            if px <= 0:
                self._paddle.x = 0
            elif px >= GAME_WIDTH-PADDLE_WIDTH:
                self._paddle.x = GAME_WIDTH-PADDLE_WIDTH
            else:
                self._paddle.x = px
        self._last = touch

    def moveBall(self, sound):
        """Method used to move the ball and runs a series of methods after each movement.
        
        Precondition: sound is either True or False"""
        self._ball.changePosition()
        s = self._ball.checkWall()
        if s == 'end':
            self._playerlives -= 1
        x = self._getCollidingObject()
        if x == self._paddle:
            self._hitPaddle(sound)
        elif len(x) != 0:
            self._ball.negate_vy()
            for i in x:
                self._updateScore()
                self._wall.removeBrick(i)
            if sound == True:   
                piano = Sound('Subsynth-modfilter.ogg')
                piano.play()
        if self._wall.getBricks() == []:
            self._playerlives = 0

    def _getCollidingObject(self):
        """Returns: GObject that has collided with the ball
    
        This method checks the four corners of the ball, one at a 
        time. If one of these points collides with either the paddle 
        or a brick, it stops the checking immediately and returns the 
        object involved in the collision. It returns None if no 
        collision occurred."""

        if self._ball.getvy() < 0:
            if self._paddle.contains(self._ball.x, self._ball.y):
                return self._paddle
            elif self._paddle.contains(self._ball.x + BALL_DIAMETER, self._ball.y):
                return self._paddle
            elif self._paddle.contains(self._ball.x, self._ball.y + BALL_DIAMETER):
                return self._paddle
            elif self._paddle.contains(self._ball.x + BALL_DIAMETER, self._ball.y + BALL_DIAMETER):
                return self._paddle
        
        p=[self._wall.getBrickAt(self._ball.x, self._ball.y),
           self._wall.getBrickAt(self._ball.x + BALL_DIAMETER, self._ball.y),
           self._wall.getBrickAt(self._ball.x, self._ball.y + BALL_DIAMETER),
           self._wall.getBrickAt(self._ball.x + BALL_DIAMETER, self._ball.y + BALL_DIAMETER)]
        k=[]
        for i in p:
            if i is not None:
                k.append(i)
        return list(set(k))
    
    def resetBall(self):
        """ Helper method used to reset _ball to its original position"""
        self._ball = Ball(GEllipse())

    def resetPaddle(self):
        """ Helper method used to reset _paddle to its original position"""
        self._paddle = GRectangle(center_x=  GAME_WIDTH/2, y = PADDLE_OFFSET,
                                  width = PADDLE_WIDTH, height = PADDLE_HEIGHT,
                                  linecolor = colormodel.WHITE,
                                  fillcolor = colormodel.WHITE)

    def _hitPaddle(self, sound):
        """ Helper method used whenever the ball hits the paddle
        
        If the ball hits the paddle, the y-velocity of the ball reverses to bounce
        it back up.
        if the ball is coming from the left and hits the left 1/3 of the paddle,
        it will bounce back to the left.
        If the ball is coming from the right and hits the right 1/3 of the paddle,
        it will bounce back to the right.
        If the ball hit the paddle and _sound from breakout is True, a sound will play
        Precondition: sound is either True or False"""
        if sound == True:
            bouncesound = Sound('bounce.wav')
            bouncesound.play()
        self._ball.negate_vy()
        left = self._paddle.x
        right = self._paddle.x + PADDLE_WIDTH
        p1 = self._paddle.x + PADDLE_WIDTH/3
        p3 = self._paddle.x + 2*(PADDLE_WIDTH/3)

        if (self._ball.getvx() > 0) and (left <= (self._ball.x+BALL_DIAMETER) <= p1):
            self._ball.negate_vx()
        if (self._ball.getvx() < 0) and (p3 <= self._ball.x <= right):
            self._ball.negate_vx()

    def _updateScore(self):
        """Helper method used when a brick is hit by the paddle
        
        It increments _points by one and updates the _score label to reflect the
        current score"""
        self._points += 1
        k='Score: ' + `self._points`
        self._score = GLabel(text=k, x=2, y=2, fillcolor = colormodel.BLACK, linecolor = colormodel.WHITE)