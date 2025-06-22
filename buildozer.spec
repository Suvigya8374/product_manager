[app]
title = Product Manager
package.name = productmanager
package.domain = org.example
source.dir = .
source.include_exts = py,kv,json,png,jpg,ttf
version = 1.0
requirements = python3,kivy,openssl,requests,pyjnius,hostpython3,certifi,urllib3,chardet,idna,charset-normalizer,python-for-android,cython,mysql-connector-python
orientation = portrait
fullscreen = 0
android.archs = armeabi-v7a, arm64-v8a
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True
presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png
# Ensure MySQL SSL works on Android
android.add_libs_armeabi_v7a = libs/armeabi-v7a/*.so
android.add_libs_arm64_v8a = libs/arm64-v8a/*.so
android.allow_backup = 1

# Include database config JSON
android.add_assets = dbconfig.json

# Enable logcat debugging
log_level = 2

# Set Git path to avoid CI failures
git = /usr/bin/git

# Enable copy libs to speed up deployment
copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1
