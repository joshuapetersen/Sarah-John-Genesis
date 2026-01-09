package com.sarahcore.acetokenlistener;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends Activity {
    private TextView tokenView;
    private BroadcastReceiver tokenReceiver;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        tokenView = new TextView(this);
        tokenView.setText("Waiting for Ace Token...");
        setContentView(tokenView);

        tokenReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                String token = intent.getStringExtra("token");
                tokenView.setText("Ace Token: " + token);
            }
        };
        IntentFilter filter = new IntentFilter("com.sarahcore.ACE_TOKEN");
        registerReceiver(tokenReceiver, filter);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(tokenReceiver);
    }
}
