import React, { Component } from 'react';
//import socketIOClient from 'socket.io-client';

import Board from './Components/BoardComponent';
import Registrtion from './Components/RegistrationComponent';

class App extends Component {

	constructor(props) {
		super(props);

		this.state = {
			socketConnected: false,
			serverConnected: false,
			turn: false,
			name: "Guest",
			room: "default"
		}

		/*const ENDPOINT = "http://127.0.0.1:4001";
		
		const socket = socketIOClient(ENDPOINT);

		socket.on("connect", ()=>this.setState({serverConnected: true}));
		socket.on("toggle-turn", ()=>this.setState({turn: !this.state.turn}));*/

	}

	registerationSubmit = (na, ro) => {
		this.setState({name: na, room:ro})
		/* temp until we implement websocket */
		this.setState({
			serverConnected: true
		});
		/* End temp */
		/*socket.emit('register', {name: na}, (res) => {
			if(res) this.setState({ serverConnected: true });
		});*/
	}

	render() {
		return (
			<div className="container">
				<div className="row">
					<Registrtion name={this.state.name} room={this.state.room} registerationSubmit={this.registerationSubmit} connected={this.state.serverConnected} />
				</div>
				<div className="row">
					<div className="col-12 col-md-8">
						<Board turn={this.state.turn} />
					</div>
					<div className="col-12 col-md-4">
						<h4>Status</h4>
						<p>Server: {(this.state.socketConnected) ? "Connected":"Disconnected"}</p>
					</div>
				</div>
			</div>
		);
	}
}

export default App;
