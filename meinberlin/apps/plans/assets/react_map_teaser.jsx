const MapTeaserBox = require('./MapTeaserBox')
const React = require('react')
const ReactDOM = require('react-dom')

module.exports.renderFilter = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  ReactDOM.render(<MapTeaserBox {...props} />, el)
}
