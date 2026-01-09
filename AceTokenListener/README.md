# AceTokenListener
A simple Android app that listens for Ace Token broadcasts and displays them.

## How to build and run
1. Open this folder in Android Studio.
2. Build and run the app on your Android device.
3. Send a broadcast with action `com.sarahcore.ACE_TOKEN` and extra `token` to display the token in the app.

Example ADB command:
```
adb shell am broadcast -a com.sarahcore.ACE_TOKEN --es token "Genesis_10x_AceToken"
```
