"use strict";

// Set frequency to update every second
var accelerometerOptions = { frequency: 1000 };
var accelerometerWatcher = null;

// DOM elements
var xLabel, yLabel, zLabel, tLabel;
var startButton, stopButton;
var startTime;

// Chart setup
var xSmoothie, ySmoothie, zSmoothie;
var xCanvas, yCanvas, zCanvas;
var xLine, yLine, zLine;

// Replace PI_HOST with the Raspberry Pi hostname or IP when configuring a local test
const SERVER_URL = "http://PI_HOST:5000/motion";

// Called when device is ready
document.addEventListener("deviceready", onDeviceReady, false);
document.addEventListener("backbutton", stopWatchingAccelerometer, false);

// Main startup function
function onDeviceReady() {
	alert("🚀 App is running index.js!");

	xCanvas = document.getElementById('xCanvasId');
	yCanvas = document.getElementById('yCanvasId');
	zCanvas = document.getElementById('zCanvasId');

	xSmoothie = new SmoothieChart();
	ySmoothie = new SmoothieChart();
	zSmoothie = new SmoothieChart();

	xSmoothie.streamTo(xCanvas, 1000);
	ySmoothie.streamTo(yCanvas, 1000);
	zSmoothie.streamTo(zCanvas, 1000);

	xLine = new TimeSeries();
	yLine = new TimeSeries();
	zLine = new TimeSeries();

	xLabel = document.getElementById('xLabelId');
	yLabel = document.getElementById('yLabelId');
	zLabel = document.getElementById('zLabelId');
	tLabel = document.getElementById('tLabelId');
	startButton = document.getElementById('startButtonId');
	stopButton = document.getElementById('stopButtonId');

	startButton.addEventListener("click", startWatchingAccelerometer, false);
	stopButton.addEventListener("click", stopWatchingAccelerometer, false);

	startButton.disabled = false;
	stopButton.disabled = true;
}

// Handles each accelerometer update
function onSuccess(acceleration) {
	accelerometerSuccess(acceleration); // Updated UI

	const motionData = {
		x: acceleration.x,
		y: acceleration.y,
		z: acceleration.z,
		timestamp: new Date().toISOString()
	};

	console.log("Motion detected:", motionData);

	// Send motion data to Flask server
	fetch(SERVER_URL, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(motionData)
	})
	.then(response => {
    	if (!response.ok) {
        alert("Server responded with error: " + response.status);
    	} else {
        alert("✅ Motion data sent!");
    	}
	})
	.catch(err => {
    	alert("❌ Failed to send motion data:\n" + err.message);
	});
}
// Start listening to accelerometer
function startWatchingAccelerometer() {
	accelerometerWatcher = navigator.accelerometer.watchAcceleration(
		onSuccess,
		accelerometerFailure,
		accelerometerOptions
	);

	startTime = Date.now();
	startButton.disabled = true;
	stopButton.disabled = false;

	xSmoothie.addTimeSeries(xLine, { strokeStyle: 'rgb(255,0,0)', lineWidth: 3 });
	ySmoothie.addTimeSeries(yLine, { strokeStyle: 'rgb(0,255,0)', lineWidth: 3 });
	zSmoothie.addTimeSeries(zLine, { strokeStyle: 'rgb(0,0,255)', lineWidth: 3 });
}

// Stop accelerometer
function stopWatchingAccelerometer() {
	if (accelerometerWatcher) {
		navigator.accelerometer.clearWatch(accelerometerWatcher);
		accelerometerWatcher = null;
		startButton.disabled = false;
		stopButton.disabled = true;
	}
}

// Update UI and chart
function accelerometerSuccess(acceleration) {
	xLabel.innerHTML = "x: " + acceleration.x.toPrecision(5);
	yLabel.innerHTML = "y: " + acceleration.y.toPrecision(5);
	zLabel.innerHTML = "z: " + acceleration.z.toPrecision(6);
	tLabel.innerHTML = "t: " + Math.round(acceleration.timestamp - startTime);

	xLine.append(acceleration.timestamp, acceleration.x);
	yLine.append(acceleration.timestamp, acceleration.y);
	zLine.append(acceleration.timestamp, acceleration.z);
}

// Handle errors
function accelerometerFailure() {
	alert("Error in Accelerometer!");
}
