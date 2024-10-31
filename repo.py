class Repo:
    _instance = None
    _objects = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Repo, cls).__new__(cls)
        return cls._instance
    
    def create(self, **kwargs):
        pass
    
     
     

