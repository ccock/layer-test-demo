import sys
import os
import shutil
import log
from systemutils import SystemUtils

def getBuildRoot(root):
    return os.path.join(root, 'Build')

def getTestRoot(root):
    return os.path.join(root, 'Test')

def refreshCmake(buildRoot):
    log.banner('start to refresh cmake script...')
    if not os.path.exists(buildRoot):
        os.makedirs(buildRoot)
    os.chdir(buildRoot)
    SystemUtils.exec('cmake ../Test')

def build(buildPath):
    log.banner('start to build %s ...' % buildPath)
    os.chdir(buildPath)
    SystemUtils.exec('cmake --build .')

def run(testPath):
    log.banner('start to run %s ...' % testPath)
    for top, dirs, files in os.walk(testPath):
        for file in files:
            try:
                filePath = os.path.join(top, file)
                if SystemUtils.isTestable(filePath):
                    log.banner('run test of %s ...' % filePath)
                    SystemUtils.exec(filePath)
            except:
                pass

def test(root, target):
    log.banner('start to run %s of %s ...' % (target, getTestRoot(root)))
    buildRoot = getBuildRoot(root)
    refreshCmake(buildRoot)
    build(os.path.join(buildRoot, target))
    run(os.path.join(buildRoot, target))
    log.success('TEST')

def testAll(root):
    log.banner('start to run all of %s ...' % getTestRoot(root))
    buildRoot = getBuildRoot(root)
    refreshCmake(buildRoot)
    build(buildRoot)
    run(buildRoot)
    log.success('TEST')

def clean(root):
    log.banner('start to clean DT')
    buildPath = os.path.join(root, 'Build')
    if os.path.exists(buildPath):
        shutil.rmtree(buildPath)
    log.success('CLEAN')

def main(args):
    thisPath = os.path.split(os.path.realpath(__file__))[0]
    dtRoot = os.path.realpath(os.path.join(thisPath, '..'))
    try:
        if len(sys.argv) == 1:
            testAll(dtRoot)
        elif sys.argv[1] == 'clean':
            clean(dtRoot)
        else:
            test(dtRoot, sys.argv[1])
    except Exception as e:
        log.exception(str(e))
        exit(1)                 


if __name__ == "__main__":
    main(sys.argv)
    