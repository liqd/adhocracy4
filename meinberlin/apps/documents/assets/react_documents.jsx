const React = require('react')
const ReactDOM = require('react-dom')
const DocumentManagement = require('./DocumentManagement')

module.exports.renderDocumentManagement = function (element) {
  const chapters = JSON.parse(element.getAttribute('data-chapters'))
  const module = element.getAttribute('data-module')
  const config = JSON.parse(element.getAttribute('data-config'))

  const reloadOnSuccess = JSON.parse(element.getAttribute('data-reloadOnSuccess'))

  ReactDOM.render(<DocumentManagement key={module} module={module} chapters={chapters} config={config} reloadOnSuccess={reloadOnSuccess} />, element)
}
