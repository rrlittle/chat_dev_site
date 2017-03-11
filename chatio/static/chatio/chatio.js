function Chatio(streamurl){
	this.ws_protocol = window.location.protocol == 'https:'? 'wss':'ws';
	this.ws_path = ws_protocol + '://' + window.location.host + streamurl;
	console.log('Connecting to ', ws_path);
	this.socket = new ReconnectingWebSocket(ws_path)
}