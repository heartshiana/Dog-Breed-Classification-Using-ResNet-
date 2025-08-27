import 'package:flutter/material.dart';

void main() {
  runApp(PAWtectorApp());
}

class PAWtectorApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PAWtector',
      home: Scaffold(
        appBar: AppBar(title: Text('PAWtector')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ElevatedButton(
                child: Text("How to Use"),
                onPressed: () {
                  // TODO: open how_to_use page
                },
              ),
              SizedBox(height: 20),
              ElevatedButton(
                child: Text("What's the Dog?"),
                onPressed: () {
                  // TODO: open whats_the_dog page
                },
              ),
              SizedBox(height: 20),
              ElevatedButton(
                child: Text("Breed of Dogs"),
                onPressed: () {
                  // TODO: open breed_of_dogs page
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
