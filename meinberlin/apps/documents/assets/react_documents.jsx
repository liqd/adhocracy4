var React = require('react')
var ReactDOM = require('react-dom')
var DocumentManagement = require('./DocumentManagement')

module.exports.renderDocumentManagement = function (mountpoint) {
  const element = document.getElementById(mountpoint)

  const chapters = JSON.parse(element.getAttribute('data-chapters'))
  const module = element.getAttribute('data-module')
  const config = JSON.parse(element.getAttribute('data-config'))

  ReactDOM.render(<DocumentManagement key={module} module={module} chapters={chapters} config={config} />, element)
}
