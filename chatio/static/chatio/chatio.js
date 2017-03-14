function default_onmsg(data){
	console.log('received',data);
}

function default_onleave(data){
	console.log('left', data);
}

function default_onjoin(data){
	console.log('joined', data);
}



function Chatio(streamurl, onjoin, onleave, onmsg){
	if(onjoin == undefined){onjoin = default_onjoin;}
	if(onmsg == undefined){onmsg = default_onmsg;}
	if(onleave == undefined){onleave = default_onleave;}

	this.ws_protocol = window.location.protocol == 'https:'? 'wss':'ws';
	this.ws_path = this.ws_protocol + '://' + window.location.host + streamurl;
	console.log('Connecting to ', this.ws_path);
	this.socket = new ReconnectingWebSocket(this.ws_path);

	this.socket.onopen = function(){
		console.log('socket connected');
	}

	this.socket.onclose = function(){
		console.log('socket isconnected');
	}

	this.socket.onmessage = function (msg){
		var data = JSON.parse(msg.data);
		console.log('got a msg', data);
	
		if(data.err){
			alert(data.err);
			return;
		}
		if(data.join){ onjoin(data); }
		else if(data.leave){ onleave(data); }
		else if(data.message != undefined 
			&& data.username != undefined 
			&& data.created!= undefined){onmsg(data);}
		else{
			console.log('could not process msg!');
		}
	}

	// crates a room
	this.createroom = function(room){
		var data = {
			room: room,
			command: 'create'
		}
		this.socket.send(JSON.stringify(data));
	}
	// connect to a room
	this.join = function(room){
		var data = {
			room: room,
			command: 'join'
		}
		this.socket.send(JSON.stringify(data));
	}
	// sends message to server
	this.sendmsg = function(msg, room){
		var data = {
			message: msg,
			command: 'send',
			room: room
		}
		this.socket.send(JSON.stringify(data));
	}
	// disconnect from a room
	this.leave = function(room){
		var data = {
			room: room,
			command: 'leave'
		}
		this.socket.send(JSON.stringify(data));
	}

	///
	this.addchatdom = function(div){
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
		div.append(roomdiv);
	}
}
