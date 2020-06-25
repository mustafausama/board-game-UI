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
	                   value : 'empty'};
	      }
	    }


		this.state = {
			rows: size,
			cols: size,
			grid: g,
			itemList: [],
			cellSelected: false
		};
	}

	resetGrid(size){
	    const g = Array(size);
	    

	    //fill in the grid 
	    for(var i=0; i<size; i++){
	      g[i] = Array(size);
	      for(var j=0; j<size; j++){
	        g[i][j] = {selected : false,
	                   value : 'empty'};
	      }
	    }

	    this.setState({grid:g});
	}


	//update grid to represent items list
	//vald coords assumed
	updateGrid(){
	    const g = this.state.grid;
	    const items = this.state.itemList;
	    
	    for(var i=0; i<items.length; i++){
	    	var id = items[i].id;
	    	var figure = items[i].type;
	    	//var color = items[i].isWhite;
	    	var col = items[i].x - 1;
	    	var row = items[i].y - 1;
	    	var imageURL = items[i].image;

	    	g[row][col].id = id;
	    	g[row][col].value = figure;
	    	g[row][col].img = imageURL;
	    }

	    this.setState({grid:g});
	}

	//make GET request, save result to state and update grid
	getItemList(){
		fetch('/api/chess/item').then(res => res.json()).then(data => this.setState({itemList:data}));
		console.log(this.state.itemList);
		this.updateGrid();
	}


	renderBoardCells() {
		const cellSize = 5;
		const rows = [];
		for(var i = 0; i < this.state.rows; i++) {
			const cells = [];
			for(var j = 0; j < this.state.cols; j++) {
				cells.push(<Cell size={cellSize} key={i+"_"+j} 
								selected={this.state.grid[i][j].selected}
								value={this.state.grid[i][j].value} 
								image={this.state.grid[i][j].img}
								onClick={() => this.clickHandle(i, j)}/>);
			}
			rows.push(<tr>{cells}</tr>);
		}

		return <table>{rows}</table>;
	}


	clickHandle(x, y){
		
	}


	//POST any changes made to the server
	postUpdate(){
		//TODO
	}

	render() {
		return (<div>
					<button value='update' onClick={() => this.getItemList()}>update</button>
					<button value='update' onClick={() => this.postUpdate()}>post</button>
			   		<div className="justify-content-center">{this.renderBoardCells()}</div>
			   </div>);
	}

}

export default Board;
