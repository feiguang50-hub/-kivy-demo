[app]

# (str) Title of your application
title = Hello App

# (str) Package name
package.name = helloapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using Unix-style wildcards
# source.include_patterns = assets/*,images/*.png

# (list) List of exclusions using Unix-style wildcards
# source.exclude_patterns = venv, __pycache__, *.pyc

# (list) List of directory to exclude from the APK
source.exclude_dirs = tests, venv

# (list) List of requirements
requirements = python3,kivy

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Android API to use
android.api = 31

# (int) Minimum API required
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use AndroidX
android.use_androidx = 1

# (str) Android logcat filter to show
android.logcat_filters = *

# (str) Android additional libraries to deploy
# android.add_libs =

# (bool) Enable OpenSSL
# android.openssl = 0
