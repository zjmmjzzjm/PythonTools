import os,sys,getopt,re

class UnityBuildHandler:
    def __init__(self, target_type, target_dir, log_file):
        self.target_type =  target_type
        self.target_dir = target_dir
        self.log_file = log_file
        self.unity_cmd='unity.exe -batchMode -quit -projectPath '
        self.unity_cmd += target_dir + ' -logFile ' + log_file + ' '

    def build_aos(self):
        cmd = self.unity_cmd + '-executeMethod CommandBuild.BuildAndroid'
        print('Building aos : ' + cmd)
        ret = os.system(cmd)
        return ret


    def build_ios(self):
        cmd = self.unity_cmd + '-executeMethod CommandBuild.BuildIOS'
        print('Building ios : ' + cmd)
        ret = os.system(cmd)
        return ret

    def build(self):
        ret = 0
        if  self.target_type.upper() == 'AOS' :
           ret = self.build_aos()
        elif self.target_type.upper() == 'IOS':
           ret = self.build_ios()
        else:
            print('!!Invalid target_type ' + self.target_type)
            return -1
        return ret


def print_usage():
    print(r'''usage:
        python build.py -p project_path -l logfile_path -t buildtype
        Building unity project in commandline mode.
        Example:
        python build.py -p D:\frontend\BladeOfDragon -l D:\unity.log -t  aos

        -p, --project=project_path    Denoting unity project path
        -l, --logfile=logfile_path    Denoting log file path
        -t, --type=target_type        Target platform: AOS=>Android, IOS=>Iphone
        -h, --help                    Print this message


          ''')

if __name__ == '__main__':
    project_dir = r'D:\Workspace\projects\game\trunk\DragonBlade\Dev\frontend\BladeOfDragon'
    logfile =  r'd:\unity.log'
    target_type = 'AOS'
    try:
        opt,arg = getopt.getopt(sys.argv[1:],'p:l:t:h',['project=', 'logfile=', 'type=', 'help'])
        for o,a in opt:
            if o in ('-p', '--project'):
                project_dir = a
            elif o in ('-l', '--logfile'):
                logfile = a
            elif o in ('-t', '--type'):
                target_type = a
            elif o in ('-h', '--help'):
                print_usage()
            else:
                print('Invalid arguments:' + o)
    except getopt.GetoptError as err:
        print('Parsing arguments failed. ' + str(err))
        print_usage()
        exit(-1)

    h = UnityBuildHandler(target_type, project_dir , logfile)
    ret = h.build()
    if ret != 0 :
        print('Building failed. ret ' + ret)
        exit(-1)
