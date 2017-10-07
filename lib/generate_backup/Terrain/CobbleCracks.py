''' This is the Cobble -> Grass terraforming class.
Used in the map generation script

'''

class CobbleCracks:
    def edges(self, x, y):
        ## Up and Down
        if self.layer[x, y] == self.key_pieces[14] and self.layer[x, y-1] == self.key_pieces[5]:
            self.layer[x, y] = self.key_pieces[83] # Up
        if self.layer[x, y] == self.key_pieces[14] and self.layer[x, y+1] == self.key_pieces[5]:
            self.layer[x, y] = self.key_pieces[89] # Down
        ## Left and Right
        if self.layer[x, y] == self.key_pieces[14] and self.layer[x-1, y] == self.key_pieces[5]:
            self.layer[x, y] = self.key_pieces[85] # Left
        if self.layer[x, y] == self.key_pieces[14] and self.layer[x+1, y] == self.key_pieces[5]:
            self.layer[x, y] = self.key_pieces[87] # Right
        return self.layer

    def t(self, x, y):            
        ## Right Facing T
        if self.layer[x, y] == self.key_pieces[87] and self.layer[x, y+1] == self.key_pieces[89]:
            self.layer[x, y+1] = self.key_pieces[87]
        if self.layer[x, y] == self.key_pieces[87] and self.layer[x, y-1] == self.key_pieces[83]: 
            self.layer[x, y-1] = self.key_pieces[84]
            self.layer[x-1, y-1] = self.key_pieces[98]
        ## Left Facing T
        if self.layer[x, y] == self.key_pieces[85] and self.layer[x, y+1] == self.key_pieces[89]:
            self.layer[x, y+1] = self.key_pieces[85]                                   ##  ─ ##
        if self.layer[x, y] == self.key_pieces[85] and self.layer[x, y-1] == self.key_pieces[83]: 
            self.layer[x, y-1] = self.key_pieces[85]
        ## Downward Facing T
        if self.layer[x, y] == self.key_pieces[89] and self.layer[x+1, y] == self.key_pieces[87]:
            self.layer[x+1, y] = self.key_pieces[5]                                   
        if self.layer[x, y] == self.key_pieces[89] and self.layer[x-1, y] == self.key_pieces[85]:  
            self.layer[x-1, y] = self.key_pieces[5]
        ## Upward Facing T
        if self.layer[x, y] == self.key_pieces[83] and self.layer[x+1, y] == self.key_pieces[87]:
            self.layer[x+1, y] = self.key_pieces[5]                                   
        if self.layer[x, y] == self.key_pieces[83] and self.layer[x-1, y] == self.key_pieces[85]: 
            self.layer[x-1, y] = self.key_pieces[5]
        ## Extra Ts
        if self.layer[x, y] == self.key_pieces[85] and self.layer[x+1, y] == self.key_pieces[83]:
            self.layer[x+1, y] = self.key_pieces[5]                                   
        if self.layer[x, y] == self.key_pieces[83] and self.layer[x-1, y] == self.key_pieces[85]:  
            self.layer[x-1, y] = self.key_pieces[5]
        return self.layer

    def corners(self, x, y):
        ## Inner Corners
        if self.layer[x, y] == self.key_pieces[89] and self.layer[x-1, y+1] == self.key_pieces[87]:
            self.layer[x-1, y] = self.key_pieces[96] # Top-Left
            
        if self.layer[x, y] == self.key_pieces[89] and self.layer[x+1, y+1] == self.key_pieces[87]:  
            self.layer[x-1, y] = self.key_pieces[97] # Top-Right
        if self.layer[x, y] == self.key_pieces[89] and self.layer[x+1, y+1] == self.key_pieces[85]:  
            self.layer[x+1, y] = self.key_pieces[97] # Top-Right
            
        if self.layer[x, y] == self.key_pieces[83] and self.layer[x+1, y-1] == self.key_pieces[85]:
            self.layer[x+1, y] = self.key_pieces[99] # Bottom-Right
        if self.layer[x, y] == self.key_pieces[89] and self.layer[x+1, y+1] == self.key_pieces[85]: 
            self.layer[x+1, y] = self.key_pieces[97] # Bottom-Right
            
        if self.layer[x, y] == self.key_pieces[83] and self.layer[x-1, y-1] == self.key_pieces[85]:
            self.layer[x-1, y] = self.key_pieces[98] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[83] and self.layer[x-1, y-1] == self.key_pieces[87]: 
            self.layer[x-1, y] = self.key_pieces[98] # Bottom-Left
            
        ## Outer Corners
        if self.layer[x, y] == self.key_pieces[83] and self.layer[x+1, y+1] == self.key_pieces[87]:
            self.layer[x+1, y] = self.key_pieces[84] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[83] and self.layer[x-1, y+1] == self.key_pieces[85]:
            self.layer[x-1, y] = self.key_pieces[82] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[89] and self.layer[x+1, y-1] == self.key_pieces[87]:
            self.layer[x+1, y] = self.key_pieces[90] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[89] and self.layer[x-1, y-1] == self.key_pieces[85]:
            self.layer[x-1, y] = self.key_pieces[88] # Bottom-Left
        return self.layer

    def steps(self, x, y):
        ## Steps
        if self.layer[x, y] == self.key_pieces[83] and self.layer[x+1, y+1] == self.key_pieces[83]:
            self.layer[x, y] = self.key_pieces[84]
            self.layer[x, y+1] = self.key_pieces[98]
        if self.layer[x, y] == self.key_pieces[83] and self.layer[x-1, y+1] == self.key_pieces[83]:
            self.layer[x-1, y] = self.key_pieces[82]
            self.layer[x-1, y+1] = self.key_pieces[99]
            
        if self.layer[x, y] == self.key_pieces[87] and self.layer[x+1, y+1] == self.key_pieces[87]:
            self.layer[x+1, y] = self.key_pieces[83]
            self.layer[x, y] = self.key_pieces[98]
        if self.layer[x, y] == self.key_pieces[87] and self.layer[x-1, y+1] == self.key_pieces[87]:
            self.layer[x, y] = self.key_pieces[90]
            self.layer[x-1, y] = self.key_pieces[96]

        if self.layer[x, y] == self.key_pieces[85] and self.layer[x+1, y+1] == self.key_pieces[85]:
            self.layer[x, y+1] = self.key_pieces[88]
            self.layer[x+1, y+1] = self.key_pieces[97]
        if self.layer[x, y] == self.key_pieces[85] and self.layer[x-1, y+1] == self.key_pieces[85]:
            self.layer[x-1, y] = self.key_pieces[82]
            self.layer[x, y] = self.key_pieces[99]

        if self.layer[x, y] == self.key_pieces[89] and self.layer[x+1, y+1] == self.key_pieces[89]:
            self.layer[x, y+1] = self.key_pieces[88]
            self.layer[x, y] = self.key_pieces[97]
        if self.layer[x, y] == self.key_pieces[89] and self.layer[x-1, y+1] == self.key_pieces[89]:
            self.layer[x, y+1] = self.key_pieces[90]
            self.layer[x, y] = self.key_pieces[96]
        return self.layer
        
