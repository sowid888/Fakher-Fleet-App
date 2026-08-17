[app]

# (str) Title of your application
title = Fakher Fleet

# (str) Package name
package.name = fakherfleet

# (str) Package domain
package.domain = com.fakher.fleet

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (str)
source.include_exts = py,png,jpg,kv,atlas,json,db

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (str)
#source.exclude_exts = spec

# (list) List of directory to exclude (str)
#source.exclude_dirs = tests, bin, venv, .buildozer, .git

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,README.md

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.1

# (str) Custom source folders for requirements
# Sets custom source for any requirement with recipes
# requirements.source.kivy = ../kivy

# (str) Presplash animation
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = MyServiceName:%(source.dir)s/myservice.py

# (bool) Fullscreen mode (0 or 1)
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, white, black, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = white

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
android.ndk = 25c

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip python-for-android compilation
#android.skip_update = False

# (bool) If True, then automatic update python-for-android is enabled
#android.accept_sdk_license = True

# (list) Android application meta-data to set (key=value)
#android.meta_data =

# (list) Android library project to add (paths)
#android.add_libs_to_resource =

# (str) python-for-android git repo to use for Buildozer
#p4a.fork = kivy

# (str) python-for-android git branch to use for Buildozer
#p4a.branch = master

# (str) python-for-android git commit to use for Buildozer
#p4a.commit = HEAD

# (str) python-for-android source code directory
#p4a.source_dir =

# (str) Command line arguments to pass to p4a create --dist_name option
#p4a.extra_args =

# (list) List of Java .jar files to add to the libs / sqlite inputs
#android.add_jars = foo.jar,bar.jar,%(source.dir)s/libs/baz.jar

# (list) List of Java files to add to the project (Androdi target only)
#android.add_src =

# (list) Android AAR archives to add
#android.add_aars =

# (list) Put these files or directories in the apk assets directory
#android.add_assets =

# (list) Gradle dependencies to add
#android.gradle_dependencies =

# (bool) Enable AndroidX support.
android.enable_androidx = True

# (list) List of gradle repositories to add
#android.gradle_repositories =

# (list) Packaging options to pass to gradle
#android.add_packaging_options =

# (list) Java classes to add as entry points
#android.add_activities = com.example.ExampleActivity

# (str) OUName of OU
#android.ou_name =

# (str) Organization Name
#android.organization_name =

# (list) List of architectures to build for
android.archs = arm64-v8a

# (bool) Automatically accept Android SDK licenses
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 0

# (str) Path to buildozer data directory
#buildozer_title = Buildozer
