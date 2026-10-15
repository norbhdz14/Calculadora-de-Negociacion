[app]
title = BATNA Cipher
package.name = batnacipher
package.domain = mx.cipher
source.dir = .
source.include_exts = py,png,ttf,json
version = 1.0
requirements = python3==3.11.8,kivy==2.3.0
orientation = portrait
fullscreen = 0
icon.filename = assets/logo_cipher.png
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
