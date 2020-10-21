<h1>me</h1>

## **self**

### variables:

n -> tasso di apprendimento, iterazioni durante il learning 

flux -> Flusso di apprendimento.

learned -> {'oggetto':{'%':range,'v':activation_variable}} *p2*

tag -> stringa di identificazione (Man+random.randint(100,1000))

### functions:

1. __init __: 
    1. sets up previous variables.

1. learn:
    1. gen:
        1. generate till res != 0
    1. get datas using obj.activate()
    1. convert data to a rasterized matrix [0,1..]
        1. ``` int(100*(sum(raster(d))/len(d))) ```
    1. update learned dict using its syntax

1. communicate:
    1. raise NotImplementedError

## **Flux**

### add
```python
man.flux.add(obj)
```
convert obj to Urge and append it to elements

### process
```python
man.flux.process()
```
flush() the first element of elements if len(elements)

## **Urges**

### activate
```python
urge.activate(obj)
```
applica un incremento contenuto nel range obj.val alla variabile obj.(urge.var)

passa self come obj per attivare su te stesso l'effetto.

### flush
```python
urge.flush(obj)
```
(come prima, passa self come obj per attivare su te stesso)
passa urge a obj.learn() e si autorimuove dagli elementi del flusso di obj
(obj.flux.elements)

# Events
## **cos'è un evento**

```
un evento è un insieme di Urge()s che seguendo l'ordine in Event.sorts[:]

 vanno ad eseguirsi in Event.target
 ```

## **internal structure**

### Variables:

1. sorts -> ordine di attivazione -type = list
2. target -> Human item -------- type = Human
3. urges -> impulsi da attivare -- type = Urge

### Functions:

1. Activate:

## **Syntax**

### creazione:

```python
Event.make(urge1, urge2 ...)
```
Event.make ha *args come argomento, ogni Urge passato viene aggiunto a Event.urges e in sorts verranno scritti secondo l'ordine dato alla creazione, in questo caso sorts=[urge1, urge2 ...]

### attivazione:

```python
Event.activate(me) # me is the Human instance
``` 
aggiunge a me tutti gli Urge di Event.urges in ordine Event.sorts ed esegue flusha un Urge per volta, alternando flush() a me.mainloop()

<h1>making</h1>

## instanciate:

```python
me = Human(n)
```

this will exec:
1. Human.init()
    1. only sets up variables and **flux** passing self

1. Flux.init(man)
    1. self.man=man; elements=list()

## make a Urge
```python
u=Urge(var, val||range)
```
this will exec:

1. Urge.init(var, val||range)
    1. set var and if range val=0 else range=None

## activate a Urge
```python
u.activate(me)
```
me is passed as obj

1. choose range or val
    1. if range do; else range(-val, val)
1. se var inizia con $ è una variabile sentimento
    1. aggiungi un valore casuale nel range scelto a me.var o me.feels[var]
1. ritorna il valore sommato.

## make an Event
```python
e=Event(me, u1, u2)
```
> [type(i) for i in args] only <class:"Urge">

1. Event.init(target=me, args=(u1, u2,))
    1. self.urges=[u1,u2]
    1. self.target=me

## activate an Event
```python
e.activate()
```
1. aggiungi tutti gli elementi di e.urges al flux di e.target
    1. flux.add(urge in e.urges uno per uno)
        1. se è uno urge aggiungi a flux.elements sennò rendilo tale e aggiungi
    1. flux.process() processa il primo elemento aggiunto
1. ritorna None
