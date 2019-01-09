import pickle
from functools import wraps
from time import sleep


PICKLE_OBJ_DICT = {}
FUNC_CALL_ID_DICT = {}
FUNC_ID_DICT = {}


def _get_func_code(func):
    if type(func).__name__ == 'function':
        func_byte_code = func.__code__.co_code
    elif type(func).__name__ == 'instancemethod':
        func_byte_code = func.__func__.__code__.co_code
    else:
        raise TypeError('{} is not a function nor a instancemethod'.format(func))
    return func_byte_code

def _get_func_id(func):
    func_byte_code = _get_func_code(func)
    for fid, bcode in FUNC_ID_DICT.items():
        if bcode == func_byte_code:
            return fid
    # not founded, add one
    fid = len(FUNC_ID_DICT) + 1
    func_byte_code = _get_func_code(func)
    FUNC_ID_DICT[fid] = func_byte_code
    return fid


def _get_id(func, args, kwargs):
    for _id, lst in FUNC_CALL_ID_DICT.items():
        fid = _get_func_id(func)
        if lst == [fid, args, kwargs]:
            return _id
    return 0

def _set_id(func, args, kwargs, _id):
    fid = _get_func_id(func)
    FUNC_CALL_ID_DICT[_id] = [fid, args, kwargs]

def _pickle(obj):
    data = pickle.dumps(obj)
    _id = len(PICKLE_OBJ_DICT) + 1
    PICKLE_OBJ_DICT[_id] = data
    return _id


def _unpickle(_id):
    data = PICKLE_OBJ_DICT[_id]
    return pickle.loads(data)


def repeaty_wrapper():
    def wrap(func):
        @wraps(func)
        def call(*args, **kwargs):
            _id = _get_id(func, args, kwargs)
            if _id:
                return _unpickle(_id)
            else:
                obj = func(*args, **kwargs)
                _id = _pickle(obj)
                _set_id(func, args, kwargs, _id)
                return obj
        return call
    return wrap

@repeaty_wrapper()
def testfunc2(arg1, arg2):
    sleep(3)
    return arg1 + arg2
from IPython import embed
embed()