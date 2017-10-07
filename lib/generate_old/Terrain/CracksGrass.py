''' This is the Cracks -> Grass terraforming class.
Used in the map generation script

'''

class CracksGrass:
    def edges(self, x, y):
        ## Up and Down
        if self.layer[x, y] == self.key_pieces[32] and self.layer[x, y-1] == self.key_pieces[14]:
            self.layer[x, y] = self.key_pieces[65] # Up
        if self.layer[x, y] == self.key_pieces[32] and self.layer[x, y+1] == self.key_pieces[14]:
            self.layer[x, y] = self.key_pieces[71] # Down
        ## Left and Right
        if self.layer[x, y] == self.key_pieces[32] and self.layer[x-1, y] == self.key_pieces[14]:
            self.layer[x, y] = self.key_pieces[67] # Left
        if self.layer[x, y] == self.key_pieces[32] and self.layer[x+1, y] == self.key_pieces[14]:
            self.layer[x, y] = self.key_pieces[69] # Right
        return self.layer

    def t(self, x, y):            
        ## Right Facing T
        if self.layer[x, y] == self.key_pieces[69] and self.layer[x, y+1] == self.key_pieces[71]: ##  │ ##
            self.layer[x, y+1] = self.key_pieces[69]                                              ##  ─ ##
        if self.layer[x, y] == self.key_pieces[69] and self.layer[x, y-1] == self.key_pieces[65]: ##  _ ## 
            self.layer[x, y-1] = self.key_pieces[69]                                              ##  │ ##
        ## Left Facing T
        if self.layer[x, y] == self.key_pieces[67] and self.layer[x, y+1] == self.key_pieces[71]: ##  │ ##
            self.layer[x, y+1] = self.key_pieces[67]                                              ##  ─ ##
        if self.layer[x, y] == self.key_pieces[67] and self.layer[x, y-1] == self.key_pieces[65]: ##  _ ## 
            self.layer[x, y-1] = self.key_pieces[67]                                              ##  │ ##
        ## Downward Facing T
        if self.layer[x, y] == self.key_pieces[71] and self.layer[x+1, y] == self.key_pieces[69]: ## -| ##
            self.layer[x+1, y] = self.key_pieces[32]                                   
        if self.layer[x, y] == self.key_pieces[71] and self.layer[x-1, y] == self.key_pieces[67]: ## |- ##  
            self.layer[x-1, y] = self.key_pieces[32]
        ## Upward Facing T
        if self.layer[x, y] == self.key_pieces[65] and self.layer[x+1, y] == self.key_pieces[69]: ## -| ##
            self.layer[x+1, y] = self.key_pieces[32]                                   
        if self.layer[x, y] == self.key_pieces[65] and self.layer[x-1, y] == self.key_pieces[67]: ## |- ##  
            self.layer[x-1, y] = self.key_pieces[32]
        ## Extra Ts
        if self.layer[x, y] == self.key_pieces[67] and self.layer[x+1, y] == self.key_pieces[65]: ## -| ##
            self.layer[x+1, y] = self.key_pieces[32]                                   
        if self.layer[x, y] == self.key_pieces[67] and self.layer[x-1, y] == self.key_pieces[67]: ## |- ##  
            self.layer[x-1, y] = self.key_pieces[32]
        return self.layer

    def corners(self, x, y):
        ## Inner Corners
        if self.layer[x, y] == self.key_pieces[71] and self.layer[x-1, y+1] == self.key_pieces[69]:
            self.layer[x-1, y] = self.key_pieces[76] # Top-Left
            
        if self.layer[x, y] == self.key_pieces[71] and self.layer[x+1, y+1] == self.key_pieces[69]:  
            self.layer[x-1, y] = self.key_pieces[77] # Top-Right
        if self.layer[x, y] == self.key_pieces[71] and self.layer[x+1, y+1] == self.key_pieces[67]:  
            self.layer[x+1, y] = self.key_pieces[77] # Top-Right
            
        if self.layer[x, y] == self.key_pieces[65] and self.layer[x+1, y-1] == self.key_pieces[67]:
            self.layer[x+1, y] = self.key_pieces[79] # Bottom-Right
        if self.layer[x, y] == self.key_pieces[71] and self.layer[x+1, y+1] == self.key_pieces[67]: 
            self.layer[x+1, y] = self.key_pieces[77] # Bottom-Right
            
        if self.layer[x, y] == self.key_pieces[65] and self.layer[x-1, y-1] == self.key_pieces[67]:
            self.layer[x-1, y] = self.key_pieces[78] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[65] and self.layer[x-1, y-1] == self.key_pieces[69]: 
            self.layer[x-1, y] = self.key_pieces[78] # Bottom-Left
            
        ## Outer Corners
        if self.layer[x, y] == self.key_pieces[65] and self.layer[x+1, y+1] == self.key_pieces[69]:
            self.layer[x+1, y] = self.key_pieces[66] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[65] and self.layer[x-1, y+1] == self.key_pieces[67]:
            self.layer[x-1, y] = self.key_pieces[64] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[71] and self.layer[x+1, y-1] == self.key_pieces[69]:
            self.layer[x+1, y] = self.key_pieces[72] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[71] and self.layer[x-1, y-1] == self.key_pieces[67]:
            self.layer[x-1, y] = self.key_pieces[70] # Bottom-Left
        return self.layer

    def steps(self, x, y):
        ## Steps
        if self.layer[x, y] == self.key_pieces[65] and self.layer[x+1, y+1] == self.key_pieces[65]:
            self.layer[x, y] = self.key_pieces[66]
            self.layer[x, y+1] = self.key_pieces[78]
        if self.layer[x, y] == self.key_pieces[65] and self.layer[x-1, y+1] == self.key_pieces[65]:
            self.layer[x-1, y] = self.key_pieces[64]
            self.layer[x-1, y+1] = self.key_pieces[79]
            
        if self.layer[x, y] == self.key_pieces[69] and self.layer[x+1, y+1] == self.key_pieces[69]:
            self.layer[x+1, y] = self.key_pieces[66]
            self.layer[x, y] = self.key_pieces[78]
        if self.layer[x, y] == self.key_pieces[69] and self.layer[x-1, y+1] == self.key_pieces[69]:
            self.layer[x, y] = self.key_pieces[72]
            self.layer[x-1, y] = self.key_pieces[76]

        if self.layer[x, y] == self.key_pieces[67] and self.layer[x+1, y+1] == self.key_pieces[67]:
            self.layer[x, y+1] = self.key_pieces[70]
            self.layer[x+1, y+1] = self.key_pieces[77]
        if self.layer[x, y] == self.key_pieces[67] and self.layer[x-1, y+1] == self.key_pieces[67]:
            self.layer[x-1, y] = self.key_pieces[64]
            self.layer[x, y] = self.key_pieces[79]

        if self.layer[x, y] == self.key_pieces[71] and self.layer[x+1, y+1] == self.key_pieces[71]:
            self.layer[x, y+1] = self.key_pieces[70]
            self.layer[x, y] = self.key_pieces[77]
        if self.layer[x, y] == self.key_pieces[71] and self.layer[x-1, y+1] == self.key_pieces[71]:
            self.layer[x, y+1] = self.key_pieces[72]
            self.layer[x, y] = self.key_pieces[76]
        return self.layer
        
