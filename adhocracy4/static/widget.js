/* Intializes adhcoracy4 react widgets without inline code
 * params:
 *  namespace: a string representing the namespace of the widget.
 *  name: a string representing the name of the widget.
 *  fn: a callback function that takes an element as its argument.
 * The element `<div data-$namespace-$name></div>` triggers and invocation of
 * $fn with the div dom node as argument. Further arguments should be passed as
 * additional data attributes. The widget is expected to render inside the div.
 */
export function initialise (namespace, name, fn) {
  const key = 'data-' + namespace + '-widget'
  const selector = '[' + key + '=' + name + ']'
  const elements = document.querySelectorAll(selector)

  for (let i = 0; i < elements.length; i++) {
    const el = elements[i]
    fn(el)

    // avoid double-initialisation
    el.removeAttribute(key)
  }
}
