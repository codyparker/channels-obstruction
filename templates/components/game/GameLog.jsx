import React, {Component, PropTypes} from 'react'

class GameLog extends Component {

    constructor(props) {
        super(props)
        this.state = {
            log_entries: props.log_entries,
            chat_text: null
        }

        this.sayIt = this.sayIt.bind(this)

    }
    
    componentWillReceiveProps(newProps){
        this.setState({
            log_entries: newProps.log_entries
            })
    }


    renderLogEntry(entry){
        let log_sender = "System"
        if (entry.player != null){
            log_sender = entry.player.username
            
        }
        return <li key={entry.id} className="list-group-item">
                 <span className="badge pull-left player-badge ">
                        {log_sender}
                </span>
                        <span>{entry.text}</span>
                </li>  
    }

    renderLog(){
        
        if (this.state.log_entries){
          return this.state.log_entries.map(function(entry){
            return this.renderLogEntry(entry)
           }.bind(this))      
        }
        
        
    }



    sayIt(){
        // submit the chat text
        let chat_text = this.refs.log_chat.value
        // send the chat text to the server
        this.props.sendSocketMessage({action: "chat_text_entered", 
                                      text: chat_text, 
                                      game_id: this.props.game_id })
    }
    

    render () {
        return (
            <div >
                <h3>Game Log</h3>
               <ul className="list-group">
                    { this.renderLog() }
                </ul>
                <div className="input-group">
                    <input ref="log_chat" type="text" className="form-control" placeholder="Type to chat..."/>
                    <span className="input-group-btn">
                        <button onClick={this.sayIt} className="btn btn-default" type="button">Say It</button>
                    </span>
                </div>
             
            </div>
        )
    }
}

GameLog.propTypes = {
    log_entries: PropTypes.array,
    sendSocketMessage: PropTypes.func
}

export default GameLog