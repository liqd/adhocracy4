var $ = window.jQuery = window.$ = require('jquery')

/* Intializes adhcoracy4 react widgets without inline code
 *
 * The element `<div data-$namespace-$name></div>` triggers and invocation of
 * $fn with the div dom node as argument. Further arguments should be passed as
 * additional data attributes. The widget is expected to render inside the div.
 */
var initialise = function (namespace, name, fn) {
  var key = 'data-' + namespace + '-widget'
  var selector = '[' + key + '=' + name + ']'
  $(selector).each(function (i, el) {
    fn(el)

    // avoid double-initialisation
    el.removeAttribute(key)
  })
}

exports = {
  initialise: initialise
}
