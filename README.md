# Datalogging

## Description

Librairie Python3 permettant de loguer des données dans des fichiers CSV datés.  

## Exemples

### Fonction record

Par défaut les données sont logués dans un fichier `~/data/%Y/%m/%d.dat`. Voici un première exemple utilisant la fonction `record` :  

```python
#!/usr/bin/python3


from datalogging import record


record('foo','bar','ooz')
```

Ce qui créer le fichier `/home/user/data/2018/09/24.dat` contenant :

```
10:02:17|foo|bar|ooz
```

### Class Recorder

```python
#!/usr/bin/python3


from datalogging import Recorder


a = Recorder('a')                                                                                                                    
a.record('foo','bar')                                                                                                                
                                                                                                                                     
b = Recorder('b',fqpnt='/tmp/b/%Y-%m-%d.dat')                                                                                       
b.record('ooz','baz')                                                                                                                
                                                                                                                                     
a.record('foo','bar')                                                                                                                
b.record('ooz','baz')                                                                                                                
a.record('foo','bar')
```

Ce qui donne :  

```bash
# cat /home/user/data/a/2018/09/24.dat                                                                                               
# 11:03:11|foo|bar
# 11:03:11|foo|bar
# 11:03:11|foo|bar
# cat /tmp/b/2018-09-24.dat
# 11:03:11|ooz|baz
# 11:03:11|ooz|baz
```

### Class Recorder, les paramètres

```python
#!/usr/bin/python3


from collections import OrderedDict

from datalogging import Recorder


a = Recorder('a',
             timezone='Europe/Paris',
             fqpnt='/%(~)s/data.dat',
             separator=';',
             ending='\n',
             encoding='utf-8',
             dataheader=('data1','data2'),
             metadata=OrderedDict([('date','%Y-%m-%d'),('time','%H:%M:%S'),]))

a.record('foo','bar')
a.record('foo','bar')
```

Ce qui donne :  

```bash
# cat /home/user/data.dat
date;time;data1;data2
2018-09-25;09:00:49;foo;bar
2018-09-25;09:00:49;foo;bar
```

