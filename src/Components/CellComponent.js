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
			selected: false
		};
	}

	cellOnClick = (style) => {
		console.log(style);
		this.setState({dStyles : {backgroundColor: !this.state.selected ? 'black' : 'white'}, selected: !this.state.selected});
	}

	renderCellContent() {
		return <span></span>;
	}

	render() {
		return <td style={{...this.state.dStyles,...this.state.fStyle}} onClick={(e) => this.cellOnClick(e)}>{this.renderCellContent()}</td>;
	}

}

export default Cell;
