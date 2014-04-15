import os,sys,getopt,re

class UnityBuildHandler:
    def __init__(self, target_type, target_dir, log_file, buildtype):
        self.target_type =  target_type
        self.target_dir = target_dir
        self.log_file = log_file
        self.buildtype = buildtype
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
        if self.buildtype.upper() == "APP":
            if  self.target_type.upper() == 'AOS' :
                ret = self.build_aos()
            elif self.target_type.upper() == 'IOS':
                ret = self.build_ios()
            else:
                print('!!Invalid target_type ' + self.target_type)
                return -1
        elif self.buildtype.upper() == "PATCH":
            ret = self.build_patch();
        elif self.buildtype.upper() == "DESIGN":
            ret = self.build_design_data();
        elif self.buildtype.upper() == "VERSION":
            ret = self.build_version();
        else:
            print('!!Invalid build type : ' + self.buildtype)
            return -1
        return ret

    def build_patch(self):
        cmd = self.unity_cmd + '-executeMethod CommandBuild.BuildAssetBundles'
        print('Building patch: ' + cmd)
        ret = os.system(cmd)
        return ret

    def build_design_data(self):
        cmd = self.unity_cmd + '-executeMethod CommandBuild.BuildSqliteTemplate'
        print('Building Binarys: ' + cmd)
        ret = os.system(cmd)
        return ret

    def build_version(self):
        cmd = self.unity_cmd + '-executeMethod CommandBuild.buildVersionList'
        print('Building version: ' + cmd)
        ret = os.system(cmd)
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
        -b, --buildtype=buildtype     What kind of build, App or Patch or design or version
        -h, --help                    Print this message


          ''')

if __name__ == '__main__':
    project_dir = r'D:\Workspace\projects\game\trunk\DragonBlade\Dev\frontend\BladeOfDragon'
    logfile =  r'd:\unity.log'
    target_type = 'AOS'
    build_type = "App"
    try:
        opt,arg = getopt.getopt(sys.argv[1:],'b:p:l:t:h',['buildtype=','project=', 'logfile=', 'type=', 'help'])
        for o,a in opt:
            if o in ('-p', '--project'):
                project_dir = a
            elif o in ('-l', '--logfile'):
                logfile = a
            elif o in ('-t', '--type'):
                target_type = a
            elif o in ('-b', '--buildtype'):
                build_type = a
            elif o in ('-h', '--help'):
                print_usage()
                exit(0)
            else:
                print('Invalid arguments:' + o)
                exit(-1)
    except getopt.GetoptError as err:
        print('Parsing arguments failed. ' + str(err))
        print_usage()
        exit(-1)

    print("====================================================================")
    print("project_dir: " + project_dir)
    print("logfile: " + logfile)
    print("target_type: " + target_type)
    print("build_type: " + build_type)
    print("====================================================================")

    h = UnityBuildHandler(target_type, project_dir , logfile, build_type)
    ret = h.build()
    if ret != 0 :
        print('Building failed. ret ' + ret)
        exit(-1)
