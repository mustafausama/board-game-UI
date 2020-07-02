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
	        g[i][j] = { selected : false,
	        			available : false,
	                    value : 'empty',
	                	id: null,
	                	img: '',
	                	available_cells:[],
	                };
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

	emptyGrid(){

		const height = this.state.rows;
		const width = this.state.cols;

	    const g = Array(height);
	    

	    //fill in the grid 
	    for(var i=0; i<height; i++){
	      g[i] = Array(width);
	      for(var j=0; j<width; j++){
	        g[i][j] = { selected : false,
	        			available : false,
	                    value : 'empty',
	                	id: null,
	                	img: '',
	                	available_cells:[],
	                };
	      }
	    }

	    return g;
	}


	//update grid to represent items list
	//vald coords assumed
	updateGrid(itemList){

	    const g = this.emptyGrid();
	    const items = itemList;
	    
	    for(var i=0; i<items.length; i++){
	    	var id = items[i].id;
	    	var figure = items[i].type;
	    	//var color = items[i].isWhite;
	    	var col = items[i].coordinates.x - 1;
	    	var row = items[i].coordinates.y - 1;
	    	var imageURL = items[i].image;
	    	var available_cells = items[i].available_cells;

	    	g[row][col].id = id;
	    	g[row][col].value = figure;
	    	g[row][col].img = imageURL;
	    	g[row][col].available_cells = available_cells;
	    }

	    this.setState({grid:g, itemList:itemList});
	}

	//make GET request, save result to state and update grid
	getItemList(){
		fetch('/api/chess/item').then(res => res.json()).then(data => this.updateGrid(data));
		//console.log(this.state.itemList);
		//this.updateGrid();
	}


	renderBoardCells() {
		const cellSize = 5;
		const rows = [];
		for(let i = 0; i < this.state.rows; i++) {
			const cells = [];
			for(let j = 0; j < this.state.cols; j++) {
				cells.push(<Cell size={cellSize} key={i+"_"+j} 
								selected={this.state.grid[i][j].selected}
								highlighted={this.state.grid[i][j].available}
								value={this.state.grid[i][j].value} 
								image={this.state.grid[i][j].img}
								onClick={() => this.clickHandle(i, j)}/>);
			}
			rows.push(<tr>{cells}</tr>);
		}

		return <table>{rows}</table>;
	}


	clickHandle(r, c){
		const g = this.state.grid;


		//if some figure is selected
		if(this.state.cellSelected === false){
			g[r][c].selected = !g[r][c].selected;
			
			const possibleCells = g[r][c].available_cells;

			//if there is something to highlight, mark it to be so
			if(possibleCells !== undefined){
				for(var i=0; i<possibleCells.length; i++){
					var col = possibleCells[i].x - 1;
		    		var row = possibleCells[i].y - 1;
		    		g[row][col].available = true;
				}
			}

			//update grid and save selected figure
			this.setState({grid:g, cellSelected: {y:r, x:c}});

		}else{
			//get coords of preciously selected figure
			const x = this.state.cellSelected.x;
			const y = this.state.cellSelected.y;


			//get old cell content
			const old = g[y][x];

			//save highlighted cells
			const possibleCells = old.available_cells;


			//if move is valid, make it and patch serversde info
			if(g[r][c].available &&  !(y===r && x===c)){

				//swap cells content
				var other = g[r][c];
				g[r][c] = old;

				//clear source cell
				g[y][x] = { selected : false,
	        			available : false,
	                    value : 'empty',
	                	id: null,
	                	img: '',
	                	available_cells:[],
	                };

				//update db via PATCH request
				const body = {coordinates:{x:c+1,y:r+1}};

				console.log(JSON.stringify(body));
				console.log(body);


				//PATCH position of moved piece
				fetch('/api/chess/item/'+old.id,{
					method: 'PATCH',
					body: JSON.stringify(body),
					headers: {
		            'Content-Type': 'application/json'
		        	}
				});


				//delete other piece
				if(other.id !== null){
					fetch('/api/chess/item/'+other.id,{
						method: 'DELETE'
					});
				}


				

			}


			//unhighlight everythng
			for(var i=0; i<this.state.rows; i++){
				for(var j=0; j<this.state.cols; j++){
					g[i][j].available = false;
					g[i][j].selected = false;
				}
			}

			//clear selection and update grid
			this.setState({cellSelected: false});

			//wait a second and update grid
			setTimeout(() => this.getItemList(), 500);
		}
	}



	render() {
		return (<div>
					<button value='update' onClick={() => this.getItemList()}>update</button>
					
			   		<div className="justify-content-center">{this.renderBoardCells()}</div>
			   </div>);
	}

}

export default Board;
