/* eslint no-unused-vars: "off" */

var ReactComments = require('adhocracy4').comments
var ReactRatings = require('adhocracy4').ratings

var ReactParagraphs = require('../../../apps/documents/assets/ParagraphBox.jsx')

// make jquery available for non-webpack js
window.jQuery = window.$ = require('jquery')
window.Tether = require('tether/dist/js/tether.js')

var dropdown = require('bootstrap/js/src/dropdown.js')
var modal = require('bootstrap/js/src/modal.js')
var tab = require('bootstrap/js/src/tab.js')
var popover = require('bootstrap/js/src/popover.js')

// enable bootstrap popover
$(function () {
  $('[data-toggle="popover"]').popover()
})

module.exports = {
  'renderComment': ReactComments.renderComment,
  'renderRatings': ReactRatings.renderRatings,
  'renderParagraphs': ReactParagraphs.renderParagraphs
}
