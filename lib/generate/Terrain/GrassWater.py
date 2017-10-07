''' This is the Sand -> Water terraforming class.
Used in the map generation script

'''

class GrassWater:
    def edges(self, x, y):
        ## Up and Down
        if self.layer[x, y] == self.key_pieces[23] and self.layer[x, y-1] == self.key_pieces[5]:
            self.layer[x, y] = self.key_pieces[20] # Up
        if self.layer[x, y] == self.key_pieces[23] and self.layer[x, y+1] == self.key_pieces[5]:
            self.layer[x, y] = self.key_pieces[26] # Down
        ## Left and Right
        if self.layer[x, y] == self.key_pieces[23] and self.layer[x-1, y] == self.key_pieces[5]:
            self.layer[x, y] = self.key_pieces[22] # Left
        if self.layer[x, y] == self.key_pieces[23] and self.layer[x+1, y] == self.key_pieces[5]:
            self.layer[x, y] = self.key_pieces[24] # Right
        return self.layer

    def t(self, x, y):
        if self.layer[x, y] == self.key_pieces[24] and self.layer[x, y+1] == self.key_pieces[26]:
            self.layer[x, y+1] = self.key_pieces[24]
        ## Right Facing T
        if self.layer[x, y] == self.key_pieces[24] and self.layer[x, y+1] == self.key_pieces[26]:
            self.layer[x, y+1] = self.key_pieces[24]
        if self.layer[x, y] == self.key_pieces[24] and self.layer[x, y-1] == self.key_pieces[20]: 
            self.layer[x, y-1] = self.key_pieces[24]
        ## Left Facing T
        if self.layer[x, y] == self.key_pieces[22] and self.layer[x, y+1] == self.key_pieces[26]:
            self.layer[x, y+1] = self.key_pieces[22]
        if self.layer[x, y] == self.key_pieces[22] and self.layer[x, y-1] == self.key_pieces[20]: 
            self.layer[x, y-1] = self.key_pieces[22]
        ## Downward Facing T
        if self.layer[x, y] == self.key_pieces[26] and self.layer[x+1, y] == self.key_pieces[24]:
            self.layer[x+1, y] = self.key_pieces[23]                                   
        if self.layer[x, y] == self.key_pieces[26] and self.layer[x-1, y] == self.key_pieces[22]:  
            self.layer[x-1, y] = self.key_pieces[23]
        ## Upward Facing T
        if self.layer[x, y] == self.key_pieces[20] and self.layer[x+1, y] == self.key_pieces[24]:
            self.layer[x+1, y] = self.key_pieces[23]                                   
        if self.layer[x, y] == self.key_pieces[20] and self.layer[x-1, y] == self.key_pieces[22]:  
            self.layer[x-1, y] = self.key_pieces[23]
        ## Extra Ts
        if self.layer[x, y] == self.key_pieces[22] and self.layer[x+1, y] == self.key_pieces[20]:
            self.layer[x+1, y] = self.key_pieces[23]                                   
        if self.layer[x, y] == self.key_pieces[22] and self.layer[x-1, y] == self.key_pieces[22]:  
            self.layer[x-1, y] = self.key_pieces[23]
        return self.layer
    
    def corners(self, x, y):
        ## Inner Corners
        if self.layer[x, y] == self.key_pieces[26] and self.layer[x-1, y+1] == self.key_pieces[24]:
            self.layer[x-1, y] = self.key_pieces[31] # Top-Left
            
        if self.layer[x, y] == self.key_pieces[26] and self.layer[x+1, y+1] == self.key_pieces[24]:  
            self.layer[x-1, y] = self.key_pieces[31] # Top-Right
        if self.layer[x, y] == self.key_pieces[26] and self.layer[x+1, y+1] == self.key_pieces[22]:  
            self.layer[x+1, y] = self.key_pieces[31] # Top-Right
            
        if self.layer[x, y] == self.key_pieces[20] and self.layer[x+1, y-1] == self.key_pieces[22]:
            self.layer[x+1, y] = self.key_pieces[34] # Bottom-Right
        if self.layer[x, y] == self.key_pieces[26] and self.layer[x+1, y+1] == self.key_pieces[22]: 
            self.layer[x+1, y] = self.key_pieces[33] # Bottom-Right
            
        if self.layer[x, y] == self.key_pieces[20] and self.layer[x-1, y-1] == self.key_pieces[22]:
            self.layer[x-1, y] = self.key_pieces[27] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[20] and self.layer[x-1, y-1] == self.key_pieces[24]: 
            self.layer[x-1, y] = self.key_pieces[32] # Bottom-Left
            
        ## Outer Corners
        if self.layer[x, y] == self.key_pieces[20] and self.layer[x+1, y+1] == self.key_pieces[24]:
            self.layer[x+1, y] = self.key_pieces[25] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[20] and self.layer[x-1, y+1] == self.key_pieces[22]:
            self.layer[x-1, y] = self.key_pieces[19] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[26] and self.layer[x+1, y-1] == self.key_pieces[24]:
            self.layer[x+1, y] = self.key_pieces[27] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[26] and self.layer[x-1, y-1] == self.key_pieces[22]:
            self.layer[x-1, y] = self.key_pieces[21] # Bottom-Left
        return self.layer
    

    def steps(self, x, y):
        ## Steps
        if self.layer[x, y] == self.key_pieces[20] and self.layer[x+1, y+1] == self.key_pieces[20]:
            self.layer[x, y] = self.key_pieces[25]
            self.layer[x, y+1] = self.key_pieces[32]
        if self.layer[x, y] == self.key_pieces[20] and self.layer[x-1, y+1] == self.key_pieces[20]:
            self.layer[x-1, y] = self.key_pieces[19]
            self.layer[x-1, y+1] = self.key_pieces[34]
            
        if self.layer[x, y] == self.key_pieces[24] and self.layer[x+1, y+1] == self.key_pieces[24]:
            self.layer[x, y] = self.key_pieces[32]
            self.layer[x+1, y] = self.key_pieces[25]
        if self.layer[x, y] == self.key_pieces[24] and self.layer[x-1, y+1] == self.key_pieces[24]:
            self.layer[x, y] = self.key_pieces[27]
            self.layer[x-1, y] = self.key_pieces[31]

        if self.layer[x, y] == self.key_pieces[22] and self.layer[x+1, y+1] == self.key_pieces[22]:
            self.layer[x, y+1] = self.key_pieces[21]
            self.layer[x+1, y+1] = self.key_pieces[33]
        if self.layer[x, y] == self.key_pieces[22] and self.layer[x-1, y+1] == self.key_pieces[22]:
            self.layer[x-1, y] = self.key_pieces[19]
            self.layer[x, y] = self.key_pieces[34]

        if self.layer[x, y] == self.key_pieces[26] and self.layer[x+1, y+1] == self.key_pieces[26]:
            self.layer[x, y+1] = self.key_pieces[21]
            self.layer[x, y] = self.key_pieces[33]
        if self.layer[x, y] == self.key_pieces[26] and self.layer[x-1, y+1] == self.key_pieces[26]:
            self.layer[x, y+1] = self.key_pieces[27]
            self.layer[x, y] = self.key_pieces[31]
##        try:
##            self.layer[x, y] = self.key_pieces[x]
##        except:
##            pass
        return self.layer
