// list of predefined selectors to find elements which are to be updated.
const elementsToUpdate = [
  '.l-menu__menu',
  '.l-menu__aside',
  '.js-selector-update-dashboard'
]

export const updateDashboard = async () => {
  // fetching the entire dom and store as html
  const response = await fetch(window.location.pathname)
  const htmlString = await response.text()
  try {
    // convert text to html = a new DOM
    const parser = new DOMParser()
    const newDom = parser.parseFromString(htmlString, 'text/html')

    // find new and old elements
    const selectors = elementsToUpdate.join(', ')
    const newElements = newDom.querySelectorAll(selectors)
    const oldElements = document.querySelectorAll(selectors)

    // replace old by new elements
    oldElements.forEach(function (oldElement, index) {
      oldElement.replaceWith(newElements[index])
    })
  } catch (error) {
    console.log('error', error)
  }
}
