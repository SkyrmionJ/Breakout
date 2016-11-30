# breakout.py
# Jason Sze (jks255), Ya Xin Huang (yh398)
# 12-10-2014
"""Primary module for Breakout application

This module contains the App controller class for the Breakout application.
There should not be any need for additional classes in this module.
If you need more classes, 99% of the time they belong in either the gameplay
module or the models module. If you are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from gameplay import *
from game2d import *


# PRIMARY RULE: Breakout can only access attributes in gameplay.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is a Breakout App
    
    This class extends GameApp and implements the various methods necessary 
    for processing the player inputs and starting/running a game.
    
        Method init starts up the game.
        
        Method update either changes the state or updates the Gameplay object
        
        Method draw displays the Gameplay object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the init method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Gameplay.
    Gameplay should have a minimum of two methods: updatePaddle(touch) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView, it is inherited from GameApp]:
            the game view, used in drawing (see examples from class)
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
            the current state of the game represented a value from constants.py
        _last   [GPoint, or None if mouse button is not pressed]:
            the last mouse position (if Button was pressed)
        _game   [GModel, or None if there is no game currently active]: 
            the game controller, which manages the paddle, ball, and bricks
    
    ADDITIONAL INVARIANTS: Attribute _game is only None if _state is STATE_INACTIVE.
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _message            [Instance of GLabel]
            used as the welcome messagefor the game
        _touch              [GPoint, or None if mouse button is not currently held down]
            whether the mouse button is currently pressed down or not
        _countdownTime      [int]
            accumulator for the countdown portion of the game
        _countdownMessage   [Instance of GLabel]
            used as the 3 second countdown during _Countdown
        _pausedMessage      [Instance of GLabel]
            used as the message when the game is paused or complete
        _sound              [True or False]
            True if sounds are on, False otherwise
        _soundImage         [Instance of GImage]
            used to display the sound icon
        _background         [Instance of GRectangle]
            used as the background of the game
    """
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # GAMEAPP METHODS
    def init(self):
        """Initialize the game state.
        
        This method is distinct from the built-in initializer __init__.
        This method is called once the game is running. You should use
        it to initialize any game specific attributes.
        
        This method should initialize any state attributes as necessary 
        to statisfy invariants. When done, set the _state to STATE_INACTIVE
        and create a message (in attribute _mssg) saying that the user should 
        press to play a game."""
        self._last = None
        self._game = None
        self._state = STATE_INACTIVE
        self._message = GLabel(text='Breakout\n\nClick To Begin\n\nGood Luck',
                               font_size=24,x=GAME_WIDTH / 2.0, y=GAME_HEIGHT*(2.0/3.0),
                               halign='center', valign='middle', linecolor=colormodel.WHITE)
        self._touch = None
        self._countdownTime = 0
        self._countdownMessage = GLabel(text='3', font_size=40,x=GAME_WIDTH / 2.0,
                                        y=GAME_HEIGHT*(2.0/3.0), halign='center',
                                        valign='middle', linecolor=colormodel.WHITE)
        self._pausedMessage = GLabel()
        self._sound = True
        self._soundImage = GImage(x=GAME_WIDTH-32, y=0, width=32, height=22,
                                  source='whitevolumeon.png')
        self._background = GRectangle(x=0, y=0, width=GAME_WIDTH, height=GAME_HEIGHT,
                                      fillcolor=colormodel.BLACK, linecolor=colormodel.BLACK)
    
    def update(self,dt):
        """Animate a single frame in the game.
        
        It is the method that does most of the work. Of course, it should
        rely on helper methods in order to keep the method short and easy
        to read.  Some of the helper methods belong in this class, but most
        of the others belong in class Gameplay.
        
        The first thing this method should do is to check the state of the
        game. We recommend that you have a helper method for every single
        state: STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE.
        The game does different things in each state.
        
        In STATE_INACTIVE, the method checks to see if the player clicks
        the mouse (_last is None, but view.touch is not None). If so, it 
        (re)starts the game and switches to STATE_COUNTDOWN.
        
        STATE_PAUSED is similar to STATE_INACTIVE. However, instead of 
        restarting the game, it simply switches to STATE_COUNTDOWN.
        
        In STATE_COUNTDOWN, the game counts down until the ball is served.
        The player is allowed to move the paddle, but there is no ball.
        Paddle movement should be handled by class Gameplay (NOT in this class).
        This state should delay at least one second.
        
        In STATE_ACTIVE, the game plays normally.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Gameplay (NOT in this class).
        Gameplay should have methods named updatePaddle and updateBall.
        
        While in STATE_ACTIVE, if the ball goes off the screen and there
        are tries left, it switches to STATE_PAUSED.  If the ball is lost 
        with no tries left, or there are no bricks left on the screen, the
        game is over and it switches to STATE_INACTIVE.  All of these checks
        should be in Gameplay, NOT in this class.
        
        While in STATE_RESET, breakout prepares for the start of a new game, and
        a click of the button will bring you back to STATE_INACTIVE.
        
        While in STATE_COMPELTE, the current game is over and it will display
        a message indicating whether you won or lost. A click of the button will
        switch you to STATE_RESET and preprs for a new game.
        
        You are allowed to add more states if you wish. Should you do so,
        you should describe them here.
        
        Precondition: dt is the time since last update (a float).  This
        parameter can be safely ignored. It is only relevant for debugging
        if your game is running really slowly. If dt > 0.5, you have a 
        framerate problem because you are trying to do something too complex."""
        #print self._state
        if self._state == STATE_INACTIVE:
            self._inactive()
        elif self._state == STATE_COUNTDOWN:
            self._countdown()
        elif self._state == STATE_PAUSED:
            self._paused()
        elif self._state == STATE_ACTIVE:
            self._active()
        elif self._state == STATE_RESET:
            self._reset()
        elif self._state == STATE_COMPLETE:
            self._complete()
    
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject. 
        To draw a GObject g, simply use the method g.draw(view).  It is 
        that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are
        attributes in Gameplay. In order to draw them, you either need to
        add getters for these attributes or you need to add a draw method
        to class Gameplay.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        self._background.draw(self.view)
        if self._state == STATE_INACTIVE:
            self._message.draw(self.view)
        if self._state == STATE_COUNTDOWN:
            self._game.draw(self.view)
            self._countdownMessage.draw(self.view)
            self._soundImage.draw(self.view)
        if self._state == STATE_ACTIVE:
            self._game.draw(self.view)
            self._soundImage.draw(self.view)
        if self._state == STATE_PAUSED:
            self._game.draw(self.view)
            self._pausedMessage.draw(self.view)
        if self._state == STATE_RESET:
            self._message.draw(self.view)
        if self._state == STATE_COMPLETE:
            self._game.draw(self.view)
            self._pausedMessage.draw(self.view)

    def _click(self):
        """Recognizes any mouse click and records the coordinate into the
        touch attribute.
        
        Helper method used by any method that requires mouse click input"""
        self._touch = self.view.touch

    def _movePaddle(self):
        """ Helper function that moves the paddle
        """
        self._click()
        self._game.updatePaddle(self._touch)
        self._last = self._touch
    
    def _inactive(self):
        """Helper method used when _state is STATE_INACTIVE
        
        If a mouse click occurs, changes the _state to STATE_COUNTDOWN, and
        creates a new game."""
        self._click()
        if self._last is None and self._touch is not None:
            self._state = STATE_COUNTDOWN
            self._game = Gameplay()
        self._last = self._touch

    def _countdown(self):
        """ Helper method used when _state is STATE_COUNTDOWN
        
        Counts down from 3 and changes the _state to STATE_ACTIVE"""
        self._soundhelper()
        self._movePaddle()
        if 0 <= self._countdownTime < 60:
                k='3'
        elif 60 <= self._countdownTime < 120:
                k='2'
        elif 120 <= self._countdownTime < 180:
                k='1'
        self._countdownMessage=GLabel(text=k, font_size=40,x=GAME_WIDTH / 2.0,
                               y=GAME_HEIGHT*(2.0/3.0), halign='center',
                               valign='middle', linecolor=colormodel.WHITE)
        self._countdownTime += 1
        if self._countdownTime == 180:
            self._state = STATE_ACTIVE

    def _active(self):
        """ Helper method used when _state is STATE_ACTIVE
        
        Checks for clicks to the mute button, moves the paddle and ball, and checks
        for STATE_PAUSED and STATE_COMPLETE scenarios"""
        self._soundhelper()
        k = self._game.getPlayerLives()
        self._movePaddle()
        self._game.moveBall(self._sound)
        if self._game.getPlayerLives() == 0:
            self._state = STATE_COMPLETE
        elif self._game.getPlayerLives() < k:
            self._state = STATE_PAUSED

    def _paused(self):
        """ Helper method used when _state is STATE_PAUSED
        
        Shows a lives remaining message and checks for a click.
        If a click occurs, sets _state to STATE_COUNTDOWN and continues the game"""
        self._last = self._touch
        m = 'You have '+`self._game.getPlayerLives()`+' lives remaining.\nClick to continue'
        f = 25
        self._click()
        if self._last is None and self._touch is not None:
            self._state = STATE_COUNTDOWN
            self._game.resetBall()
            self._game.resetPaddle()
            m = ''
        self._last = self._touch
        self._countdownTime = 0
        self._countdownMessage = GLabel(text='3', font_size=40,x=GAME_WIDTH / 2.0,
                                            y=GAME_HEIGHT*(2.0/3.0), halign='center',
                                            valign='middle', linecolor=colormodel.WHITE)
        self._pausedMessage = GLabel(text=m,font_size=f,x=GAME_WIDTH / 2.0,
                                     y=GAME_HEIGHT*(2.0/3.0), halign='center',
                                     valign='middle', linecolor=colormodel.WHITE)

    def _complete(self):
        """ Helper method used when _state is STATE_COMPLETE
        
        Shows a message for either winning or losing, and checks for a click
        If a click occurs, the helper playAgain runs."""
        self._last = self._touch
        if self._game.getWall().getBricks() == []:
            m = 'Congratulations!\nYou Won\n\nClick to play again'
            f = 30
            h = GAME_HEIGHT*(2.0/3.0)
            self._playAgain()
        elif self._game.getPlayerLives() == 0:
            m = 'Game Over\nClick to try again'
            f = 30
            h = GAME_HEIGHT*(2.0/3.0)-10
            self._playAgain()
        self._countdownTime = 0
        self._countdownMessage = GLabel(text='3', font_size=40,x=GAME_WIDTH / 2.0,
                                            y=GAME_HEIGHT*(2.0/3.0), halign='center',
                                            valign='middle', linecolor=colormodel.WHITE)
        self._pausedMessage = GLabel(text=m,font_size=f,x=GAME_WIDTH / 2.0,
                                     y=h, halign='center', valign='middle',
                                     linecolor=colormodel.WHITE)
    
    def _playAgain(self):
        """Helper used to check for a click and set the _state to STATE_RESET"""
        self._click()
        if self._last is None and self._touch is not None:
            self._state = STATE_RESET

    def _reset(self):
        """Helper method used when _state is STATE_RESET
        
        Checks for a click and if clicked, sets _state to STATE_INACTIVE"""
        self._click()
        if self._touch is None:
            self._state = STATE_INACTIVE

    def _soundhelper(self):
        """Helper method used for the functionality of the sound button
        Checks for a click at the position of the sound button and inverts _sound
        such that it is either on or off"""
        self._click()
        if self._last is None and self._touch is not None:
            if self._soundImage.contains(self._touch.x, self._touch.y):
                self._sound = not self._sound
                if self._soundImage.source == 'whitevolumeon.png':
                    self._soundImage.source = 'whitevolumenull.png'
                else:
                    self._soundImage.source = 'whitevolumeon.png'