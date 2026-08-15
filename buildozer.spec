[app]

# App Info
title = Hinata Bot
package.name = hinatabot
package.domain = org.hinatabot

version = 1.0.0

# Source Files
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt
source.exclude_dirs = tests,bin,venv,.venv,.buildozer,.git,.github

# Requirements (kivy==2.2.1 se '==2.2.1' hata diya hai taakay python-for-android wheel fail na ho)
requirements = python3,kivy,kivymd==1.1.1,requests,urllib3,certifi,chardet,idna,pillow

# Display Configuration
orientation = portrait
fullscreen = 0

# Android Specs
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
android.enable_androidx = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 0
