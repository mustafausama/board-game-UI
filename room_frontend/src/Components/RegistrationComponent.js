import React from 'react';
import { Jumbotron, Button, InputGroup, Input, InputGroupAddon } from 'reactstrap';

class Registration extends React.Component {
    constructor() {
        super();
        this.state = {
            name: "",
            room: ""
        };
    }

    renderForm() {
        if(this.props.connected) return null;
        return (
        <div>
            <hr className="my-2" />
            <p className="lead">How can we call you?</p>
            <InputGroup>
                <Input name="username" type="text" placeholder="Username" onChange={(d) => {
                    this.setState({name: d.target.value})
                }}/>
                <Input name="default" type="text" placeholder="Room" onChange={(d) => {
                    this.setState({room: d.target.value})
                }}/>
                <InputGroupAddon addonType="append">
                    <Button type="button" color="primary" onClick={this.props.registerationSubmit.bind(this, this.state.name, this.state.room)}>Connect</Button>
                </InputGroupAddon>
            </InputGroup>
        </div>
        );
  }

  render() {
    return (!this.state.connected) ? (
        <Jumbotron className="col-12">
            <h1 className="display-3">Hello, {this.props.name}! Selected room: {this.props.room}</h1>
            {this.renderForm()}
        </Jumbotron>
    ) : null;
  }
}

export default Registration;
