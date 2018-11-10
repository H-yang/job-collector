class Result:
    def __init__(self):
        self.companyName=''
        self.jobTitle=''
        self.isHeadHunter=False
        self.location=''
        self.postedOn=''
        self.isOnNOH1BList=False
        self.visaKeywords=[]
        self.applied=''
        self.enterDate=''
        self.url=''
        self.isAd=False
        self.experience=''
        self.jobType=''
        self.notPrefer=[]
        self.skillSets=[]
        
    def printOut(self):
        print 'companyName:', self.companyName
        print 'Title:', self.jobTitle
        print 'isHeadHunter', self.isHeadHunter
        print 'location:', self.location
        print 'postedOn:', self.postedOn
        print 'isOnNOH1BList:', self.isOnNOH1BList
        print 'visa keywords:', self.visaKeywords
        print 'applied:', self.applied
        print 'enterdate:', self.enterDate
        print 'url:', self.url
        print 'is AD:', self.isAd
        print 'job type:', self.jobType
        print 'skillSets ', self.skillSets
        print 'experience ', self.experience
        print 'not prefer ', self.notPrefer
    
    