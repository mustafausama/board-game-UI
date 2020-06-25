import React from 'react';
import Cell from './CellComponent';

class Board extends React.Component {
	constructor() {
		super();

		//initiate empty grid
		const size = 8;
	    const g = Array(size);
	    

	    //fill in the grid 
	    for(var i=0; i<size; i++){
	      g[i] = Array(size);
	      for(var j=0; j<size; j++){
	        g[i][j] = {selected : false,
	                   value : (i<2 || i>5) ? 1:0};
	      }
	    }


		this.state = {
			rows: size,
			cols: size,
			grid: g
		};
	}

	resetGrid(size){
	    const g = Array(size);
	    

	    //fill in the grid 
	    for(var i=0; i<size; i++){
	      g[i] = Array(size);
	      for(var j=0; j<size; j++){
	        g[i][j] = {selected : false,
	                   value : (i<2 || i>5) ? 1:0};
	      }
	    }

	    this.setState({grid:g});
	}


	renderBoardCells() {
		const size = 5;
		const rows = [];
		for(var i = 0; i < this.state.rows; i++) {
			const cells = [];
			for(var j = 0; j < this.state.cols; j++) {
				cells.push(<Cell size={size} key={i+"_"+j} value={this.state.grid[i][j].value}/>);
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
