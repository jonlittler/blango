// JS React
alert('Hello, from Pj & Apple!')

// Create React Button
class ClickButton extends React.Component {
  state = { wasClicked: false }

  handleClick () {
    this.setState({wasClicked: true})
  }

  render () {
    let buttonText

    if (this.state.wasClicked)
      buttonText = 'Clicked!'
    else
      buttonText = 'Click Me'

    return React.createElement(
      'button', 
      {className: 'btn btn-primary mt-2', onClick: () => { this.handleClick() }},
      buttonText
    )
  }
}

// Mount to DOM
// See post-table.html <div id="react_root"></div>
const domContainer = document.getElementById('react_root')
ReactDOM.render(
  React.createElement(ClickButton),
  domContainer
)