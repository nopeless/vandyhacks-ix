import json


def dir_filtered(t):
    return [x for x in dir(t) if not x.startswith("__") and not x.endswith("__")]


def construct_proxy(f, trigger):
    def proxy(*args, **kwargs):
        r = f(*args, **kwargs)
        trigger()
        return r

    return proxy


class JSONFile:
    def __init__(self, path):
        self.path = path

        self.filehandle = open(
            path,
            "w+",
            encoding="utf-8",
        )

        text = self.filehandle.read()

        if text == "":
            text = "{}"

        writing = False

        def trigger():
            nonlocal writing
            if writing:
                return
            writing = True
            try:
                self.filehandle.seek(0)
                self.filehandle.truncate()
                self.filehandle.write(json.dumps(self.data))
            except Exception as e:
                raise e
            finally:
                writing = False

        self.data = JSONObject(json.loads(text), trigger)

    def close():
        self.filehandle.close()


def attr_trigger(f):
    def l(self, name, value, *args, **kwargs):

        # "private" attributes
        if name.startswith("_"):
            super(type(self), self).__setattr__(name, value, *args, **kwargs)
            return

        v = get_value(value, self._trigger)

        super(type(self), self).__setattr__(name, v, *args, **kwargs)

        super(type(self), self).__setitem__(name, v, *args, **kwargs)

        self._trigger()

    return l


class JSONObject(dict):
    def __init__(self, d, trigger):
        super().__init__(d)
        self._trigger = trigger

        for name in dir_filtered(dict):
            f = getattr(super(), name)

            super().__setattr__(name, construct_proxy(f, trigger))

    @attr_trigger
    def __setattr__(self, name, value):
        pass

    def __repr__(self):
        return "JSONObject(" + super().__repr__() + ")"


class JSONArray(list):
    def __init__(self, l, trigger):
        super().__init__(l)
        self._trigger = trigger

        for name in dir_filtered(list):
            f = getattr(super(), name)

            super().__setattr__(name, construct_proxy(f, trigger))

    def __repr__(self):
        return "JSONArray(" + super().__repr__() + ")"


def get_value(v, trigger):
    if isinstance(v, dict):
        return JSONObject({k: get_value(v, trigger) for k, v in v.items()}, trigger)
    elif isinstance(v, list):
        return JSONArray([get_value(v, trigger) for v in v], trigger)
    else:
        return v


j = JSONFile("save.json").data
j.something = {}
j.something.moreprop = 100
j.something.moreprop = [1]
j.something.moreprop.append(2)
j.something.moreprop.reverse()
