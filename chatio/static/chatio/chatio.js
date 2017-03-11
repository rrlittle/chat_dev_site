function Chatio(streamurl, onjoin, onleave, onmsg){
	if(onjoin == undefined){onjoin = default_onjoin;}
	if(onmsg == undefined){onjoin = default_onmsg;}
	if(onleave == undefined){onjoin = default_onleave;}

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

	this.socket.onmesssage = function(msg){
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
			&& data.created!= undefined){msgfunc(data);}
		else{
			console.log('could not process msg!');
		}
	}

	this.createroom = function(room){
		var data = {
			room: room,
			command: 'create'
		}
		this.socket.send(JSON.stringify(data));
	}
	// connect to a room
	this.connect = function(room){
		var data = {
			room: room,
			command: 'join'
		}
		this.socket.send(JSON.stringify(data));
	}
	this.sendmsg = function(msg, room){
		var data = {
			message: msg,
			command: 'send',
			room: room
		}
		socket.send(JSON.stringify(data));
	}
}

function default_onmsg(data){
	console.log('received',data);
}

function default_onleave(data){
	console.log('left', data);
}

function default_onjoin(data){
	console.log('joined', data);
}