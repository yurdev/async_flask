$(document).ready(function() {
    // Connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    // Receive new number from server
    socket.on('new_number', function(msg) {
        console.log("Received number: " + msg.number);
        // Maintain a list of ten numbers
        if (numbers_received.length >= 10) {
            numbers_received.shift()
        }            
        numbers_received.push(msg.number);
        numbers_string = '';
        for (var i = 0; i < numbers_received.length; i++) {
            numbers_string += '<p>' + numbers_received[i] + '</p>';
        }
        $('#log').html(numbers_string);
    });
});