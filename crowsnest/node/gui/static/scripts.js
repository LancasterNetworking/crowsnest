$(document).ready(function(){
    var socket = io.connect();
	socket.emit('my event', {'data': 'yes'});
    socket.on('my response', function(msg) {
    	console.log('event')
    });
});