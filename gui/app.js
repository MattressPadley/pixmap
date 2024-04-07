const video = document.getElementById('video');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const canvas = document.getElementById('canvas'); // Assuming you have a canvas element with id 'canvas'
const ctx = canvas.getContext('2d');

// Create a WebSocket connection
const socket = new WebSocket('ws://localhost:8765'); // Replace with your server address

socket.onopen = function(e) {
  console.log("Connection established");
};

socket.onclose = function(event) {
  console.log("Connection closed", event);
};

socket.onerror = function(error) {
  console.log("WebSocket error", error);
};

socket.addEventListener('message', function(event) {
    const reader = new FileReader();
    reader.onload = function() {
        const imageDataUrl = reader.result;
        const img = new Image();
        img.onload = function() {
            ctx.drawImage(img, 0, 0);
        };
        img.src = imageDataUrl;
    };
    reader.readAsDataURL(event.data);
});
