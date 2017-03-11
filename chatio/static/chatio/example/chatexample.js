
function onjoin(data){
	console.log('joined', data.join)
	var roomdiv = $(
			'<div class="room well" id="room-'+data.join+'"">' +
				'<div id="messages-'+data.join+'"></div>' + 
				'<input><button id="send-'+data.join+'">send</button>' +
				'<button id="leave-'+data.join+'">leave</button>' +
			'</div>'
		);
	roomdiv.find('#send-'+data.join).click(function(){
		chat.sendmsg(roomdiv.find('input').val(), data.join);
		roomdiv.find('input').val(''); //clear input
		return false;  // don't refresh page
	});
	roomdiv.find('#leave-'+data.join).click(function(){
		chat.leave(data.join);
	});
	$('#roomgroup-' + data.join).append(roomdiv);
}

function onmsg(data){
	console.log('showing message')
	var msg = 	"<div class='message'>" +
					"<span class='username'>" + data.username + ":</span>" +
					"<span class='body'>" + data.message + "</span>" +
				"</div>";
	$('#messages-'+ data.room).append(msg);
}
	
function onleave(data){
	$('#room-' + data.leave).remove();
	$('#roomgroupbtn-' + data.leave).prop('disabled',false);
}

var chat = new Chatio('/chat', onjoin, onleave, onmsg);

$('.room-connect').click(function(){
	console.log('clicked', $(this).id);
	$(this).prop('disabled', true);
	chat.join(this.dataset.room);
});

