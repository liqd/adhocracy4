/* This is a workaround for a certain ES5 related import mess.
 * It should not be needed any more once we switch to full ES6.
 */
import './adhocracy4/static/global_jquery'

export { default as alert } from './adhocracy4/static/Alert'
export { default as api } from './adhocracy4/static/api'
export { default as comments } from './adhocracy4/comments/static/comments/react_comments'
export * as commentsAsync from './adhocracy4/comments_async/static/comments_async'
export { default as config } from './adhocracy4/static/config'
export { default as follows } from './adhocracy4/follows/static/follows/react_follows'
export * as maps from './adhocracy4/maps/static/a4maps/a4maps_common'
export { default as polls } from './adhocracy4/polls/assets/react_polls'
export { default as ratings } from './adhocracy4/ratings/static/ratings/react_ratings'
export { default as reports } from './adhocracy4/reports/static/reports/react_reports'
export { default as selectDropdown } from './adhocracy4/static/select_dropdown'
export * as widget from './adhocracy4/static/widget'
