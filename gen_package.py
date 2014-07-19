__author__ = 'dongdaqing'

import os

class Gen_Package(object):

    def __init__(self):
        self.project_path = "/Users/dongdaqing/workspace/iOS/UICatalog"
        self.app_path = os.path.join(self.project_path, 'app_path')
        if not os.path.exists(self.app_path):
            os.mkdir(self.app_path)

        self.ipa_path = os.path.join(self.project_path, 'ipa_path')
        if not os.path.exists(self.ipa_path):
            os.mkdir(self.ipa_path)

    def gen_app(self):
        os.chdir(self.project_path)
        clean_app_command = "xcodebuild -scheme UICatalog -configuration Release\
         -derivedDataPath {0} clean".format(self.app_path)
        build_app_command = "xcodebuild -scheme UICatalog -configuration Release\
         -derivedDataPath {0} build".format(self.app_path)
        os.system(clean_app_command)
        os.system(build_app_command)

    def gen_ipa(self):
        os.chdir(self.project_path)
        # build_ipa_command = "xcrun -sdk iphoneos PackageApplication \
        # -v {0}/Build/Products/Release-iphoneos/UICatalog.app \
        # -o {1}/UICatalog.ipa".format(self.app_path,self.ipa_path)
        build_ipa_command = "xcrun -sdk iphoneos PackageApplication \
        -v {0}/Build/Products/Release-iphoneos/UICatalog.app \
        -o {1}/UICatalog.ipa \
        --sign 'iPhone Developer: xxxxxx' \
        --embed {2}/*.mobileprovision".format(self.app_path,self.ipa_path,self.project_path)
        os.system(build_ipa_command)

if __name__ == '__main__':

    gen_package_obj = Gen_Package()
    gen_package_obj.gen_app()
    gen_package_obj.gen_ipa()
