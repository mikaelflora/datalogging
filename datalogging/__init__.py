#!/usr/bin/python3
# -*- coding: utf-8 -*-


__version__ = '%(prog)s 0.1'
__author__  = 'Mikael Flora'
__all__     = ['Formatter','Recorder','record']


import os

from collections import Mapping
from collections import Iterable
from collections import OrderedDict
from os          import makedirs
from os          import path
from datetime    import datetime as dt
from pytz        import timezone as tz
from dateutil.tz import tzlocal


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func,k,kwargs[k])
        return func
    return decorate


@static_vars(init=None)
def record(*data):
    if not record.init:
        record.init = Recorder('')
    record.init.record(*data)


class Formatter(dict):
    def __init__(self, inp=None):
        self._mode = 'p'
        if isinstance(inp,dict):
            super(Formatter,self).__init__(inp)
        else:
            super(Formatter,self).__init__()
            if isinstance(inp, (Mapping, Iterable)): 
                si = self.__setitem__
                for k,v in inp:
                    si(k,v)
        self.__setitem__('~', path.expanduser('~'))

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if mode not in set('pur'):                              # p: pass
            raise ValueError("invalid mode '{}'".format(mode))  # u: update
        self._mode = mode                                       # r: raise

    def __setitem__(self, k, v):
        try:
            self.__getitem__(k)
            if self._mode == 'u':
                super(Formatter,self).__setitem__(k,v)
            elif self._mode == 'r':
                raise ValueError("duplicate key '{}' found".format(k))
        except KeyError:
            super(Formatter,self).__setitem__(k,v)


class Recorder():
    def __init__(self,
                 name,
                 timezone=None,
                 fqpnt=path.join('%(~)s','data','%(name)s','%Y','%m','%d.dat'),
                 separator='|',
                 ending='\r\n' if os.name == 'nt' else '\n',
                 encoding='utf-8',
                 dataheader=list(),
                 metadata=OrderedDict([('time','%H:%M:%S'),])):
        if timezone:
            self._timezone = tz(timezone)
        else:
            self._timezone = tzlocal()
        self._now        = dt.now(self._timezone)
        self._name       = str(name).strip()
        self._fqpnt      = str(fqpnt)
        self._separator  = str(separator)
        self._ending     = str(ending)
        self._encoding   = str(encoding)
        self._metadata   = metadata
        self._dataheader = dataheader
        self._formatter               = Formatter()
        self._formatter['name']       = self._name
        self._header     = True if len(dataheader) else False

    def format(self, entry):
        return self._now.strftime(entry) % self._formatter

    def fqpn(self):
        return self.format(self._fqpnt)

    def header(self):
        header  = self._separator.join(map(str,self._metadata.keys()))
        header += self._separator
        header += self._separator.join(map(str,self._dataheader))
        if header[-len(self._ending):] != self._ending:
             header += self._ending
        return self.format(header)

    def metadata(self):
        metadata  = self._separator.join(map(str,self._metadata.values()))
        return self.format(metadata)

    def record(self, *data):
        self._now = dt.now(self._timezone)
        fqpn = self.fqpn()
        dat  = self.metadata()
        dat += self._separator
        dat += self._separator.join(map(str,data))
        if dat[-len(self._ending):] != self._ending:
             dat += self._ending
        try:
            open(self.fqpn(), 'r').close()
        except FileNotFoundError:
            makedirs(path.dirname(self.fqpn()), exist_ok=True)
            if self._header:
                with open(self.fqpn(),'a') as f:
                    f.write(self.header())
        finally:
            with open(self.fqpn(), 'a', encoding=self._encoding) as f:
                f.write(dat)

