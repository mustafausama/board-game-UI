import React from 'react';
import Cell from './CellComponent';

class Board extends React.Component {
	constructor() {
		super();
		this.state = {
			rows: 5,
			cols: 5
		};
	}

	renderBoardCells() {
		const size = 5;
		const rows = [];
		for(var i = 1; i <= this.state.rows; i++) {
			const cells = [];
			for(var j = 1; j <= this.state.cols; j++) {
				cells.push(<Cell size={size} key={i+"_"+j}/>);
			}
			rows.push(<tr>{cells}</tr>);
		}
		return <table>{rows}</table>;
	}

	render() {
		return <div className="justify-content-center">{this.renderBoardCells()}</div>;
	}

}

export default Board;
