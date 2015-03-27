var previous_sessions = null
var current_session = null
var socket = null

$(document).ready(function(){
	socket = io.connect();

	socket.emit('my event', {'data': 'yes'});

	socket.on('my response', function(msg) {
		if (previous_sessions == null) {
			previous_sessions = msg['sessions']
		} else {
			if ($(previous_sessions).not(msg['sessions']).length === 0 && $(msg['sessions']).not(previous_sessions).length === 0) {
				return
			}
		}
		previous_sessions = msg['sessions']
		var html_ = ""
		for (var i = 0; i < msg['sessions'].length; i++) {
			html_ += "<span>" + msg['sessions'][i] + "</span><br/>"
		}
		$("#sessions .body").html(html_);
		$("#sessions span:first-child").click();
	});

	socket.on('bitrate_stats', function(message) {
		Object.keys(message).forEach(function (key) {
			$('#' + key).text(message[key]);
		});
	});

	socket.on('timeseries', function(message) {
		Object.keys(message).forEach(function (key) {
			$.plot($("#" + key + "_graph"), [message[key]]);
		});
	});

$('#sessions').affix({
  offset: {
    top: 1,
    bottom: function () {
      return (this.bottom = $('.footer').outerHeight(true))
    }
  }
})
});

$('#sessions').on('click', 'span', function(){
	$('.selected').removeClass('selected');
	$(this).addClass('selected');
	current_session = $(this).text();
	socket.emit('session_changed', {'session': current_session});
});