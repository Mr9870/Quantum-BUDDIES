import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  double? latitude;
  double? longitude;
  double? speed;
  double? distance;

  // Get user location
  Future<void> getLocation() async {
    Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high);
    
    setState(() {
      latitude = position.latitude;
      longitude = position.longitude;
      speed = position.speed; // Speed in m/s
    });

    sendLocationToServer(latitude!, longitude!, speed!);
  }

  // Send location data to Python backend
  Future<void> sendLocationToServer(double lat, double lon, double spd) async {
    var url = Uri.parse("http://YOUR_SERVER_IP:8000/track-location/");
    var response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"latitude": lat, "longitude": lon, "speed": spd}),
    );

    var data = jsonDecode(response.body);
    setState(() {
      distance = data["distance_km"];
      speed = data["speed_kmh"];
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text("Location Tracker")),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text("Latitude: $latitude"),
              Text("Longitude: $longitude"),
              Text("Speed: ${speed?.toStringAsFixed(2)} km/h"),
              Text("Distance: ${distance?.toStringAsFixed(2)} km"),
              ElevatedButton(
                onPressed: getLocation,
                child: Text("Start Tracking"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
