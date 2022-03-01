import pyotp

class Authenticator:
    def __init__(self, secret = pyotp.random_base32()):
        self.secret = secret
        self.interval= None
        self.totp = None
        



# sets new seret and specifi time interval default is 30 seconds
    def getpin(self):
        try:
            return self.totp.now()
            
        except:
            return "Not available"
   
    def setSecret(self, secret =''):
        if secret =='':
            self.secret = pyotp.random_base32()     
        else:
            self.secret = secret  
        return self.secret

    def setInterval(self,interval=30):
        self.interval=interval
        return True

    
    def setTotp(self):
        self.totp = pyotp.TOTP(self.secret,interval=self.interval)
        
        return self.totp.now()

    
    def getSecret(self):
        return self.secret

    def print(self):
        print(f"{self.totp.interval}")