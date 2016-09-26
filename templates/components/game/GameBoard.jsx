import React, {Component, PropTypes} from 'react'
import GameSquare from './GameSquare'
import GameLog from './GameLog'
import $ from 'jquery'
import Websocket from 'react-websocket'

class GameBoard extends Component {
    // lifecycle methods
    constructor(props) {
        super(props)
        this.state = {
            game: null,
            squares: null,
            log: null
        }

        // bind button click
        this.sendSocketMessage = this.sendSocketMessage.bind(this)
        this.isPlayerTurn = this.isPlayerTurn.bind(this)
    }

    componentDidMount() {
        
       this.getGame()
       //this.getSquares()
              
    }

    componentWillUnmount() {
        this.serverRequest.abort();
    }

    // custom methods
    getGame(){
         const game_url = 'http://localhost:8080/game-from-id/' + this.props.game_id
         
         this.serverRequest = $.get(game_url, function (result) {
             
            this.setState({
                game: result.game,
                log: result.log,
                squares: result.squares,
            })
        }.bind(this))
    }

    getSquares(){
         const squares_url = 'http://localhost:8080/game-squares/' + this.props.game_id
         this.serverRequest = $.get(squares_url, function (result) {
            this.setState({
                squares: result
            })
        }.bind(this))
    }
    
    

    handleData(data) {
        //receives messages from the connected websocket
        let result = JSON.parse(data)
        this.setState({game: result.game, 
                       squares: result.squares, 
                       log: result.log})

    }

    sendSocketMessage(message){
        // sends message to channels back-end
       const socket = this.refs.socket
       socket.state.ws.send(JSON.stringify(message))
    }

    isPlayerTurn(){
        if (this.props.current_user.id == this.state.game.current_turn.id){
            return true
        }else{
            return false
        }
    }

    // ----  RENDER FUNCTIONS ---- //
    // --------------------------- //
    renderRow(row_num, cols) {
       
        let row = cols.map(function(square){
            
           // for each col, render a square for this row
           return <GameSquare game_creator={this.state.game.creator.id}
                              key={square.id}
                              owner={square.owner}
                              square_id={square.id}
                              possession_type={square.status}
                              loc_x={parseInt(square.col)} 
                              loc_y={parseInt(square.row)} 
                              sendSocketMessage={this.sendSocketMessage} 
                              isPlayerTurn={this.isPlayerTurn}
                              />
        }.bind(this))

        return (
            <tr key={row_num}>{row}</tr>
        )
    }

    renderBoard() {
        // renders the obstruction grid/board
        // build by row and then by col, based on the height and width values
        let board = []
        let cur_row = -1
        // for each rown
        if (this.state.game != null && this.state.squares != null){
            // build the squares
            // if this is a new row, get the cols
            board = this.state.squares.map(function(square){
                if (square.row != cur_row){
                    // new row
                    cur_row = square.row
                    // get just current row cols
                    let row_cols = this.state.squares.filter(function(c){
                        if (c.row == cur_row){
                            return c
                        }
                    })
                    // with array of cols for this row, render it out
                    //board.push(this.renderRow(cur_row, row_cols))
                   return this.renderRow(cur_row, row_cols ) 
                }
              
             }, this)
    
        }else{
            board = 'LOADING...'
        }
        return board

        
    }

    currentTurn(){
        if (this.state.game){
            if (this.state.game.completed != null){
                // game is over
                return <h3>The Winner: <span className="text-primary">{(this.state.game.current_turn.username)}</span></h3>
            }else{
                return <h3>Current Turn: 
                    <span className="text-primary">{(this.state.game.current_turn.username)}</span>
                 </h3>
            }
            
        }
    }

    render() {
        return (
            <div className="row">
                <div className="col-sm-6"> 
                    {this.currentTurn()}
                    <table>
                        <tbody>
                        { this.renderBoard() }
                        </tbody>
                    </table>
                </div>
            <div className="col-sm-6">
             <GameLog sendSocketMessage={this.sendSocketMessage} 
                         log_entries={this.state.log}
                         game_id={this.props.game_id} />
            </div>   
            <Websocket ref="socket" url={this.props.socket}
                    onMessage={this.handleData.bind(this)} reconnect={true}/>
            </div>
        )
    }
}

GameBoard.propTypes = {
    game_id: PropTypes.number,
    socket: PropTypes.string,
    current_user: PropTypes.object
    
}

export default GameBoard