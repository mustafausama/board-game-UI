import React from 'react';
import Cell from './CellComponent';
import { Table } from 'reactstrap';

class Board extends React.Component {
	constructor() {
		super();
		this.state = {
			rows: 5,
			cols: 5
		};
	}

	renderBoardCells() {
		var c = 1;
		const rows = [];
		for(var i = 1; i <= this.state.rows; i++) {
			const cells = [];
			for(var j = 1; j <= this.state.cols; j++) {
				cells.push(<Cell key={c++}/>);
			}
			rows.push(<tr>{cells}</tr>);
		}
		return <Table bordered>{rows}</Table>;
	}

	render() {
		return this.renderBoardCells();
	}

}

export default Board;
