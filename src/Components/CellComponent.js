import React from 'react';

class Cell extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			styles : {
				backgroundColor: 'white'
			},
			selected: false
		};
	}

	cellOnClick = (style) => {
		console.log(style);
		this.setState({styles : {backgroundColor: !this.state.selected ? 'black' : 'white'}, selected: !this.state.selected});
	}

	renderCellContent() {
		return <span></span>;
	}

	render() {
		return <td style={this.state.styles} onClick={(e) => this.cellOnClick(e)}>{this.renderCellContent()}</td>;
	}

}

export default Cell;
