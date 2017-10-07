''' This is the Sand -> Water terraforming class.
Used in the map generation script

'''

class SandWater:
    def edges(self, x, y):
        ## Up and Down
        if self.layer[x, y] == self.key_pieces[41] and self.layer[x, y-1] == self.key_pieces[23]:
            self.layer[x, y] = self.key_pieces[38] # Up
        if self.layer[x, y] == self.key_pieces[41] and self.layer[x, y+1] == self.key_pieces[23]:
            self.layer[x, y] = self.key_pieces[44] # Down
        ## Left and Right
        if self.layer[x, y] == self.key_pieces[41] and self.layer[x-1, y] == self.key_pieces[23]:
            self.layer[x, y] = self.key_pieces[40] # Left
        if self.layer[x, y] == self.key_pieces[41] and self.layer[x+1, y] == self.key_pieces[23]:
            self.layer[x, y] = self.key_pieces[42] # Right
        return self.layer

    def t(self, x, y):
        if self.layer[x, y] == self.key_pieces[42] and self.layer[x, y+1] == self.key_pieces[44]:
            self.layer[x, y+1] = self.key_pieces[42]
        ## Right Facing T
        if self.layer[x, y] == self.key_pieces[42] and self.layer[x, y+1] == self.key_pieces[44]:
            self.layer[x, y+1] = self.key_pieces[42]
        if self.layer[x, y] == self.key_pieces[42] and self.layer[x, y-1] == self.key_pieces[38]: 
            self.layer[x, y-1] = self.key_pieces[42]
        ## Left Facing T
        if self.layer[x, y] == self.key_pieces[40] and self.layer[x, y+1] == self.key_pieces[44]:
            self.layer[x, y+1] = self.key_pieces[40]
        if self.layer[x, y] == self.key_pieces[40] and self.layer[x, y-1] == self.key_pieces[38]: 
            self.layer[x, y-1] = self.key_pieces[40]
        ## Downward Facing T
        if self.layer[x, y] == self.key_pieces[44] and self.layer[x+1, y] == self.key_pieces[42]:
            self.layer[x+1, y] = self.key_pieces[41]                                   
        if self.layer[x, y] == self.key_pieces[44] and self.layer[x-1, y] == self.key_pieces[40]:  
            self.layer[x-1, y] = self.key_pieces[41]
        ## Upward Facing T
        if self.layer[x, y] == self.key_pieces[38] and self.layer[x+1, y] == self.key_pieces[42]:
            self.layer[x+1, y] = self.key_pieces[41]                                   
        if self.layer[x, y] == self.key_pieces[38] and self.layer[x-1, y] == self.key_pieces[40]:  
            self.layer[x-1, y] = self.key_pieces[41]
        ## Extra Ts
        if self.layer[x, y] == self.key_pieces[40] and self.layer[x+1, y] == self.key_pieces[38]:
            self.layer[x+1, y] = self.key_pieces[41]                                   
        if self.layer[x, y] == self.key_pieces[40] and self.layer[x-1, y] == self.key_pieces[40]:  
            self.layer[x-1, y] = self.key_pieces[41]
        return self.layer
    
    def corners(self, x, y):
        ## Inner Corners
        if self.layer[x, y] == self.key_pieces[44] and self.layer[x-1, y+1] == self.key_pieces[42]:
            self.layer[x-1, y] = self.key_pieces[49] # Top-Left
            
        if self.layer[x, y] == self.key_pieces[44] and self.layer[x+1, y+1] == self.key_pieces[42]:  
            self.layer[x-1, y] = self.key_pieces[49] # Top-Right
        if self.layer[x, y] == self.key_pieces[44] and self.layer[x+1, y+1] == self.key_pieces[40]:  
            self.layer[x+1, y] = self.key_pieces[49] # Top-Right
            
        if self.layer[x, y] == self.key_pieces[38] and self.layer[x+1, y-1] == self.key_pieces[40]:
            self.layer[x+1, y] = self.key_pieces[52] # Bottom-Right
        if self.layer[x, y] == self.key_pieces[44] and self.layer[x+1, y+1] == self.key_pieces[40]: 
            self.layer[x+1, y] = self.key_pieces[51] # Bottom-Right
            
        if self.layer[x, y] == self.key_pieces[38] and self.layer[x-1, y-1] == self.key_pieces[40]:
            self.layer[x-1, y] = self.key_pieces[45] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[38] and self.layer[x-1, y-1] == self.key_pieces[42]: 
            self.layer[x-1, y] = self.key_pieces[50] # Bottom-Left
            
        ## Outer Corners
        if self.layer[x, y] == self.key_pieces[38] and self.layer[x+1, y+1] == self.key_pieces[42]:
            self.layer[x+1, y] = self.key_pieces[43] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[38] and self.layer[x-1, y+1] == self.key_pieces[40]:
            self.layer[x-1, y] = self.key_pieces[37] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[44] and self.layer[x+1, y-1] == self.key_pieces[42]:
            self.layer[x+1, y] = self.key_pieces[45] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[44] and self.layer[x-1, y-1] == self.key_pieces[40]:
            self.layer[x-1, y] = self.key_pieces[39] # Bottom-Left
        return self.layer
    

    def steps(self, x, y):
        ## Steps
        if self.layer[x, y] == self.key_pieces[38] and self.layer[x+1, y+1] == self.key_pieces[38]:
            self.layer[x, y] = self.key_pieces[43]
            self.layer[x, y+1] = self.key_pieces[50]
        if self.layer[x, y] == self.key_pieces[38] and self.layer[x-1, y+1] == self.key_pieces[38]:
            self.layer[x-1, y] = self.key_pieces[37]
            self.layer[x-1, y+1] = self.key_pieces[52]
            
        if self.layer[x, y] == self.key_pieces[42] and self.layer[x+1, y+1] == self.key_pieces[42]:
            self.layer[x, y] = self.key_pieces[50]
            self.layer[x+1, y] = self.key_pieces[43]
        if self.layer[x, y] == self.key_pieces[42] and self.layer[x-1, y+1] == self.key_pieces[42]:
            self.layer[x, y] = self.key_pieces[45]
            self.layer[x-1, y] = self.key_pieces[49]

        if self.layer[x, y] == self.key_pieces[40] and self.layer[x+1, y+1] == self.key_pieces[40]:
            self.layer[x, y+1] = self.key_pieces[39]
            self.layer[x+1, y+1] = self.key_pieces[51]
        if self.layer[x, y] == self.key_pieces[40] and self.layer[x-1, y+1] == self.key_pieces[40]:
            self.layer[x-1, y] = self.key_pieces[37]
            self.layer[x, y] = self.key_pieces[52]

        if self.layer[x, y] == self.key_pieces[44] and self.layer[x+1, y+1] == self.key_pieces[44]:
            self.layer[x, y+1] = self.key_pieces[39]
            self.layer[x, y] = self.key_pieces[51]
        if self.layer[x, y] == self.key_pieces[44] and self.layer[x-1, y+1] == self.key_pieces[44]:
            self.layer[x, y+1] = self.key_pieces[45]
            self.layer[x, y] = self.key_pieces[49]
##        try:
##            self.layer[x, y] = self.key_pieces[x]
##        except:
##            pass
        return self.layer
