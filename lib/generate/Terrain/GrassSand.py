''' This is the Sand -> Water terraforming class.
Used in the map generation script

'''

class GrassSand:
    def edges(self, x, y):
        ## Up and Down
        if self.layer[x, y] == self.key_pieces[5] and self.layer[x, y-1] == self.key_pieces[41]:
            self.layer[x, y] = self.key_pieces[56] # Up
        if self.layer[x, y] == self.key_pieces[5] and self.layer[x, y+1] == self.key_pieces[41]:
            self.layer[x, y] = self.key_pieces[62] # Down
        ## Left and Right
        if self.layer[x, y] == self.key_pieces[5] and self.layer[x-1, y] == self.key_pieces[41]:
            self.layer[x, y] = self.key_pieces[58] # Left
        if self.layer[x, y] == self.key_pieces[5] and self.layer[x+1, y] == self.key_pieces[41]:
            self.layer[x, y] = self.key_pieces[60] # Right
        return self.layer

    def t(self, x, y):
        if self.layer[x, y] == self.key_pieces[60] and self.layer[x, y+1] == self.key_pieces[62]:
            self.layer[x, y+1] = self.key_pieces[60]
        ## Right Facing T
        if self.layer[x, y] == self.key_pieces[60] and self.layer[x, y+1] == self.key_pieces[62]:
            self.layer[x, y+1] = self.key_pieces[60]
        if self.layer[x, y] == self.key_pieces[60] and self.layer[x, y-1] == self.key_pieces[56]: 
            self.layer[x, y-1] = self.key_pieces[60]
        ## Left Facing T
        if self.layer[x, y] == self.key_pieces[58] and self.layer[x, y+1] == self.key_pieces[62]:
            self.layer[x, y+1] = self.key_pieces[58]
        if self.layer[x, y] == self.key_pieces[58] and self.layer[x, y-1] == self.key_pieces[56]: 
            self.layer[x, y-1] = self.key_pieces[58]
        ## Downward Facing T
        if self.layer[x, y] == self.key_pieces[62] and self.layer[x+1, y] == self.key_pieces[60]:
            self.layer[x+1, y] = self.key_pieces[41]                                   
        if self.layer[x, y] == self.key_pieces[62] and self.layer[x-1, y] == self.key_pieces[58]:  
            self.layer[x-1, y] = self.key_pieces[41]
        ## Upward Facing T
        if self.layer[x, y] == self.key_pieces[56] and self.layer[x+1, y] == self.key_pieces[60]:
            self.layer[x+1, y] = self.key_pieces[41]                                   
        if self.layer[x, y] == self.key_pieces[56] and self.layer[x-1, y] == self.key_pieces[58]:  
            self.layer[x-1, y] = self.key_pieces[41]
        ## Extra Ts
        if self.layer[x, y] == self.key_pieces[58] and self.layer[x+1, y] == self.key_pieces[56]:
            self.layer[x+1, y] = self.key_pieces[41]                                   
        if self.layer[x, y] == self.key_pieces[58] and self.layer[x-1, y] == self.key_pieces[58]:  
            self.layer[x-1, y] = self.key_pieces[41]
        return self.layer
    
    def corners(self, x, y):
        ## Inner Corners
        if self.layer[x, y] == self.key_pieces[62] and self.layer[x-1, y+1] == self.key_pieces[60]:
            self.layer[x-1, y] = self.key_pieces[64] # Top-Left
            
        if self.layer[x, y] == self.key_pieces[62] and self.layer[x+1, y+1] == self.key_pieces[60]:  
            self.layer[x-1, y] = self.key_pieces[64] # Top-Right
        if self.layer[x, y] == self.key_pieces[62] and self.layer[x+1, y+1] == self.key_pieces[58]:  
            self.layer[x+1, y] = self.key_pieces[64] # Top-Right
            
        if self.layer[x, y] == self.key_pieces[56] and self.layer[x+1, y-1] == self.key_pieces[58]:
            self.layer[x+1, y] = self.key_pieces[67] # Bottom-Right
        if self.layer[x, y] == self.key_pieces[62] and self.layer[x+1, y+1] == self.key_pieces[58]: 
            self.layer[x+1, y] = self.key_pieces[66] # Bottom-Right
            
        if self.layer[x, y] == self.key_pieces[56] and self.layer[x-1, y-1] == self.key_pieces[58]:
            self.layer[x-1, y] = self.key_pieces[63] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[56] and self.layer[x-1, y-1] == self.key_pieces[60]: 
            self.layer[x-1, y] = self.key_pieces[65] # Bottom-Left
            
        ## Outer Corners
        if self.layer[x, y] == self.key_pieces[56] and self.layer[x+1, y+1] == self.key_pieces[60]:
            self.layer[x+1, y] = self.key_pieces[61] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[56] and self.layer[x-1, y+1] == self.key_pieces[58]:
            self.layer[x-1, y] = self.key_pieces[55] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[62] and self.layer[x+1, y-1] == self.key_pieces[60]:
            self.layer[x+1, y] = self.key_pieces[63] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[62] and self.layer[x-1, y-1] == self.key_pieces[58]:
            self.layer[x-1, y] = self.key_pieces[57] # Bottom-Left
        return self.layer
    

    def steps(self, x, y):
        ## Steps
        if self.layer[x, y] == self.key_pieces[56] and self.layer[x+1, y+1] == self.key_pieces[56]:
            self.layer[x, y] = self.key_pieces[61]
            self.layer[x, y+1] = self.key_pieces[65]
        if self.layer[x, y] == self.key_pieces[56] and self.layer[x-1, y+1] == self.key_pieces[56]:
            self.layer[x-1, y] = self.key_pieces[55]
            self.layer[x-1, y+1] = self.key_pieces[67]
            
        if self.layer[x, y] == self.key_pieces[60] and self.layer[x+1, y+1] == self.key_pieces[60]:
            self.layer[x, y] = self.key_pieces[65]
            self.layer[x+1, y] = self.key_pieces[61]
        if self.layer[x, y] == self.key_pieces[60] and self.layer[x-1, y+1] == self.key_pieces[60]:
            self.layer[x, y] = self.key_pieces[63]
            self.layer[x-1, y] = self.key_pieces[64]

        if self.layer[x, y] == self.key_pieces[58] and self.layer[x+1, y+1] == self.key_pieces[58]:
            self.layer[x, y+1] = self.key_pieces[57]
            self.layer[x+1, y+1] = self.key_pieces[66]
        if self.layer[x, y] == self.key_pieces[58] and self.layer[x-1, y+1] == self.key_pieces[58]:
            self.layer[x-1, y] = self.key_pieces[55]
            self.layer[x, y] = self.key_pieces[67]

        if self.layer[x, y] == self.key_pieces[62] and self.layer[x+1, y+1] == self.key_pieces[62]:
            self.layer[x, y+1] = self.key_pieces[57]
            self.layer[x, y] = self.key_pieces[66]
        if self.layer[x, y] == self.key_pieces[62] and self.layer[x-1, y+1] == self.key_pieces[62]:
            self.layer[x, y+1] = self.key_pieces[63]
            self.layer[x, y] = self.key_pieces[64]
##        try:
##            self.layer[x, y] = self.key_pieces[x]
##        except:
##            pass
        return self.layer
