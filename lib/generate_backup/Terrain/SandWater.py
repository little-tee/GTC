''' This is the Sand -> Water terraforming class.
Used in the map generation script

'''

class SandWater:
    def edges(self, x, y):
        ## Up and Down
##        if self.layer[x, y] == self.key_pieces[50] and self.layer[x, y-1] == self.key_pieces[23]:
##            self.layer[x, y] = self.key_pieces[107] # Up
##        if self.layer[x, y] == self.key_pieces[50] and self.layer[x, y+1] == self.key_pieces[23]:
##            self.layer[x, y] = self.key_pieces[101] # Down
        ## Left and Right
        if self.layer[x, y] == self.key_pieces[50] and self.layer[x-1, y] == self.key_pieces[23]:
            self.layer[x, y] = self.key_pieces[105] # Left
        if self.layer[x, y] == self.key_pieces[50] and self.layer[x+1, y] == self.key_pieces[23]:
            self.layer[x, y] = self.key_pieces[103] # Right
        return self.layer

    def t(self, x, y):
        print(self.layer[x, y].gid)
        if self.layer[x, y] == self.key_pieces[105] and self.layer[x, y+1] == self.key_pieces[107]: ##  │ ##
            self.layer[x, y+1] = self.key_pieces[106]
            print("Yup!")
##        ## Right Facing T
##        if self.layer[x, y] == self.key_pieces[105] and self.layer[x, y+1] == self.key_pieces[107]: ##  │ ##
##            self.layer[x, y+1] = self.key_pieces[105]                                              ##  ─ ##
##        if self.layer[x, y] == self.key_pieces[105] and self.layer[x, y-1] == self.key_pieces[101]: ##  _ ## 
##            self.layer[x, y-1] = self.key_pieces[105]                                              ##  │ ##
##        ## Left Facing T
##        if self.layer[x, y] == self.key_pieces[103] and self.layer[x, y+1] == self.key_pieces[107]: ##  │ ##
##            self.layer[x, y+1] = self.key_pieces[103]                                              ##  ─ ##
##        if self.layer[x, y] == self.key_pieces[103] and self.layer[x, y-1] == self.key_pieces[101]: ##  _ ## 
##            self.layer[x, y-1] = self.key_pieces[103]                                              ##  │ ##
##        ## Downward Facing T
##        if self.layer[x, y] == self.key_pieces[107] and self.layer[x+1, y] == self.key_pieces[105]: ## -| ##
##            self.layer[x+1, y] = self.key_pieces[23]                                   
##        if self.layer[x, y] == self.key_pieces[107] and self.layer[x-1, y] == self.key_pieces[103]: ## |- ##  
##            self.layer[x-1, y] = self.key_pieces[23]
##        ## Upward Facing T
##        if self.layer[x, y] == self.key_pieces[101] and self.layer[x+1, y] == self.key_pieces[105]: ## -| ##
##            self.layer[x+1, y] = self.key_pieces[23]                                   
##        if self.layer[x, y] == self.key_pieces[101] and self.layer[x-1, y] == self.key_pieces[103]: ## |- ##  
##            self.layer[x-1, y] = self.key_pieces[23]
##        ## Extra Ts
##        if self.layer[x, y] == self.key_pieces[103] and self.layer[x+1, y] == self.key_pieces[101]: ## -| ##
##            self.layer[x+1, y] = self.key_pieces[23]                                   
##        if self.layer[x, y] == self.key_pieces[103] and self.layer[x-1, y] == self.key_pieces[103]: ## |- ##  
##            self.layer[x-1, y] = self.key_pieces[23]
        return self.layer
    
    def corners(self, x, y):
        ## Inner Corners
        if self.layer[x, y] == self.key_pieces[107] and self.layer[x-1, y+1] == self.key_pieces[105]:
            self.layer[x-1, y] = self.key_pieces[112] # Top-Left
            
        if self.layer[x, y] == self.key_pieces[107] and self.layer[x+1, y+1] == self.key_pieces[105]:  
            self.layer[x-1, y] = self.key_pieces[113] # Top-Right
        if self.layer[x, y] == self.key_pieces[107] and self.layer[x+1, y+1] == self.key_pieces[103]:  
            self.layer[x+1, y] = self.key_pieces[113] # Top-Right
            
        if self.layer[x, y] == self.key_pieces[101] and self.layer[x+1, y-1] == self.key_pieces[103]:
            self.layer[x+1, y] = self.key_pieces[115] # Bottom-Right
        if self.layer[x, y] == self.key_pieces[107] and self.layer[x+1, y+1] == self.key_pieces[103]: 
            self.layer[x+1, y] = self.key_pieces[113] # Bottom-Right
            
        if self.layer[x, y] == self.key_pieces[101] and self.layer[x-1, y-1] == self.key_pieces[103]:
            self.layer[x-1, y] = self.key_pieces[114] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[101] and self.layer[x-1, y-1] == self.key_pieces[105]: 
            self.layer[x-1, y] = self.key_pieces[114] # Bottom-Left
            
        ## Outer Corners
        if self.layer[x, y] == self.key_pieces[101] and self.layer[x+1, y+1] == self.key_pieces[105]:
            self.layer[x+1, y] = self.key_pieces[102] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[101] and self.layer[x-1, y+1] == self.key_pieces[103]:
            self.layer[x-1, y] = self.key_pieces[100] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[107] and self.layer[x+1, y-1] == self.key_pieces[105]:
            self.layer[x+1, y] = self.key_pieces[108] # Bottom-Left
        if self.layer[x, y] == self.key_pieces[107] and self.layer[x-1, y-1] == self.key_pieces[103]:
            self.layer[x-1, y] = self.key_pieces[106] # Bottom-Left
        return self.layer

    def steps(self, x, y):
        ## Steps
        if self.layer[x, y] == self.key_pieces[101] and self.layer[x+1, y+1] == self.key_pieces[101]:
            self.layer[x, y] = self.key_pieces[102]
            self.layer[x, y+1] = self.key_pieces[114]
        if self.layer[x, y] == self.key_pieces[101] and self.layer[x-1, y+1] == self.key_pieces[101]:
            self.layer[x-1, y] = self.key_pieces[100]
            self.layer[x-1, y+1] = self.key_pieces[115]
            
        if self.layer[x, y] == self.key_pieces[105] and self.layer[x+1, y+1] == self.key_pieces[105]:
            self.layer[x+1, y] = self.key_pieces[102]
            self.layer[x, y] = self.key_pieces[114]
        if self.layer[x, y] == self.key_pieces[105] and self.layer[x-1, y+1] == self.key_pieces[105]:
            self.layer[x, y] = self.key_pieces[108]
            self.layer[x-1, y] = self.key_pieces[112]

        if self.layer[x, y] == self.key_pieces[103] and self.layer[x+1, y+1] == self.key_pieces[103]:
            self.layer[x, y+1] = self.key_pieces[106]
            self.layer[x+1, y+1] = self.key_pieces[113]
        if self.layer[x, y] == self.key_pieces[103] and self.layer[x-1, y+1] == self.key_pieces[103]:
            self.layer[x-1, y] = self.key_pieces[100]
            self.layer[x, y] = self.key_pieces[115]

        if self.layer[x, y] == self.key_pieces[107] and self.layer[x+1, y+1] == self.key_pieces[107]:
            self.layer[x, y+1] = self.key_pieces[106]
            self.layer[x, y] = self.key_pieces[113]
        if self.layer[x, y] == self.key_pieces[107] and self.layer[x-1, y+1] == self.key_pieces[107]:
            self.layer[x, y+1] = self.key_pieces[108]
            self.layer[x, y] = self.key_pieces[112]
        return self.layer

    def new_func(self, x, y):
        if self.layer[x, y] == self.key_pieces[50] and self.layer[x, y-1] == self.key_pieces[23]:
            self.layer[x, y] = self.key_pieces[107] # Up
        if self.layer[x, y] == self.key_pieces[50] and self.layer[x, y+1] == self.key_pieces[23]:
            self.layer[x, y] = self.key_pieces[101] # Down
        return self.layer

