import React from 'react';

class Cell extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			dStyles : { // Dynamic Style
				backgroundColor: 'white',
			},
			fStyle: { // Fixed Style
				width: this.props.size+'em',
				height: this.props.size+'em',
				border: '5px solid #ddd'
			},
			selected: this.props.selected
		};
	}

	cellOnClick = (style) => {
		console.log(style);
		this.setState({dStyles : {backgroundColor: !this.state.selected ? 'black' : 'white'}, selected: !this.state.selected});
	}

	renderCellContent() {
		return <img src={this.props.image} alt={this.props.value} style={this.state.fStyle}/>;
	}

	render() {
		const bColor = this.props.selected ? 'black' : (this.props.highlighted ? 'green' :'white');
		return <td style={{backgroundColor:bColor,...this.state.fStyle}} onClick={this.props.onClick}>{this.renderCellContent()}</td>;
	}

}

export default Cell;
