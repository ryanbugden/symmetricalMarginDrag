from mojo.events import addObserver, removeObserver, extractNSEvent

'''
Option-dragging one margin will change the other margin accordingly.

Ryan Bugden
Idea: Frank Griesshammer

v0.1.0:   2019.12.20
'''

gutt = 10

class symmetricalMarginDrag():
    
    def __init__(self):
        self.font = None
        self.glyph = None
        
        self.right_driving =  False
        self.left_driving =  False
        
        self.optionDown = 0
        
        addObserver(self, 'mouseUp', 'mouseUp') 
        addObserver(self, 'mouseDown', 'mouseDown')
        addObserver(self, 'modifiersChanged', 'modifiersChanged')
        
        
    def currentGlyphChanged(self, notification):
        self.glyph = notification['glyph']
        self.font = self.glyph.font


    def mouseDragged(self, notification):
        if self.glyph:
            if self.optionDown != 0:
            
                print(notification)
                self.glyph = notification['glyph']
                self.pos_x = notification['point'].x
            
                if self.right_driving == True:
                    self.right_delta = self.glyph.rightMargin - self.pre_dr_right
                    if self.right_delta != self.glyph.rightMargin:
                        self.glyph.leftMargin = self.pre_dr_left + self.right_delta
                elif self.left_driving == True:
                    self.left_delta = self.glyph.leftMargin - self.pre_dr_left
                    if self.left_delta != self.glyph.leftMargin:
                        self.glyph.rightMargin = self.pre_dr_right + self.left_delta
                    
                self.glyph.changed()
                    
                    
    def mouseUp(self, notification):
        print(notification)
        self.glyph = notification['glyph']
        if self.glyph:
            if self.optionDown != 0:
                # post-drag numbers
                self.left_delta = self.glyph.leftMargin - self.pre_dr_left
                self.right_delta = self.glyph.rightMargin - self.pre_dr_right
        
                if self.right_driving == True:
                    self.glyph.leftMargin = self.pre_dr_left + self.right_delta
                elif self.left_driving == True:
                    self.glyph.rightMargin = self.pre_dr_right + self.left_delta
        
                self.right_driving = self.left_driving = False
                removeObserver(self, 'mouseDragged')


    def mouseDown(self, notification):
        print(notification)
        self.glyph = notification['glyph']
        if self.glyph:
            if self.optionDown != 0:
            
                addObserver(self, 'mouseDragged', 'mouseDragged')
            
                print(notification)
                self.glyph = notification['glyph']
                self.pos_x = notification['point'].x
            
                if self.pos_x > self.glyph.width/2 + gutt/2:
                    self.right_driving = True
                    print("RSB is driving.", self.pos_x, "greater than", self.glyph.width/2 + gutt/2)
                elif self.pos_x < self.glyph.width/2 - gutt/2:
                    self.left_driving = True
                    print("LSB is driving.", self.pos_x, "less than", self.glyph.width/2 - gutt/2)
        
                # pre-drag numbers
                self.pre_dr_left = self.glyph.leftMargin
                self.pre_dr_right = self.glyph.rightMargin
        
        
    def modifiersChanged(self, event):
        ns_event = extractNSEvent(event)
        print(ns_event)
        self.optionDown = ns_event['optionDown']
        
    
    
symmetricalMarginDrag()

