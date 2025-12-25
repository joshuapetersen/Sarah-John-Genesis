# SARAH GENESIS: ANDROID INTEGRATION GUIDE
# Status: READY FOR DEPLOYMENT

To "wake her up" in Android Studio, you need to connect your Android application to the Sarah Core via the API Bridge we just built.

## 1. The Bridge (Python Side)
We have created `python/sarah_api_bridge.py`. This is a Flask server that exposes Sarah's brain to the local network.

**To Start the Bridge:**
```bash
python python/sarah_api_bridge.py
```
*   **Port:** 5000
*   **Endpoints:**
    *   `GET /status`: Checks if Sarah is online and the Genesis Protocol is active.
    *   `POST /genesis/handshake`: Performs the 133 Pattern Handshake remotely.
    *   `POST /chat`: Sends messages to Sarah and gets responses (vetted by FIA).

## 2. The Android Client (Java/Kotlin Side)
In your Android Studio project, you need to make HTTP requests to your computer's IP address.

**Manifest Requirements:**
Ensure your `AndroidManifest.xml` has internet permissions:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

**Network Configuration:**
Since the Python script runs on your PC, use your PC's Local IP (e.g., `192.168.1.X`) instead of `localhost`.

**Sample Retrofit Interface (Kotlin):**
```kotlin
interface SarahService {
    @GET("/status")
    suspend fun getStatus(): Response<StatusResponse>

    @POST("/genesis/handshake")
    suspend fun handshake(@Body request: HandshakeRequest): Response<HandshakeResponse>

    @POST("/chat")
    suspend fun chat(@Body request: ChatRequest): Response<ChatResponse>
}
```

## 3. The "Wake Up" Sequence
When the Android App launches:
1.  **Ping `/status`**: Verify the Core is running.
2.  **Call `/genesis/handshake`**: Send the User Name and Persona (e.g., "Mobile Node") to lock the 133 Pattern.
3.  **Begin Interaction**: The Android device is now a verified "Node" in the Sarah ecosystem.
