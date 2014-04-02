#encoding: UTF-8
import os,shutil,sys,re,getopt
#C://user/zjm
mydir=os.path.expanduser('~')
latest_vesion_name='LatestVersionListV2.txt'

webroot='D:\\Apps\\xampp\\htdocs\\DragonBlade\\'
web_bundle_dir=webroot + 'Alpha\\Android\\AssetBundle\\'
web_design_dir=webroot +  'Alpha\\Android\\Design\\'

persistence_root_dir=mydir+'\\AppData\\LocalLow\\Cherry Online Game\\Blade Of Dragon\\'
persistence_bundle_dir=persistence_root_dir + 'AssetBundle\\'
persistence_Design_dir=persistence_root_dir + 'Design\\'

#project_dir='D:\\Workspace\\projects\\game\\trunk\\mobile_fight\\frontend\\BladeOfDragon\\Assets\\'
project_dir='D:\\Workspace\\projects\\game\\trunk\\DragonBlade\\Dev\\frontend\\BladeOfDragon\\Assets\\'
custom_root_dir=os.path.join(project_dir,'CustomAssetBundle')

def copy_spec_file(srcdir, targetdir, filter=None):
    is_filter_ok=False
    if (filter is None) == False:
        pattern=re.compile(filter)


    for f in os.listdir(srcdir):
        srcfile=os.path.join(srcdir, f)
        targetfile=os.path.join(targetdir, f)
        if os.path.isfile( srcfile ) == False:
            continue

        is_filter_ok=False
        if  not (filter is None) and pattern.match(f):
            is_filter_ok = True

        if is_filter_ok == False:
            continue;
        shutil.copy(srcfile, targetfile)

def remove_files_in_dir(dirname):
    for f in os.listdir(dirname):
        fn=os.path.join(dirname, f)
        os.remove(fn)

def pre_make():
    print("Hi\n")

def after_make():
    print('after make')

def prepare_for_version_list():
    #delet all files in persistenceDataPath
    remove_files_in_dir(persistence_bundle_dir)
    #copy web assetbundle to persistence_bundle_dir
    copy_spec_file(web_bundle_dir, persistence_bundle_dir, r'.*unity3d$' )
    #override new bundle file
    copy_spec_file(custom_root_dir, persistence_bundle_dir, r'.*unity3d$' )

#next you should RemakeVersionList
def deploy_bundle():
    #and next copy VersionList to the webrootdir
    verlist=os.path.join(custom_root_dir, latest_vesion_name )
    if os.path.isfile(verlist):
        print(verlist)
    else:
        print("not a file")

    remove_files_in_dir(web_bundle_dir)
    shutil.copy(verlist, web_bundle_dir)
    copy_spec_file(persistence_Design_dir, web_design_dir)

    copy_spec_file(custom_root_dir, web_bundle_dir, r'.*unity3d$' )

print("==============begin")

try:
    opts,args=getopt.getopt(sys.argv[1:], 'pdv:ht',['prepare','deploy','help','verbose=','test'])
    print(opts)
    for o,a in opts:
        if o in  ('-p', '--prepare'):
            print('call prepare')
            prepare_for_version_list()
        elif o in ('-d','--deploy'):
            print('call deploy')
            deploy_bundle()
        elif o in ('-t','--test'):
             print(__name__)
        elif o in ('-h','--help'):
            print('-p, --prepare prepare for RemakeVersionList\n-d, --deploy finally deploy the bundles\n')
except getopt.GetoptError:
     sys.exit()



print("===============Ok")
