
#Types of error in the creation of figures

class ExceptionFigure:

    '''
        TYPES OF ERROR:
        1. Warning: It can be run with this but need to be fixed
        2. Basic Error: Doesnt run but it can be fixed
        3. Fatal Error: Not idea what is happening ??? 
    '''

    def __init__(self, error, message):
        self.error = error
        self.message = message 

    
 