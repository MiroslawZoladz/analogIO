# import os

nonvolatile_obj_ctr = 0

class NonVolatile:   
    
    def __init__(self,default=None,test=False):
        global nonvolatile_obj_ctr
        
        file_name = f'vf_{nonvolatile_obj_ctr}.txt' if not test else f'vf_test_{nonvolatile_obj_ctr}.txt' 
        self._file_path = f"../nv/{file_name}"
        try:
            with open(self._file_path, "r") as file:
                self._data = eval(file.read())
        except OSError:
#             self._data = default
            self._data=None
            self.save()            
            
        nonvolatile_obj_ctr+=1
    
    def save(self):
        with open(self._file_path, "w") as file:
            file.write(str(self._data))
        
    def get(self):
        return self._data
    
    def set(self, data):
        self._data = data