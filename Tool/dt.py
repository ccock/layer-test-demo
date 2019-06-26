import argparse
import sys
import os
import shutil
import log
from systemutils import SystemUtils

def getBuildRoot(root):
    return os.path.join(root, 'Build')

def getTestRoot(root):
    return os.path.join(root, 'Test')

def getCodeRoot(root):
    return os.path.join(root, '../hert_bsp/Source')

def generateParentCMakeListsFile(testPath, dirs):
    print('generateParentCMakeListsFile in %s' % testPath)
    print(dirs)

def generateProjectCMakeListsFile(testPath, parent, files):
    print('generateProjectCMakeListsFile in %s of %s' % (testPath, parent))
    print(files)

def generateTestFile():
    print('generateTestFile')

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

def create(root, path):
    log.banner('create DT project for %s ...' % path)
    testRoot = getTestRoot(root)
    projectRoot = os.path.join(getCodeRoot(root), path)
    for parent, dirs, files in os.walk(projectRoot):
        testPath = os.path.join(testRoot, parent)
        if not os.path.exists(testPath):
            os.makedirs(testPath)
            if not SystemUtils.existCFile(files) and len(dirs) > 0:
                generateParentCMakeListsFile(testPath, dirs)
            elif SystemUtils.existCFile(files):
                generateProjectCMakeListsFile(testPath, parent, files)
                generateTestFile()
            else:
                pass
    log.success('CREATE')      

def main():
    parser = argparse.ArgumentParser(description = 'cup : c++ unified package management tool')
    subparsers = parser.add_subparsers(help = 'commands')

    new_parser = subparsers.add_parser('create', help = 'create project')
    new_parser.add_argument('path', action = 'store', help = 'project path')
    new_parser.set_defaults(func = create)   

    add_parser = subparsers.add_parser('clean', help = 'clean project')
    add_parser.add_argument('path', action = 'store', help = 'project path')
    add_parser.set_defaults(func = clean)    

    build_parser = subparsers.add_parser('build', help = 'build project')
    build_parser.add_argument('path', action = 'store', help = 'project path')
    build_parser.set_defaults(func = build)  

    test_parser = subparsers.add_parser('test', help = 'test project')
    test_parser.add_argument('path', action = 'store', help = 'project path')
    test_parser.add_argument('-p', '--paras', action = 'store', default = '', help = 'test parameters')
    test_parser.set_defaults(func = test)   

    args = parser.parse_args()
    args.func(args)    


if __name__ == '__main__':
    try:
        main()
        exit(0)
    except Exception as e:
        log.exception(str(e))
        exit(1)  
    