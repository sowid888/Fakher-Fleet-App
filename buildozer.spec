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

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy==2.3.0,cython

# (str) Supported orientations
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (int) Android NDK API
android.ndk_api = 21

# (bool) Use private storage
android.private_storage = True

# (list) List of architectures to build for
android.archs = arm64-v8a

# (bool) Automatically accept Android SDK licenses
android.accept_sdk_license = True

# (bool) Enable AndroidX support
android.enable_androidx = True

[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if run as root
warn_on_root = 0
