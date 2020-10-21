import json
import time, random
from colors import bcolors as css

random.seed(time.time())

def ConvertionError(message):
    print(css.FAIL+'[!!]', message, css.ENDC)
    exit(code=1)

def toUrge(x):
    try:
        return Urge(x['var'], x['val'])
    except:
        ConvertionError('line 16, cannot convert '+str(type(x))+' to urge.')

def raster(x):
    for item in x:
        if not item:
            x[x.index(item)]=0
    res=[1 if i>0 else 0 for i in x]
    return res

class BaseHandler():
    def __init__(self):
        self.rng=None
        self.activate=Urge.activate

class Urge():
    def __init__(self, var:str, val:int=0, steps:int=1, _range:range=None, slags=1, f=None):
        self._range=_range
        self.var=var
        self.outrange=range(-abs(val), abs(val), steps)
        self.slags=slags
        if not f:
            self.can_activate=True
        else: self.can_activate=False
    def getKey(self):
        if self._range:
            return 'U'+str(self.var)+str(self._range)
        else:
            return 'U'+str(self.var)+str(self.outrange)
    def activate(self, obj):
        if not can_activate: return 'Cannot Access This Resource, access denied.'
        if not self._range:
            s=self.outrange[random.randint(0,len(self.outrange)-1)]
        else:
            s=self._range[random.randint(0,len(self._range)-1)]
        if self.var.startswith('$'):
            var=''.join(self.var.split('$'))
            try:
                #setattr(obj, obj.feels[var], getattr(obj.feels[var], self.var)+s)
                #print('feels:',obj.feels,'s:',s,'var:',var)
                obj.feels[var]+=s
            except:
                #setattr(obj, self.var, s)
                print(css.WARNING, 'line 37, exception block', css.ENDC)
            return s
        try:
            setattr(obj, self.var, getattr(obj, self.var)+s)
        except:
            setattr(obj, self.var, s)
        return s
    def flush(self, obj):
        #obj.man.learned.update({self:self.r})
        #print('check, me:',self.getKey(),'and',obj.man.learned,'and',obj.man.flux.elements[0].getKey())
        if self.getKey() in obj.man.learned.keys():
            print(css.background.RED+'line 58'+css.ENDC+css.FAIL+' flush is skipping learning cause',self.getKey(),'is already in',obj.man.learned.keys(),'->',obj.man.learned,css.ENDC)
        else:
            obj.man.learn(self)
        self.slags-=1
        if self.slags<=0:
            obj.elements.remove(self)
        #return self.r[random.randint(0,len(self.r))]

class Flux():
    def __init__(self, man):
        self.man=man
        self.elements=[]
    def add(self, obj):
        #print(text)
        if isinstance(obj, Urge):
            self.elements.append(obj)
        else:
            self.elements.append(toUrge(obj))
    def process(self, mode='std'):
        #print('check, me:',self.elements,'and',self.man.learned)
        #if mode=='std':
        try:
            self.elements[0].flush(self)
        except:
            print(css.FAIL+'[!!] No Urge to flux.'+css.ENDC)
        '''elif mode=='*':
            for i in self.elements:
                i.flush(self)'''

class Human():
    def __init__(self, learning_rate=10, train_on_spawn=False, show_logs=False, **feels):
        self.n=learning_rate
        self.flux=Flux(self)
        self.learned={}
        self.tag='Man'+str(random.randint(100,1000))
        self.log_showed=1
        self.shl=show_logs
        # --- test variables ---
        self.hp=100 
        self.feels={'h':0, 's':0} # feelings, h->happyness s->sadness
        # --- if specified, learn some feels
        if train_on_spawn:
            if 'urges' in feels.keys() or 'feels' in feels.keys():
                if 'urges' in feels.keys():k='urges'
                else: k='feels'
                for u in feels[k]:
                    if isinstance(u, Urge):
                        self.learn(u)
                    else:
                        print(css.FAIL+'cannot learn a non-urge object, type-> '+str(type(u))+css.ENDC)
                        break
            else: # learn std feels 
                raise NotImplementedError('now instanciate pain, sadness, happyness and learn them')
    def entire_log(self, **kws):
        # std variables
        color=css.OKBLUE
        print(css.background.RED+'[INFO]'+css.ENDC+' Showing for the '+css.HEADER+str(self.log_showed)+css.ENDC+' times:')
        self.log_showed+=1
        # customizing
        if 'color' in kws.keys():
            color=kws['color']
        if 'flux' in kws.keys():
            if kws['flux']:
                pass
            else:
                flux=False
        # print out
        print(css.background.RED+'[INFO]'+css.ENDC+css.HEADER+' Me log:'+css.ENDC)
        for a, b in zip(self.__dict__.keys(), self.__dict__.values()):
            print(css.OKCYAN, a,css.ENDC+'->',css.OKGREEN,b, css.ENDC)
        print(css.background.RED+'[INFO][specs]'+css.ENDC+css.HEADER+' Flux Details:'+css.ENDC)
        for a, b in zip(self.flux.__dict__.keys(), self.flux.__dict__.values()):
            print(css.OKCYAN, a,css.ENDC+'->',css.OKGREEN,b, css.ENDC)
        i=1
        for item in self.flux.elements:
            print('\r',css.HEADER+'Flux',i,'Element:',css.ENDC,item)
            i+=1
        return
        #print(color,'main dict:',self.__dict__, css.ENDC)
    def learn(self, obj):
        def gen(x):
            r=random.randint(min(x),max(x))
            if not r==0:
                return r
            else:
                gen(x)
        d=[]
        for _ in range(self.n):
            val=obj.activate(self)
            if not val==0:
                d.append(val)
            else:
                pass
        # rebuild d
        if not len(d)==self.n:
            for _ in range(self.n-len(d)):
                #print(obj.__dict__)
                if obj.outrange==range(0,0):
                    d.append(gen(obj._range))
                    continue
                d.append(gen(obj.outrange))
        #print('dict:',d)
        r=int(100*(sum(raster(d))/len(d)))
        self.learned.update({obj.getKey():{'%':r,'v':obj.var}})
        if self.shl:
            print(css.YELLOW+'object',obj,'successfully learned and '+css.BOLD+'learned(dict)'+' updated with:',obj.getKey()+':','%:',r,'var: '+obj.var+css.ENDC)
    def communicate(self, x):
        print(css.OKGREEN+self.tag,'->'+css.ENDC,x)
    def Percept(self, obj):
        if isinstance(obj, Event):
            obj.activate()
            return
        elif isinstance(obj, Urge):
            #print('is a urge')
            obj.activate(self)
            return
        else:
            ConvertionError('line 98, object must be Urge or Event.')
    def mkf(self, source:'class', *urges, **kwargs):
        '''
        Make Function()
        questo metodo crea una funzione in modo da gestire in modo specifico uno Urge
        source (classe) -> classe sorgente per l'handling
        se kwargs['readHDL'] è True allora legge la stringa source come codice hdl da
        compilare e rendere pycode.
        '''
        #raise NotImplementedError('mkf became a function in mpp1.2a')
        # use only function, NotImplementedError for hdl
        def get_range(key:str):
            o1=key.split('range')[1][1:-1]
            o2=[int(i) for i in o1.split(', ')]
            return o2
        if 'readHDL' in kwargs:
            raise NotImplementedError('hdl files are not implemented.')
        else:
            return source.activate(source, 'ciao')
    
    def extend(self, func, *args, **kwargs):
        return

class Event():
    def __init__(self, target, *args):
        self.urges=[*args]
        self.sorts='std'
        self.target=target
    def activate(self):
        #print(self.urges)
        for u in self.urges:
            print(css.WARNING+'activating',u,'...',css.ENDC)
            self.target.flux.add(u)
            self.target.Percept(u)
        self.target.flux.process() # process only the first urge
        return

class NewHandler(BaseHandler):
    def activate(self, text):
        print('subclass ->',text)
        super().activate(self, text)

'''
u=Urge('hp', 5)
me=Human()
me.mkf(source=NewHandler)
'''
'''
# --- DEFINES ---
sadness=Event(me, Urge('hp', 4), Urge('$h', _range=range(-5, 0)))
temp=Urge('hp', _range=range(-1,5))

# --- MAIN ---

me.entire_log()
me.Percept(sadness)
#print('flux elements:',me.flux.elements)
me.flux.process()
me.Percept(temp)
me.entire_log(flux=False, color=css.OKGREEN)
#me.flux.process(); me.entire_log()
print(sadness)

functions:
1. init: set up variables -> self
    1. **self.n=n** -> learning rate
    1. **self.flux** -> an instance of Flux
    1. **learned** -> dict {obj.getKey():obj.specs}
    1. **tag** -> string
1. entire_log: print out self specs -> str
    1. colors, flux .. customization
    1. print obj.dict formatted


me=Human()
u1=Urge(input('new urge var>> '), int(input('max value: '))) # make a new urge
u2=Urge(input('urge var>> '), int(input('value: ')))
print('me:',me.__dict__,'\nflux:',me.flux.elements)
e=Event(me, u1, u2)
e.activate()
print('me:',me.__dict__,'\nflux:',me.flux.elements)
me.flux.process('*')


me.flux.add(u)
print(css.WARNING,me.flux.elements, me.__dict__, css.ENDC)
print('[*] Processing flux')
me.flux.process()
print(css.WARNING,me.flux.elements, me.__dict__,css.ENDC)
u.activate(me)
print(css.WARNING,me.flux.elements, me.__dict__,css.ENDC)
'''