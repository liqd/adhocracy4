'use strict'

exports.__esModule = true

var _extends2 = require('babel-runtime/helpers/extends')

var _extends3 = _interopRequireDefault(_extends2)

var _objectWithoutProperties2 = require('babel-runtime/helpers/objectWithoutProperties')

var _objectWithoutProperties3 = _interopRequireDefault(_objectWithoutProperties2)

var _classCallCheck2 = require('babel-runtime/helpers/classCallCheck')

var _classCallCheck3 = _interopRequireDefault(_classCallCheck2)

var _possibleConstructorReturn2 = require('babel-runtime/helpers/possibleConstructorReturn')

var _possibleConstructorReturn3 = _interopRequireDefault(_possibleConstructorReturn2)

var _inherits2 = require('babel-runtime/helpers/inherits')

var _inherits3 = _interopRequireDefault(_inherits2)

var _react = require('react')

var _react2 = _interopRequireDefault(_react)

var _propTypes = require('prop-types')

var _propTypes2 = _interopRequireDefault(_propTypes)

var _classnames = require('classnames')

var _classnames2 = _interopRequireDefault(_classnames)

var _scrollfeatures = require('scrollfeatures')

var _scrollfeatures2 = _interopRequireDefault(_scrollfeatures)

var _objectAssign = require('object-assign')

var _objectAssign2 = _interopRequireDefault(_objectAssign)

var _featureDetect = require('./featureDetect')

var _featureDetect2 = _interopRequireDefault(_featureDetect)

function _interopRequireDefault (obj) { return obj && obj.__esModule ? obj : { default: obj } }

// var log = function log () {}

var initialState = {
  initialized: false,
  sticky: false,
  absolute: false,
  fixedOffset: '',
  offsetHeight: 0,
  bounds: {
    top: null,
    left: null,
    right: null,
    bottom: null,
    height: null,
    width: null
  },
  restrict: {
    top: null,
    left: null,
    right: null,
    bottom: null,
    height: null,
    width: null
  },
  wrapperStyle: null,
  elementStyle: null,
  initialStyle: null,
  style: {
    top: null,
    bottom: null,
    left: null,
    right: null,
    'margin-top': 0,
    'margin-bottom': 0,
    'margin-left': 0,
    'margin-right': 0
  },
  disabled: false
}

var getAbsolutBoundingRect = function getAbsolutBoundingRect (el, fixedHeight) {
  var rect = el.getBoundingClientRect()
  var top = rect.top + _scrollfeatures2.default.windowY
  var height = fixedHeight || rect.height
  return {
    top: top,
    bottom: top + height,
    height: height,
    width: rect.width,
    left: rect.left,
    right: rect.right
  }
}

var addBounds = function addBounds (rect1, rect2) {
  var rect = (0, _objectAssign2.default)({}, rect1)
  rect.top -= rect2.top
  rect.left -= rect2.left
  rect.right = rect.left + rect1.width
  rect.bottom = rect.top + rect1.height
  return rect
}

var getPositionStyle = function getPositionStyle (el) {
  var result = {}
  var style = window.getComputedStyle(el, null)

  for (var key in initialState.style) {
    var value = parseInt(style.getPropertyValue(key))
    value = isNaN(value) ? null : value
    result[key] = value
  }

  return result
}

var getPreviousElementSibling = function getPreviousElementSibling (el) {
  var prev = el.previousElementSibling
  if (prev && prev.tagName.toLocaleLowerCase() === 'script') {
    prev = getPreviousElementSibling(prev)
  }
  return prev
}

var ReactStickyState = (function (_Component) {
  (0, _inherits3.default)(ReactStickyState, _Component)

  function ReactStickyState (props, context) {
    (0, _classCallCheck3.default)(this, ReactStickyState)

    var _this = (0, _possibleConstructorReturn3.default)(this, _Component.call(this, props, context))

    _this._updatingBounds = false
    _this._shouldComponentUpdate = true
    _this._updatingState = false

    _this.state = (0, _objectAssign2.default)({}, initialState, { disabled: props.disabled })

    // if (props.debug === true) {
    //   log = console.log.bind(console)
    // }

    return _this
  }

  ReactStickyState.prototype.getBoundingClientRect = function getBoundingClientRect () {
    return this.refs.el.getBoundingClientRect()
  }

  ReactStickyState.prototype.getBounds = function getBounds (noCache) {
    var clientRect = this.getBoundingClientRect()
    var offsetHeight = _scrollfeatures2.default.documentHeight
    noCache = noCache === true

    if (noCache !== true && this.state.bounds.height !== null) {
      if (this.state.offsetHeight === offsetHeight && clientRect.height === this.state.bounds.height) {
        return {
          offsetHeight: offsetHeight,
          style: this.state.style,
          bounds: this.state.bounds,
          restrict: this.state.restrict
        }
      }
    }

    // var style = noCache ? this.state.style : getPositionStyle(this.el);
    var initialStyle = this.state.initialStyle
    if (!initialStyle) {
      initialStyle = getPositionStyle(this.refs.el)
    }

    var style = initialStyle
    var child = this.refs.wrapper || this.refs.el
    var rect
    var restrict
    var offsetY = 0
    // var offsetX = 0;

    if (!_featureDetect2.default.sticky) {
      rect = getAbsolutBoundingRect(child, clientRect.height)
      if (this.hasOwnScrollTarget) {
        var parentRect = getAbsolutBoundingRect(this.scrollTarget)
        offsetY = this.scroll.y
        rect = addBounds(rect, parentRect)
        restrict = parentRect
        restrict.top = 0
        restrict.height = this.scroll.scrollHeight || restrict.height
        restrict.bottom = restrict.height
      }
    } else {
      var elem = getPreviousElementSibling(child)
      offsetY = 0

      if (elem) {
        offsetY = parseInt(window.getComputedStyle(elem)['margin-bottom'])
        offsetY = offsetY || 0
        rect = getAbsolutBoundingRect(elem)
        if (this.hasOwnScrollTarget) {
          rect = addBounds(rect, getAbsolutBoundingRect(this.scrollTarget))
          offsetY += this.scroll.y
        }
        rect.top = rect.bottom + offsetY
      } else {
        elem = child.parentNode
        offsetY = parseInt(window.getComputedStyle(elem)['padding-top'])
        offsetY = offsetY || 0
        rect = getAbsolutBoundingRect(elem)
        if (this.hasOwnScrollTarget) {
          rect = addBounds(rect, getAbsolutBoundingRect(this.scrollTarget))
          offsetY += this.scroll.y
        }
        rect.top = rect.top + offsetY
      }
      if (this.hasOwnScrollTarget) {
        restrict = getAbsolutBoundingRect(this.scrollTarget)
        restrict.top = 0
        restrict.height = this.scroll.scrollHeight || restrict.height
        restrict.bottom = restrict.height
      }

      rect.height = child.clientHeight
      rect.width = child.clientWidth
      rect.bottom = rect.top + rect.height
    }

    restrict = restrict || getAbsolutBoundingRect(child.parentNode)

    return {
      offsetHeight: offsetHeight,
      style: style,
      bounds: rect,
      initialStyle: initialStyle,
      restrict: restrict
    }
  }

  ReactStickyState.prototype.updateBounds = function updateBounds (silent, noCache, cb) {
    var _this2 = this

    noCache = noCache === true
    this._shouldComponentUpdate = silent !== true

    this.setState(this.getBounds(noCache), function () {
      _this2._shouldComponentUpdate = true
      if (cb) {
        cb()
      }
    })
  }

  // updateFixedOffset() {
  //   if (this.hasOwnScrollTarget && !Can.sticky) {

  //     if (this.state.sticky) {
  //       this.setState({ fixedOffset: this.scrollTarget.getBoundingClientRect().top + 'px' });
  //       if (!this.hasWindowScrollListener) {
  //         this.hasWindowScrollListener = true;
  //         ScrollFeatures.getInstance(window).on('scroll:progress', this.updateFixedOffset);
  //       }
  //     } else {
  //       this.setState({ fixedOffset: '' });
  //       if (this.hasWindowScrollListener) {
  //         this.hasWindowScrollListener = false;
  //         ScrollFeatures.getInstance(window).off('scroll:progress', this.updateFixedOffset);
  //       }
  //     }
  //   }
  // }

  ReactStickyState.prototype.updateFixedOffset = function updateFixedOffset () {
    // var fixedOffset = this.state.fixedOffset
    if (this.state.sticky) {
      this.setState({ fixedOffset: this.scrollTarget.getBoundingClientRect().top + 'px;' })
    } else {
      this.setState({ fixedOffset: '' })
    }
    // if (fixedOffset !== this.state.fixedOffset) {
    //   this.render();
    // }
  }

  ReactStickyState.prototype.addSrollHandler = function addSrollHandler () {
    if (!this.scroll) {
      var hasScrollTarget = _scrollfeatures2.default.hasInstance(this.scrollTarget)
      this.scroll = _scrollfeatures2.default.getInstance(this.scrollTarget)
      this.onScroll = this.onScroll.bind(this)
      this.scroll.on('scroll:start', this.onScroll)
      this.scroll.on('scroll:progress', this.onScroll)
      this.scroll.on('scroll:stop', this.onScroll)

      if (this.props.scrollClass.active) {
        this.onScrollDirection = this.onScrollDirection.bind(this)
        this.scroll.on('scroll:up', this.onScrollDirection)
        this.scroll.on('scroll:down', this.onScrollDirection)
        if (!this.props.scrollClass.persist) {
          this.scroll.on('scroll:stop', this.onScrollDirection)
        }
      }
      if (hasScrollTarget && this.scroll.scrollY > 0) {
        this.scroll.trigger('scroll:progress')
      }
    }
  }

  ReactStickyState.prototype.removeSrollHandler = function removeSrollHandler () {
    if (this.scroll) {
      this.scroll.off('scroll:start', this.onScroll)
      this.scroll.off('scroll:progress', this.onScroll)
      this.scroll.off('scroll:stop', this.onScroll)
      if (this.props.scrollClass.active) {
        this.scroll.off('scroll:up', this.onScrollDirection)
        this.scroll.off('scroll:down', this.onScrollDirection)
        this.scroll.off('scroll:stop', this.onScrollDirection)
      }
      if (!this.scroll.hasListeners()) {
        this.scroll.destroy()
      }
      this.onScroll = null
      this.onScrollDirection = null
      this.scroll = null
    }
  }

  ReactStickyState.prototype.addResizeHandler = function addResizeHandler () {
    if (!this.onResize) {
      this.onResize = this.update.bind(this)
      window.addEventListener('sticky:update', this.onResize, false)
      window.addEventListener('resize', this.onResize, false)
      window.addEventListener('orientationchange', this.onResize, false)
    }
  }

  ReactStickyState.prototype.removeResizeHandler = function removeResizeHandler () {
    if (this.onResize) {
      window.removeEventListener('sticky:update', this.onResize)
      window.removeEventListener('resize', this.onResize)
      window.removeEventListener('orientationchange', this.onResize)
      this.onResize = null
    }
  }

  ReactStickyState.prototype.destroy = function destroy () {
    this._updatingBounds = false
    this._shouldComponentUpdate = false
    this._updatingState = false
    this.removeSrollHandler()
    this.removeResizeHandler()
    this.scrollTarget = null
  }

  ReactStickyState.prototype.getScrollClasses = function getScrollClasses (obj) {
    if (this.options.scrollClass.active) {
      obj = obj || {}
      var direction = this.scroll.y <= 0 || this.scroll.y + this.scroll.clientHeight >= this.scroll.scrollHeight ? 0 : this.scroll.directionY
      obj[this.options.scrollClass.up] = direction < 0
      obj[this.options.scrollClass.down] = direction > 0
    }
    return obj
  }

  ReactStickyState.prototype.getScrollClass = function getScrollClass () {
    if (this.props.scrollClass.up || this.props.scrollClass.down) {
      var direction = this.scroll.y <= 0 || this.scroll.y + this.scroll.clientHeight >= this.scroll.scrollHeight ? 0 : this.scroll.directionY
      var scrollClass = direction < 0 ? this.props.scrollClass.up : this.props.scrollClass.down
      scrollClass = direction === 0 ? null : scrollClass
      return scrollClass
    }
    return null
  }

  ReactStickyState.prototype.onScrollDirection = function onScrollDirection (e) {
    if (this.state.sticky || (e && e.type) === _scrollfeatures2.default.events.SCROLL_STOP) {
      this.setState({
        scrollClass: this.getScrollClass()
      })
    }
  }

  ReactStickyState.prototype.onScroll = function onScroll (e) {
    this.updateStickyState(false)
    if (this.hasOwnScrollTarget && !_featureDetect2.default.sticky) {
      this.updateFixedOffset()
      if (this.state.sticky && !this.hasWindowScrollListener) {
        this.hasWindowScrollListener = true
        _scrollfeatures2.default.getInstance(window).on('scroll:progress', this.updateFixedOffset)
      } else if (!this.state.sticky && this.hasWindowScrollListener) {
        this.hasWindowScrollListener = false
        _scrollfeatures2.default.getInstance(window).off('scroll:progress', this.updateFixedOffset)
      }
    }
  }

  ReactStickyState.prototype.update = function update () {
    var _this3 = this

    // this.scroll.updateScrollPosition();
    this.updateBounds(true, true, function () {
      _this3.updateStickyState(false)
    })
  }

  // update(force = false) {

  //   if (!this._updatingBounds) {
  //     this._updatingBounds = true;
  //     this.scroll.updateScrollPosition();
  //     this.updateBounds(true, true, () => {
  //       this.updateBounds(force, true, () => {
  //         this.scroll.updateScrollPosition();
  //         var updateSticky = this.updateStickyState(false, () => {
  //           if (force && !updateSticky) {
  //             this.forceUpdate();
  //           }
  //         });
  //         this._updatingBounds = false;
  //       });
  //     });
  //   }
  // }

  ReactStickyState.prototype.getStickyState = function getStickyState () {
    if (this.state.disabled) {
      return { sticky: false, absolute: false }
    }

    var scrollY = this.scroll.y
    // var scrollX = this.scroll.x;
    var top = this.state.style.top
    var bottom = this.state.style.bottom
    // var left = this.state.style.left;
    // var right = this.state.style.right;
    var sticky = this.state.sticky
    var absolute = this.state.absolute

    if (top !== null) {
      var offsetBottom = this.state.restrict.bottom - this.state.bounds.height - top
      top = this.state.bounds.top - top

      if (this.state.sticky === false && ((scrollY >= top && scrollY <= offsetBottom) || (top <= 0 && scrollY < top))) {
        sticky = true
        absolute = false
      } else if (this.state.sticky && ((top > 0 && scrollY < top) || (scrollY > offsetBottom))) {
        sticky = false
        absolute = scrollY > offsetBottom
      }
    } else if (bottom !== null) {
      scrollY += window.innerHeight
      var offsetTop = this.state.restrict.top + this.state.bounds.height - bottom
      bottom = this.state.bounds.bottom + bottom

      if (this.state.sticky === false && scrollY <= bottom && scrollY >= offsetTop) {
        sticky = true
        absolute = false
      } else if (this.state.sticky && (scrollY > bottom || scrollY < offsetTop)) {
        sticky = false
        absolute = scrollY <= offsetTop
      }
    }
    return { sticky: sticky, absolute: absolute }
  }

  ReactStickyState.prototype.updateStickyState = function updateStickyState (silent) {
    var _this4 = this

    var values = this.getStickyState()

    if (values.sticky !== this.state.sticky || values.absolute !== this.state.absolute) {
      this._shouldComponentUpdate = silent !== true
      values = (0, _objectAssign2.default)(values, this.getBounds(false))
      this._updatingState = true
      this.setState(values, function () {
        _this4._shouldComponentUpdate = true
        _this4._updatingState = false
      })
    }
  }

  // updateStickyState(bounds = true, cb) {
  //   if (this._updatingState) {
  //     return;
  //   }
  //   var values = this.getStickyState();

  //   if (values.sticky !== this.state.sticky || values.absolute !== this.state.absolute) {
  //     this._updatingState = true;
  //     if (bounds) {
  //       values = assign(values, this.getBounds(), { scrollClass: this.getScrollClass() });
  //     }
  //     this.setState(values, () => {
  //       this._updatingState = false;
  //       if (typeof cb === 'function') {
  //         cb();
  //       }
  //     });
  //     return true;
  //   } else if (typeof cb === 'function') {
  //     cb();
  //   }
  //   return false;
  // }

  ReactStickyState.prototype.initialize = function initialize () {
    var _this5 = this

    if (!this.state.initialized && !this.state.disabled) {
      this.setState({
        initialized: true
      }, function () {
        var child = _this5.refs.wrapper || _this5.refs.el
        _this5.scrollTarget = _scrollfeatures2.default.getScrollParent(child)
        _this5.hasOwnScrollTarget = _this5.scrollTarget !== window
        if (_this5.hasOwnScrollTarget) {
          _this5.updateFixedOffset = _this5.updateFixedOffset.bind(_this5)
        }

        _this5.addSrollHandler()
        _this5.addResizeHandler()
        _this5.update()
      })
    }
  }

  ReactStickyState.prototype.shouldComponentUpdate = function shouldComponentUpdate (newProps, newState) {
    return this._shouldComponentUpdate
  }

  ReactStickyState.prototype.componentWillReceiveProps = function componentWillReceiveProps (nextProps) {
    var _this6 = this

    var intialize = !this.state.initialized && nextProps.initialize

    if (nextProps.disabled !== this.state.disabled) {
      this.setState({
        disabled: nextProps.disabled
      }, function () {
        if (intialize) {
          _this6.initialize()
        }
      })
    }
  }

  ReactStickyState.prototype.componentDidMount = function componentDidMount () {
    if (!this.state.initialized && this.props.initialize) {
      this.initialize()
    }
  }

  ReactStickyState.prototype.componentWillUnmount = function componentWillUnmount () {
    this.destroy()
  }

  ReactStickyState.prototype.render = function render () {
    var _classNames, _classNames2, _classNames3, _classNames4

    if (!this.state.initialized) {
      return this.props.children
    }

    var element = _react2.default.Children.only(this.props.children)

    var _props = this.props

    var wrapperClass = _props.wrapperClass

    var stickyClass = _props.stickyClass

    var fixedClass = _props.fixedClass

    var stateClass = _props.stateClass

    var disabledClass = _props.disabledClass

    var absoluteClass = _props.absoluteClass

    // var disabled = _props.disabled

    // var debug = _props.debug

    // var tagName = _props.tagName

    var props = (0, _objectWithoutProperties3.default)(_props, ['wrapperClass', 'stickyClass', 'fixedClass', 'stateClass', 'disabledClass', 'absoluteClass', 'disabled', 'debug', 'tagName'])

    var style
    var refName = 'el'
    var className = (0, _classnames2.default)((_classNames = {}, _classNames[stickyClass] = !this.state.disabled, _classNames[disabledClass] = this.state.disabled, _classNames), (_classNames2 = {}, _classNames2[fixedClass] = !_featureDetect2.default.sticky, _classNames2), (_classNames3 = {}, _classNames3[stateClass] = this.state.sticky && !this.state.disabled, _classNames3), (_classNames4 = {}, _classNames4[absoluteClass] = this.state.absolute, _classNames4), this.state.scrollClass)

    if (!_featureDetect2.default.sticky) {
      if (this.state.absolute) {
        style = {
          marginTop: this.state.style.top !== null ? this.state.restrict.height - (this.state.bounds.height + this.state.style.top) + (this.state.restrict.top - this.state.bounds.top) + 'px' : '',
          marginBottom: this.state.style.bottom !== null ? this.state.restrict.height - (this.state.bounds.height + this.state.style.bottom) + (this.state.restrict.bottom - this.state.bounds.bottom) + 'px' : ''
        }
      } else if (this.hasOwnScrollTarget && this.state.fixedOffset !== '') {
        style = {
          marginTop: this.state.fixedOffset
        }
      }
    }

    if (element) {
      element = _react2.default.cloneElement(element, { ref: refName, style: style, className: (0, _classnames2.default)(element.props.className, className) })
    } else {
      var Comp = this.props.tagName
      element = _react2.default.createElement(
        Comp,
        (0, _extends3.default)({ ref: refName, style: style, className: className }, props),
        this.props.children
      )
    }

    if (_featureDetect2.default.sticky) {
      return element
    }

    var height = this.state.disabled || this.state.bounds.height === null /* || (!this.state.sticky && !this.state.absolute) */ ? 'auto' : this.state.bounds.height + 'px'
    var marginTop = height === 'auto' ? '' : this.state.style['margin-top'] ? this.state.style['margin-top'] + 'px' : ''
    var marginBottom = height === 'auto' ? '' : this.state.style['margin-bottom'] ? this.state.style['margin-bottom'] + 'px' : ''

    style = {
      height: height,
      marginTop: marginTop,
      marginBottom: marginBottom
    }
    if (this.state.absolute) {
      style.position = 'relative'
    }
    return _react2.default.createElement(
      'div',
      { ref: 'wrapper', className: wrapperClass, style: style },
      element
    )
  }

  return ReactStickyState
}(_react.Component))

ReactStickyState.propTypes = {
  initialize: _propTypes2.default.bool,
  wrapperClass: _propTypes2.default.string,
  stickyClass: _propTypes2.default.string,
  fixedClass: _propTypes2.default.string,
  stateClass: _propTypes2.default.string,
  disabledClass: _propTypes2.default.string,
  absoluteClass: _propTypes2.default.string,
  disabled: _propTypes2.default.bool,
  debug: _propTypes2.default.bool,
  wrapFixedSticky: _propTypes2.default.bool,
  tagName: _propTypes2.default.string,
  scrollClass: _propTypes2.default.shape({
    down: _propTypes2.default.string,
    up: _propTypes2.default.string,
    none: _propTypes2.default.string,
    persist: _propTypes2.default.bool,
    active: _propTypes2.default.bool
  })
}
ReactStickyState.defaultProps = {
  initialize: true,
  wrapperClass: 'sticky-wrap',
  stickyClass: 'sticky',
  fixedClass: 'sticky-fixed',
  stateClass: 'is-sticky',
  disabledClass: 'sticky-disabled',
  absoluteClass: 'is-absolute',
  wrapFixedSticky: true,
  debug: false,
  disabled: false,
  tagName: 'div',
  scrollClass: {
    down: null,
    up: null,
    none: null,
    persist: false,
    active: false
  }
}
exports.default = ReactStickyState
module.exports = exports['default']
