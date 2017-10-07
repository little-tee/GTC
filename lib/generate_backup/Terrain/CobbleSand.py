''' This is the Cobble -> Grass terraforming class.
Used in the map generation script

'''

class CobbleSand:
    def edges(self, x, y):
        ## Up and Down
        if self.layer[x, y] == self.key_pieces[5] and self.layer[x, y-1] == self.key_pieces[23]:
            self.layer[x, y] = self.key_pieces[2] # Up
        if self.layer[x, y] == self.key_pieces[5] and self.layer[x, y+1] == self.key_pieces[23]:
            self.layer[x, y] = self.key_pieces[8] # Down
        ## Left and Right
        if self.layer[x, y] == self.key_pieces[5] and self.layer[x-1, y] == self.key_pieces[23]:
            self.layer[x, y] = self.key_pieces[4] # Left
        if self.layer[x, y] == self.key_pieces[5] and self.layer[x+1, y] == self.key_pieces[23]:
            self.layer[x, y] = self.key_pieces[6] # Right
        return self.layer

    def t(self, x, y):
        ## Right Facing T
        if self.layer[x, y] == self.key_pieces[6] and self.layer[x, y+1] == self.key_pieces[8]: ##  │ ##
            self.layer[x, y+1] = self.key_pieces[6]                                   ##  ─ ##
        if self.layer[x, y] == self.key_pieces[6] and self.layer[x, y-1] == self.key_pieces[2]: ##  _ ## 
            self.layer[x, y-1] = self.key_pieces[6]                                   ##  │ ##
        ## Left Facing T
        if self.layer[x, y] == self.key_pieces[4] and self.layer[x, y+1] == self.key_pieces[8]: ##  │ ##
            self.layer[x, y+1] = self.key_pieces[4]                                   ##  ─ ##
        if self.layer[x, y] == self.key_pieces[4] and self.layer[x, y-1] == self.key_pieces[2]: ##  _ ## 
            self.layer[x, y-1] = self.key_pieces[4]                                   ##  │ ##
        ## Downward Facing T
        if self.layer[x, y] == self.key_pieces[8] and self.layer[x+1, y] == self.key_pieces[6]: ## -| ##
            self.layer[x+1, y] = self.key_pieces[23]                                   
        if self.layer[x, y] == self.key_pieces[8] and self.layer[x-1, y] == self.key_pieces[4]: ## |- ##  
            self.layer[x-1, y] = self.key_pieces[23]
        ## Upward Facing T
        if self.layer[x, y] == self.key_pieces[2] and self.layer[x+1, y] == self.key_pieces[6]: ## -| ##
            self.layer[x+1, y] = self.key_pieces[23]                                   
        if self.layer[x, y] == self.key_pieces[2] and self.layer[x-1, y] == self.key_pieces[4]: ## |- ##  
            self.layer[x-1, y] = self.key_pieces[23]
        ## Extra Ts
        if self.layer[x, y] == self.key_pieces[4] and self.layer[x+1, y] == self.key_pieces[2]: ## -| ##
            self.layer[x+1, y] = self.key_pieces[23]                                   
        if self.layer[x, y] == self.key_pieces[2] and self.layer[x-1, y] == self.key_pieces[4]: ## |- ##  
            self.layer[x-1, y] = self.key_pieces[23]
        return self.layer

    def corners(self, x, y):
        ## Inner Corners
        if self.layer[x, y] == self.key_pieces[8] and self.layer[x-1, y+1] == self.key_pieces[6]:
            self.layer[x-1, y] = self.key_pieces[19] # Top-Left
            
        if self.layer[x, y] == self.key_pieces[8] and self.layer[x+1, y+1] == self.key_pieces[6]:  
            self.layer[x-1, y] = self.key_pieces[20] # Top-Right
        if self.layer[x, y] == self.key_pieces[8] and self.layer[x+1, y+1] == self.key_pieces[4]:  
            self.layer[x+1, y] = self.key_pieces[20] # Top-Right
            
        if self.layer[x, y] == self.key_pieces[2] and self.layer[x+1, y-1] == self.key_pieces[4]:
            self.layer[x+1, y] = self.key_pieces[22] # Bottom-Right
        if self.layer[x, y] == self.key_pieces[8] and self.layer[x+1, y+1] == self.key_pieces[4]: 
            self.layer[x+1, y] = self.key_pieces[20] # Bottom-Right
            
        if self.layer[x, y] == self.key_pieces[2] and self.layer[x-1, y-1] == self.key_pieces[4]:
            self.layer[x-1, y] = self.key_pieces[21] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[2] and self.layer[x-1, y-1] == self.key_pieces[6]: 
            self.layer[x-1, y] = self.key_pieces[21] # Bottom-Left
            
        ## Outer Corners
        if self.layer[x, y] == self.key_pieces[2] and self.layer[x+1, y+1] == self.key_pieces[6]:
            self.layer[x+1, y] = self.key_pieces[3] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[2] and self.layer[x-1, y+1] == self.key_pieces[4]:
            self.layer[x-1, y] = self.key_pieces[1] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[8] and self.layer[x+1, y-1] == self.key_pieces[6]:
            self.layer[x+1, y] = self.key_pieces[9] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[8] and self.layer[x-1, y-1] == self.key_pieces[4]:
            self.layer[x-1, y] = self.key_pieces[7] # Bottom-Left
        return self.layer

    def steps(self, x, y):
        ## Steps
        if self.layer[x, y] == self.key_pieces[2] and self.layer[x+1, y+1] == self.key_pieces[2]:
            self.layer[x, y] = self.key_pieces[3]
            self.layer[x, y+1] = self.key_pieces[21]
        if self.layer[x, y] == self.key_pieces[2] and self.layer[x-1, y+1] == self.key_pieces[2]:
            self.layer[x-1, y] = self.key_pieces[1]
            self.layer[x-1, y+1] = self.key_pieces[22]
            
        if self.layer[x, y] == self.key_pieces[6] and self.layer[x+1, y+1] == self.key_pieces[6]:
            self.layer[x+1, y] = self.key_pieces[3]
            self.layer[x, y] = self.key_pieces[21]
        if self.layer[x, y] == self.key_pieces[6] and self.layer[x-1, y+1] == self.key_pieces[6]:
            self.layer[x, y] = self.key_pieces[9]
            self.layer[x-1, y] = self.key_pieces[19]

        if self.layer[x, y] == self.key_pieces[4] and self.layer[x+1, y+1] == self.key_pieces[4]:
            self.layer[x, y+1] = self.key_pieces[7]
            self.layer[x+1, y+1] = self.key_pieces[20]
        if self.layer[x, y] == self.key_pieces[4] and self.layer[x-1, y+1] == self.key_pieces[4]:
            self.layer[x-1, y] = self.key_pieces[1]
            self.layer[x, y] = self.key_pieces[22]

        if self.layer[x, y] == self.key_pieces[8] and self.layer[x+1, y+1] == self.key_pieces[8]:
            self.layer[x, y+1] = self.key_pieces[7]
            self.layer[x, y] = self.key_pieces[20]
        if self.layer[x, y] == self.key_pieces[8] and self.layer[x-1, y+1] == self.key_pieces[8]:
            self.layer[x, y+1] = self.key_pieces[9]
            self.layer[x, y] = self.key_pieces[19]
        return self.layer
        
