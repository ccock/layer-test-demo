
def lineSpliter():
    print('*' * 60)

def banner(info):
    lineSpliter()
    print('[DT]: ' + info)

def success(info):
    lineSpliter()
    print('[DT]: %s SUCCESS!' % info)

def fail(info):
    lineSpliter()
    print('[DT]: %s FAILED!' % info)

def exception(info):
    lineSpliter()
    print('[DT] Failed because of %s!' % info)
