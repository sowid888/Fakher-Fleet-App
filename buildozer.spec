[app]

# (str) Title of your application
title = Fakher Fleet

# (str) Package name
package.name = fakherfleet

# (str) Package domain (needed for android/ios packaging)
package.domain = org.fakher

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,txt,db,otf,ttf

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy,requests,urllib3,certifi,idna

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) List of Java .jar files to add to the libs dir
#android.add_jars = foo.jar,bar.jar

# (list) The Android architectures to build for
# تحديد معمارية واحدة فقط لمنع استهلاك الوقت وتوقف البناء
android.archs = arm64-v8a

# (bool) Enable AndroidX support
android.gradle_dependencies = 

# (bool) Accept SDK licenses automatically
android.accept_sdk_license = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = error, 1 = warning)
warn_on_root = 1
