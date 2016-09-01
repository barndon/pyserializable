import json

class Encoder(json.JSONEncoder):

    def __init__(self, **kwargs):
        super(Encoder, self).__init__()
        if 'camel_case' in kwargs:
            self.camel_case = kwargs['camel_case']


    def default(self, o):
        return o.to_dict(camel_case=self.camel_case)

class Decoder(object):

    def __init__(self, **kwargs):
        if 'camel_case' in kwargs and kwargs['camel_case'] == True:
            self.object_hook = ensure_camel_case_keys
        else:
            self.object_hook = ensure_snake_case_keys

    def loads(self, jstr, **kwargs):
        return json.loads(jstr, object_hook=self.object_hook, **kwargs)

class Serializable(object):

    def __str__(self):
        return '%r' % self.to_dict(camel_case=False)

    def __repr__(self):
        return '%r' % self.to_dict(camel_case=False)

    def to_dict(self, **kwargs):

        omit_nulls = False
        if 'omit_nulls' in kwargs and kwargs['omit_nulls'] == True:
            omit_nulls = True

        d = dict()
        if 'camel_case' in kwargs and kwargs['camel_case'] == True:
            for k in self.__dict__.keys():
                k2 = to_camel_case(k)

                if isinstance(self.__dict__[k], list):
                    d[k2] = []
                    for v in self.__dict__[k]:
                        if isinstance(v, Serializable):
                            d[k2].append(v.to_dict(**kwargs))
                        else:
                            if v != None or omit_nulls == True:
                                d[k2].append(v)

                if isinstance(self.__dict__[k], Serializable):
                    d[k2] = self.__dict__[k].to_dict(**kwargs)
                else:
                    if self.__dict__[k] != None or omit_nulls == True:
                        d[k2] = self.__dict__[k]

            return d
        else:
            return self.__dict__


def ensure_camel_case_keys(idct):
    odct = dict()
    for key, value in idct.iteritems():
        camel_key = to_camel_case(key)
        odct[camel_key] = value
    return odct


def ensure_snake_case_keys(idct):
    odct = dict()
    for key, value in idct.iteritems():
        snake_key = to_snake_case(key)
        odct[snake_key] = value
    return odct


def either_or(a, b, dct):
    return dct[a] if a in dct else dct[b] if b in dct else None


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + "".join(x.title() for x in components[1:])


def to_snake_case(camel_str):
    ostr = str()
    prev = None

    for c in camel_str:
        if c.isupper():
            if prev == None or prev == ' ':
                ostr += c.lower()
            else:
                ostr += '_' + c.lower()
        else:
            ostr += c
        prev = c

    return ostr
