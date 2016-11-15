import pytest

@pytest.fixture(params=['new', 'old'])
def Test(request):
    # Sadly, I have to have two blocks of almost identical code to test both
    # old and new style classes.
    if request.param == 'new':
        class Test(object):
            value = 'value'
            def __getitem__(self, key):
                if key == 'getitem':
                    return self.value
            def __setitem__(self, key, value):
                if key == 'getitem':
                    self.value = value
            def __delitem__(self, key):
                print 'DELITEM FTW'
                if key == 'getitem':
                    self.value = None
            def keys(self):
                return ['getitem']
        return Test
    else:
        class Test:
            value = 'value'
            def __getitem__(self, key):
                if key == 'getitem':
                    return self.value
            def __setitem__(self, key, value):
                if key == 'getitem':
                    self.value = value
            def __delitem__(self, key):
                print 'DELITEM FTW'
                if key == 'getitem':
                    self.value = None
            def keys(self):
                return ['getitem']
        return Test

@pytest.fixture
def context(Test, context):
    context.Test = Test
    context.test = Test()
    return context
    
def test_getitem(context):
    assert context.eval('test.getitem') == 'value'

def test_setitem(context):
    context.eval('test.getitem = "harambe"')
    # proof harambe is still alive
    assert context.eval('test.getitem') == 'harambe'

def test_delitem(context):
    test = context.eval('test = new Test()')
    assert context.eval('test.getitem') == 'value'
    context.eval('delete test.getitem')
    assert context.eval('test.getitem') == None

def test_query(context):
    descriptor = context.eval('Object.getOwnPropertyDescriptor(test, "getitem")')
    assert descriptor.writable
    assert not descriptor.enumerable
    assert descriptor.configurable
    assert descriptor.value == 'value'

def test_enumerate(context):
    name_list = context.eval('Object.getOwnPropertyNames(test)')
    assert len(name_list) == 1
    assert name_list[0] == 'getitem'