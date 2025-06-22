[app]
title = ProductManager
package.name = productmanager
package.domain = org.example

source.dir = .
source.include_exts = py,kv,json
version = 0.1
orientation = portrait
fullscreen = 0

requirements = kivy

android.permissions = INTERNET
android.archs = armeabi-v7a
android.minapi = 21
android.sdk = 31
android.ndk = 25b
log_level = 2

[buildozer]
warn_on_root = 1
log_level = 2
