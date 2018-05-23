/* eslint no-unused-vars: "off", no-new: "off" */
/* global location */

// make jquery available for non-webpack js
var $ = window.jQuery = window.$ = require('jquery')
window.Tether = require('tether/dist/js/tether.js')

require('shariff')
var Shariff = window.Shariff

// load bootstrap components
var dropdown = require('bootstrap/js/src/dropdown.js')
var modal = require('bootstrap/js/src/modal.js')
var tab = require('bootstrap/js/src/tab.js')
var collapse = require('bootstrap/js/src/collapse.js')
// var popover = require('bootstrap/js/src/popover.js')

var django = require('django')

// expose react components
var ReactComments = require('adhocracy4').comments
var ReactRatings = require('adhocracy4').ratings
var ReactReports = require('adhocracy4').reports
var ReactFollows = require('adhocracy4').follows

var ReactDocuments = require('../../apps/documents/assets/react_documents.jsx')
var ReactPolls = require('../../apps/polls/assets/react_polls.jsx')

var relativeTimestamps = require('../../apps/actions/assets/timestamps.js')
var mapAddress = require('./map-address.js')
// var remarkpopover = require('../../apps/moderatorremark/assets/idea_remarks.js')
var dynamicFields = require('../../apps/contrib/assets/dynamic_fields.js')

// This function is overwritten with custom behavior in embed.js.
var getCurrentPath = function () {
  return location.pathname
}

var initialiseWidget = function (namespace, name, fn) {
  var key = 'data-' + namespace + '-widget'
  var selector = '[' + key + '=' + name + ']'
  $(selector).each(function (i, el) {
    fn(el)

    // avoid double-initialisation
    el.removeAttribute(key)
  })
}

var init = function () {
  new Shariff($('.shariff'))

  if ($.fn.select2) {
    $('.js-select2').select2()
  }

  initialiseWidget('a4', 'comment', ReactComments.renderComment)
  initialiseWidget('a4', 'follows', ReactFollows.renderFollow)
  initialiseWidget('a4', 'ratings', ReactRatings.renderRatings)
  initialiseWidget('a4', 'reports', ReactReports.renderReports)

  initialiseWidget('mb', 'document-management', ReactDocuments.renderDocumentManagement)
  initialiseWidget('mb', 'polls', ReactPolls.renderPolls)
  initialiseWidget('mb', 'poll-management', ReactPolls.renderPollManagement)
}

$(init)
$(document).on('a4.embed.ready', init)

module.exports = {
  'getCurrentPath': getCurrentPath
}
