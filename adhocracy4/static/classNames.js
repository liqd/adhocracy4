/*
 * creates a string for className attribute from an array of classnames
 * while filtering out empty strings and undefined
 *
 * @param {...string} classes
 * @returns {string}
 */
const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ')
}

export default classNames
