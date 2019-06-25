import os
import subprocess


class SystemUtils:
    @classmethod
    def exec(cls, cmd):
        status, output = subprocess.getstatusoutput(cmd)
        print(output)
        if status != 0:
            raise Exception("execute '%s' failed" % cmd)

    @classmethod
    def isExecutable(cls, filePath):
        if cls.get_postfix(filePath) == 'exe':
            return True
        return os.path.isfile(filePath) and os.access(filePath, os.X_OK)

    @classmethod
    def isTestable(cls, filePath):
        if not cls.isExecutable(filePath):
            return False
        postfix = cls.get_postfix(filePath)
        if postfix:
            if 'bin' in postfix:
                return False
            if 'out' in postfix:
                return False
            if 'o' in postfix:
                return False
        if 'TEST' in cls.get_base_name(filePath):
            return True
        if 'test' in cls.get_base_name(filePath):
            return True
        if 'Test' in cls.get_base_name(filePath):
            return True
        return False

    @classmethod
    def get_full_path(cls, relative_path):
        return os.path.join(os.getcwd(), relative_path)

    @classmethod
    def get_path(cls, path):
        return os.path.split(path)[0]

    @classmethod
    def get_name(cls, path):
        return os.path.split(path)[1]

    @classmethod
    def get_base_name(cls, path):
        return cls.get_name(path).split('.')[0]

    @classmethod
    def get_postfix(cls, path):
        temp = cls.get_name(path).split('.')
        return None if len(temp) == 1 else temp[-1]        

    @classmethod
    def find_file_by_name(cls, path, filename):
        for file in os.listdir(path):
            fp = os.path.join(path, file)
            print(file)
            print(fp)
            if os.path.isfile(fp) and file == filename:
                return fp
            elif os.path.isdir(fp):
                result =  cls.find_file_by_name(fp, filename) 
                if result is not None : return result
        return None       
