package com.example.seniorproject.putting_wifi_on_the_map;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.location.LocationManager;
import android.location.LocationListener;
import android.location.Location;
import android.content.Context;
import android.webkit.WebSettings;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.TextView;
import android.webkit.WebView;
import android.webkit.CookieManager;
import android.webkit.CookieSyncManager;
import com.parse.*;

public class MainActivity extends Activity {

    Location currentLocation;
    double longitude = 0.0;
    double latitude = 0.0;
    int strength = 0;
    TextView lat;
    TextView longit;
    TextView wifi;
    WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Parse.initialize(this, "W0daAi5gvdhSxp5DDXhILsSyrfhzAaE3nhyePONM", "k45wkLKRTCdvuOKGTLL8H7DSChTPFBM51cpwdfA0");
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void updateButton()
    {
        lat = (TextView) findViewById(R.id.textLat);
        longit = (TextView) findViewById(R.id.textLong);
        wifi = (TextView) findViewById(R.id.wifi);
        getLinkSpeed();
        updateGPS();
        saveInParse(latitude, longitude, strength);
    }

    private class MyListener implements LocationListener {
        @Override
        public void onLocationChanged(Location location) {

            currentLocation = location;
            longitude = location.getLongitude();
            latitude = location.getLatitude();
        }

        @Override
        public void onProviderDisabled(String provider) {
        }

        @Override
        public void onProviderEnabled(String provider) {
        }

        public void onStatusChanged(String provider, int status, Bundle extras) {
        }
    }

    public void updateGPS()
    {
        LocationManager LocManage = (LocationManager)getSystemService(Context.LOCATION_SERVICE);
        LocationListener ll = new MyListener();
        LocManage.requestLocationUpdates(LocationManager.GPS_PROVIDER,0,0,ll);

        currentLocation = LocManage.getLastKnownLocation(LocationManager.GPS_PROVIDER);

        if(currentLocation != null)
        {
            longitude = currentLocation.getLongitude();
            latitude = currentLocation.getLatitude();

            lat.setText("Latitude: " + latitude);
            longit.setText("Longitude: " + longitude);
        }
    }

    public void getLinkSpeed()
    {
        WifiManager mainWifi = (WifiManager) getSystemService(Context.WIFI_SERVICE);
        WifiInfo currentWifi = mainWifi.getConnectionInfo();

        strength = currentWifi.getRssi();

        wifi.setText("Wi-Fi Strength: " + strength);
    }

    public void saveInParse(double latitude, double longitude, int strength)
    {
        ParseObject locations = new ParseObject("Location");
        locations.put("latitude", latitude);
        locations.put("longitude", longitude);
        locations.put("strength", strength);
        locations.saveInBackground();
    }

    public void buttonOnClick(View v) {
      if(v.getId() == R.id.update) {
          updateButton();
      }
      else
          getNextView(v);
    }

    public View getNextView(View v){
        switch(v.getId())
        {
            case(R.id.full_wifi_button):
                setContentView(R.layout.map_view);
                webView = (WebView)findViewById(R.id.webView);
                webView.getSettings().setJavaScriptEnabled(true);
                CookieManager.getInstance().setAcceptCookie(true);
                CookieManager.getInstance().getCookie("http://www.tcnj.edu/~gilberk1/GoogleMap.html");
                WebSettings settings = webView.getSettings();
                settings.setDomStorageEnabled(true);
                webView.setWebViewClient(new WebViewClient());
                webView.loadUrl("http://www.tcnj.edu/~gilberk1/GoogleMap.html");
                break;
            case(R.id.back_button):
                setContentView(R.layout.activity_main);
                break;
            case(R.id.help_button):
                setContentView(R.layout.info_view);
                break;
            case(R.id.signal_strength_button):
                setContentView(R.layout.signal_strength);
                break;
        }
        return v;
    }
}
