/*!
* adk v1.0.0 by Ade25
* Copyright VWC
* Licensed under [object Object].
*
* Designed and built by ade25
*/
/* ========================================================================
 * Bootstrap: transition.js v3.2.0
 * http://getbootstrap.com/javascript/#transitions
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // CSS TRANSITION SUPPORT (Shoutout: http://www.modernizr.com/)
  // ============================================================

  function transitionEnd() {
    var el = document.createElement('bootstrap')

    var transEndEventNames = {
      WebkitTransition : 'webkitTransitionEnd',
      MozTransition    : 'transitionend',
      OTransition      : 'oTransitionEnd otransitionend',
      transition       : 'transitionend'
    }

    for (var name in transEndEventNames) {
      if (el.style[name] !== undefined) {
        return { end: transEndEventNames[name] }
      }
    }

    return false // explicit for ie8 (  ._.)
  }

  // http://blog.alexmaccaw.com/css-transitions
  $.fn.emulateTransitionEnd = function (duration) {
    var called = false
    var $el = this
    $(this).one('bsTransitionEnd', function () { called = true })
    var callback = function () { if (!called) $($el).trigger($.support.transition.end) }
    setTimeout(callback, duration)
    return this
  }

  $(function () {
    $.support.transition = transitionEnd()

    if (!$.support.transition) return

    $.event.special.bsTransitionEnd = {
      bindType: $.support.transition.end,
      delegateType: $.support.transition.end,
      handle: function (e) {
        if ($(e.target).is(this)) return e.handleObj.handler.apply(this, arguments)
      }
    }
  })

}(jQuery);

/* ========================================================================
 * Bootstrap: collapse.js v3.2.0
 * http://getbootstrap.com/javascript/#collapse
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // COLLAPSE PUBLIC CLASS DEFINITION
  // ================================

  var Collapse = function (element, options) {
    this.$element      = $(element)
    this.options       = $.extend({}, Collapse.DEFAULTS, options)
    this.transitioning = null

    if (this.options.parent) this.$parent = $(this.options.parent)
    if (this.options.toggle) this.toggle()
  }

  Collapse.VERSION  = '3.2.0'

  Collapse.TRANSITION_DURATION = 350

  Collapse.DEFAULTS = {
    toggle: true
  }

  Collapse.prototype.dimension = function () {
    var hasWidth = this.$element.hasClass('width')
    return hasWidth ? 'width' : 'height'
  }

  Collapse.prototype.show = function () {
    if (this.transitioning || this.$element.hasClass('in')) return

    var startEvent = $.Event('show.bs.collapse')
    this.$element.trigger(startEvent)
    if (startEvent.isDefaultPrevented()) return

    var actives = this.$parent && this.$parent.find('> .panel').children('.in, .collapsing')

    if (actives && actives.length) {
      var hasData = actives.data('bs.collapse')
      if (hasData && hasData.transitioning) return
      Plugin.call(actives, 'hide')
      hasData || actives.data('bs.collapse', null)
    }

    var dimension = this.dimension()

    this.$element
      .removeClass('collapse')
      .addClass('collapsing')[dimension](0)
      .attr('aria-expanded', true)

    this.transitioning = 1

    var complete = function () {
      this.$element
        .removeClass('collapsing')
        .addClass('collapse in')[dimension]('')
      this.transitioning = 0
      this.$element
        .trigger('shown.bs.collapse')
    }

    if (!$.support.transition) return complete.call(this)

    var scrollSize = $.camelCase(['scroll', dimension].join('-'))

    this.$element
      .one('bsTransitionEnd', $.proxy(complete, this))
      .emulateTransitionEnd(Collapse.TRANSITION_DURATION)[dimension](this.$element[0][scrollSize])
  }

  Collapse.prototype.hide = function () {
    if (this.transitioning || !this.$element.hasClass('in')) return

    var startEvent = $.Event('hide.bs.collapse')
    this.$element.trigger(startEvent)
    if (startEvent.isDefaultPrevented()) return

    var dimension = this.dimension()

    this.$element[dimension](this.$element[dimension]())[0].offsetHeight

    this.$element
      .addClass('collapsing')
      .removeClass('collapse in')
      .attr('aria-expanded', false)

    this.transitioning = 1

    var complete = function () {
      this.transitioning = 0
      this.$element
        .removeClass('collapsing')
        .addClass('collapse')
        .trigger('hidden.bs.collapse')
    }

    if (!$.support.transition) return complete.call(this)

    this.$element
      [dimension](0)
      .one('bsTransitionEnd', $.proxy(complete, this))
      .emulateTransitionEnd(Collapse.TRANSITION_DURATION)
  }

  Collapse.prototype.toggle = function () {
    this[this.$element.hasClass('in') ? 'hide' : 'show']()
  }


  // COLLAPSE PLUGIN DEFINITION
  // ==========================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.collapse')
      var options = $.extend({}, Collapse.DEFAULTS, $this.data(), typeof option == 'object' && option)

      if (!data && options.toggle && option == 'show') options.toggle = false
      if (!data) $this.data('bs.collapse', (data = new Collapse(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.collapse

  $.fn.collapse             = Plugin
  $.fn.collapse.Constructor = Collapse


  // COLLAPSE NO CONFLICT
  // ====================

  $.fn.collapse.noConflict = function () {
    $.fn.collapse = old
    return this
  }


  // COLLAPSE DATA-API
  // =================

  $(document).on('click.bs.collapse.data-api', '[data-toggle="collapse"]', function (e) {
    var href
    var $this   = $(this)
    var target  = $this.attr('data-target')
        || e.preventDefault()
        || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '') // strip for ie7
    var $target = $(target)
    var data    = $target.data('bs.collapse')
    var option  = data ? 'toggle' : $this.data()
    var parent  = $this.attr('data-parent')
    var $parent = parent && $(parent)

    if (!data || !data.transitioning) {
      if ($parent) $parent.find('[data-toggle="collapse"][data-parent="' + parent + '"]').not($this).addClass('collapsed').attr('aria-expanded', false)
      var isCollapsed = $target.hasClass('in')
      $this.toggleClass('collapsed', isCollapsed).attr('aria-expanded', !isCollapsed)
    }

    Plugin.call($target, option)
  })

}(jQuery);

/* ========================================================================
 * Bootstrap: dropdown.js v3.2.0
 * http://getbootstrap.com/javascript/#dropdowns
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // DROPDOWN CLASS DEFINITION
  // =========================

  var backdrop = '.dropdown-backdrop'
  var toggle   = '[data-toggle="dropdown"]'
  var Dropdown = function (element) {
    $(element).on('click.bs.dropdown', this.toggle)
  }

  Dropdown.VERSION = '3.2.0'

  Dropdown.prototype.toggle = function (e) {
    var $this = $(this)

    if ($this.is('.disabled, :disabled')) return

    var $parent  = getParent($this)
    var isActive = $parent.hasClass('open')

    clearMenus()

    if (!isActive) {
      if ('ontouchstart' in document.documentElement && !$parent.closest('.navbar-nav').length) {
        // if mobile we use a backdrop because click events don't delegate
        $('<div class="dropdown-backdrop"/>').insertAfter($(this)).on('click', clearMenus)
      }

      var relatedTarget = { relatedTarget: this }
      $parent.trigger(e = $.Event('show.bs.dropdown', relatedTarget))

      if (e.isDefaultPrevented()) return

      $this
        .trigger('focus')
        .attr('aria-expanded', 'true')

      $parent
        .toggleClass('open')
        .trigger('shown.bs.dropdown', relatedTarget)
    }

    return false
  }

  Dropdown.prototype.keydown = function (e) {
    if (!/(38|40|27|32)/.test(e.which)) return

    var $this = $(this)

    e.preventDefault()
    e.stopPropagation()

    if ($this.is('.disabled, :disabled')) return

    var $parent  = getParent($this)
    var isActive = $parent.hasClass('open')

    if ((!isActive && e.which != 27) || (isActive && e.which == 27)) {
      if (e.which == 27) $parent.find(toggle).trigger('focus')
      return $this.trigger('click')
    }

    var desc = ' li:not(.divider):visible a'
    var $items = $parent.find('[role="menu"]' + desc + ', [role="listbox"]' + desc)

    if (!$items.length) return

    var index = $items.index($items.filter(':focus'))

    if (e.which == 38 && index > 0)                 index--                        // up
    if (e.which == 40 && index < $items.length - 1) index++                        // down
    if (!~index)                                      index = 0

    $items.eq(index).trigger('focus')
  }

  function clearMenus(e) {
    if (e && e.which === 3) return
    $(backdrop).remove()
    $(toggle).each(function () {
      var $this         = $(this)
      var $parent       = getParent($this)
      var relatedTarget = { relatedTarget: this }

      if (!$parent.hasClass('open')) return

      $parent.trigger(e = $.Event('hide.bs.dropdown', relatedTarget))

      if (e.isDefaultPrevented()) return

      $this.attr('aria-expanded', 'false')
      $parent.removeClass('open').trigger('hidden.bs.dropdown', relatedTarget)
    })
  }

  function getParent($this) {
    var selector = $this.attr('data-target')

    if (!selector) {
      selector = $this.attr('href')
      selector = selector && /#[A-Za-z]/.test(selector) && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
    }

    var $parent = selector && $(selector)

    return $parent && $parent.length ? $parent : $this.parent()
  }


  // DROPDOWN PLUGIN DEFINITION
  // ==========================

  function Plugin(option) {
    return this.each(function () {
      var $this = $(this)
      var data  = $this.data('bs.dropdown')

      if (!data) $this.data('bs.dropdown', (data = new Dropdown(this)))
      if (typeof option == 'string') data[option].call($this)
    })
  }

  var old = $.fn.dropdown

  $.fn.dropdown             = Plugin
  $.fn.dropdown.Constructor = Dropdown


  // DROPDOWN NO CONFLICT
  // ====================

  $.fn.dropdown.noConflict = function () {
    $.fn.dropdown = old
    return this
  }


  // APPLY TO STANDARD DROPDOWN ELEMENTS
  // ===================================

  $(document)
    .on('click.bs.dropdown.data-api', clearMenus)
    .on('click.bs.dropdown.data-api', '.dropdown form', function (e) { e.stopPropagation() })
    .on('click.bs.dropdown.data-api', toggle, Dropdown.prototype.toggle)
    .on('keydown.bs.dropdown.data-api', toggle + ', [role="menu"], [role="listbox"]', Dropdown.prototype.keydown)

}(jQuery);

(function (factory, global) {

  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module.
    define(['jquery'], factory);
  } else {
    // Browser globals.
    factory(global.jQuery);
  }

}(function ($, undef) {

  var dataKey = 'plugin_hideShowPassword'
    , shorthandArgs = ['show', 'innerToggle']
    , SPACE = 32
    , ENTER = 13;

  var canSetInputAttribute = (function(){
    var body = document.body
      , input = document.createElement('input')
      , result = true;
    if (! body) {
      body = document.createElement('body');
    }
    input = body.appendChild(input);
    try {
      input.setAttribute('type', 'text');
    } catch (e) {
      result = false;
    }
    body.removeChild(input);
    return result;
  }());

  var defaults = {
    // Visibility of the password text. Can be true, false, 'toggle'
    // or 'infer'. If 'toggle', it will be the opposite of whatever
    // it currently is. If 'infer', it will be based on the input
    // type (false if 'password', otherwise true).
    show: 'infer',

    // Set to true to create an inner toggle for this input. Can
    // also be sent to an event name to delay visibility of toggle
    // until that event is triggered on the input element.
    innerToggle: false,

    // If false, the plugin will be disabled entirely. Set to
    // the outcome of a test to insure input attributes can be
    // set after input has been inserted into the DOM.
    enable: canSetInputAttribute,

    // Class to add to input element when the plugin is enabled.
    className: 'hideShowPassword-field',

    // Event to trigger when the plugin is initialized and enabled.
    initEvent: 'hideShowPasswordInit',

    // Event to trigger whenever the visibility changes.
    changeEvent: 'passwordVisibilityChange',

    // Properties to add to the input element.
    props: {
      autocapitalize: 'off',
      autocomplete: 'off',
      autocorrect: 'off',
      spellcheck: 'false'
    },

    // Options specific to the inner toggle.
    toggle: {
      // The element to create.
      element: '<button type="button">',
      // Class name of element.
      className: 'hideShowPassword-toggle',
      // Whether or not to support touch-specific enhancements.
      // Defaults to the value of Modernizr.touch if available,
      // otherwise false.
      touchSupport: (typeof Modernizr === 'undefined') ? false : Modernizr.touch,
      // Non-touch event to bind to.
      attachToEvent: 'click',
      // Event to bind to when touchSupport is true.
      attachToTouchEvent: 'touchstart mousedown',
      // Key event to bind to if attachToKeyCodes is an array
      // of at least one keycode.
      attachToKeyEvent: 'keyup',
      // Key codes to bind the toggle event to for accessibility.
      // If false, this feature is disabled entirely.
      // If true, the array of key codes will be determined based
      // on the value of the element option.
      attachToKeyCodes: true,
      // Styles to add to the toggle element. Does not include
      // positioning styles.
      styles: { position: 'absolute' },
      // Styles to add only when touchSupport is true.
      touchStyles: { pointerEvents: 'none' },
      // Where to position the inner toggle relative to the
      // input element. Can be 'right', 'left' or 'infer'. If
      // 'infer', it will be based on the text-direction of the
      // input element.
      position: 'infer',
      // Where to position the inner toggle on the y-axis
      // relative to the input element. Can be 'top', 'bottom'
      // or 'middle'.
      verticalAlign: 'middle',
      // Amount by which to "offset" the toggle from the edge
      // of the input element.
      offset: 0,
      // Attributes to add to the toggle element.
      attr: {
        role: 'button',
        'aria-label': 'Show Password',
        tabIndex: 0
      }
    },

    // Options specific to the wrapper element, created
    // when the innerToggle is initialized to help with
    // positioning of that element.
    wrapper: {
      // The element to create.
      element: '<div>',
      // Class name of element.
      className: 'hideShowPassword-wrapper',
      // If true, the width of the wrapper will be set
      // unless it is already the same width as the inner
      // element. If false, the width will never be set. Any
      // other value will be used as the width.
      enforceWidth: true,
      // Styles to add to the wrapper element. Does not
      // include inherited styles or width if enforceWidth
      // is not false.
      styles: { position: 'relative' },
      // Styles to "inherit" from the input element, allowing
      // the wrapper to avoid disrupting page styles.
      inheritStyles: [
        'display',
        'verticalAlign',
        'marginTop',
        'marginRight',
        'marginBottom',
        'marginLeft'
      ],
      // Styles for the input element when wrapped.
      innerElementStyles: {
        marginTop: 0,
        marginRight: 0,
        marginBottom: 0,
        marginLeft: 0
      }
    },

    // Options specific to the 'shown' or 'hidden'
    // states of the input element.
    states: {
      shown: {
        className: 'hideShowPassword-shown',
        changeEvent: 'passwordShown',
        props: { type: 'text' },
        toggle: {
          className: 'hideShowPassword-toggle-hide',
          content: 'Hide',
          attr: { 'aria-pressed': 'true' }
        }
      },
      hidden: {
        className: 'hideShowPassword-hidden',
        changeEvent: 'passwordHidden',
        props: { type: 'password' },
        toggle: {
          className: 'hideShowPassword-toggle-show',
          content: 'Show',
          attr: { 'aria-pressed': 'false' }
        }
      }
    }

  };

  function HideShowPassword (element, options) {
    this.element = $(element);
    this.wrapperElement = $();
    this.toggleElement = $();
    this.init(options);
  }

  HideShowPassword.prototype = {

    init: function (options) {
      if (this.update(options, defaults)) {
        this.element.addClass(this.options.className);
        if (this.options.innerToggle) {
          this.wrapElement(this.options.wrapper);
          this.initToggle(this.options.toggle);
          if (typeof this.options.innerToggle === 'string') {
            this.toggleElement.hide();
            this.element.one(this.options.innerToggle, $.proxy(function(){
              this.toggleElement.show();
            }, this));
          }
        }
        this.element.trigger(this.options.initEvent, [ this ]);
      }
    },

    update: function (options, base) {
      this.options = this.prepareOptions(options, base);
      if (this.updateElement()) {
        this.element
          .trigger(this.options.changeEvent, [ this ])
          .trigger(this.state().changeEvent, [ this ]);
      }
      return this.options.enable;
    },

    toggle: function (showVal) {
      showVal = showVal || 'toggle';
      return this.update({ show: showVal });
    },

    prepareOptions: function (options, base) {
      var keyCodes = []
        , testElement;
      base = base || this.options;
      options = $.extend(true, {}, base, options);
      if (options.enable) {
        if (options.show === 'toggle') {
          options.show = this.isType('hidden', options.states);
        } else if (options.show === 'infer') {
          options.show = this.isType('shown', options.states);
        }
        if (options.toggle.position === 'infer') {
          options.toggle.position = (this.element.css('text-direction') === 'rtl') ? 'left' : 'right';
        }
        if (! $.isArray(options.toggle.attachToKeyCodes)) {
          if (options.toggle.attachToKeyCodes === true) {
            testElement = $(options.toggle.element);
            switch(testElement.prop('tagName').toLowerCase()) {
              case 'button':
              case 'input':
                break;
              case 'a':
                if (testElement.filter('[href]').length) {
                  keyCodes.push(SPACE);
                  break;
                }
              default:
                keyCodes.push(SPACE, ENTER);
                break;
            }
          }
          options.toggle.attachToKeyCodes = keyCodes;
        }
      }
      return options;
    },

    updateElement: function () {
      if (! this.options.enable || this.isType()) return false;
      this.element
        .prop($.extend({}, this.options.props, this.state().props))
        .addClass(this.state().className)
        .removeClass(this.otherState().className);
      this.updateToggle();
      return true;
    },

    isType: function (comparison, states) {
      states = states || this.options.states;
      comparison = comparison || this.state(undef, undef, states).props.type;
      if (states[comparison]) {
        comparison = states[comparison].props.type;
      }
      return this.element.prop('type') === comparison;
    },

    state: function (key, invert, states) {
      states = states || this.options.states;
      if (key === undef) {
        key = this.options.show;
      }
      if (typeof key === 'boolean') {
        key = key ? 'shown' : 'hidden';
      }
      if (invert) {
        key = (key === 'shown') ? 'hidden' : 'shown';
      }
      return states[key];
    },

    otherState: function (key) {
      return this.state(key, true);
    },

    wrapElement: function (options) {
      var enforceWidth = options.enforceWidth
        , targetWidth;
      if (! this.wrapperElement.length) {
        targetWidth = this.element.outerWidth();
        $.each(options.inheritStyles, $.proxy(function (index, prop) {
          options.styles[prop] = this.element.css(prop);
        }, this));
        this.element.css(options.innerElementStyles).wrap(
          $(options.element).addClass(options.className).css(options.styles)
        );
        this.wrapperElement = this.element.parent();
        if (enforceWidth === true) {
          enforceWidth = (this.wrapperElement.outerWidth() === targetWidth) ? false : targetWidth;
        }
        if (enforceWidth !== false) {
          this.wrapperElement.css('width', enforceWidth);
        }
      }
      return this.wrapperElement;
    },

    initToggle: function (options) {
      if (! this.toggleElement.length) {
        // Create element
        this.toggleElement = $(options.element)
          .attr(options.attr)
          .addClass(options.className)
          .css(options.styles)
          .appendTo(this.wrapperElement);
        // Update content/attributes
        this.updateToggle();
        // Position
        this.positionToggle(options.position, options.verticalAlign, options.offset);
        // Events
        if (options.touchSupport) {
          this.toggleElement.css(options.touchStyles);
          this.element.on(options.attachToTouchEvent, $.proxy(this.toggleTouchEvent, this));
        } else {
          this.toggleElement.on(options.attachToEvent, $.proxy(this.toggleEvent, this));
        }
        if (options.attachToKeyCodes.length) {
          this.toggleElement.on(options.attachToKeyEvent, $.proxy(this.toggleKeyEvent, this));
        }
      }
      return this.toggleElement;
    },

    positionToggle: function (position, verticalAlign, offset) {
      var styles = {};
      styles[position] = offset;
      switch (verticalAlign) {
        case 'top':
        case 'bottom':
          styles[verticalAlign] = offset;
          break;
        case 'middle':
          styles['top'] = '50%';
          styles['marginTop'] = this.toggleElement.outerHeight() / -2;
          break;
      }
      return this.toggleElement.css(styles);
    },

    updateToggle: function (state, otherState) {
      var paddingProp
        , targetPadding;
      if (this.toggleElement.length) {
        paddingProp = 'padding-' + this.options.toggle.position;
        state = state || this.state().toggle;
        otherState = otherState || this.otherState().toggle;
        this.toggleElement
          .attr(state.attr)
          .addClass(state.className)
          .removeClass(otherState.className)
          .html(state.content);
        targetPadding = this.toggleElement.outerWidth() + (this.options.toggle.offset * 2);
        if (this.element.css(paddingProp) !== targetPadding) {
          this.element.css(paddingProp, targetPadding);
        }
      }
      return this.toggleElement;
    },

    toggleEvent: function (event) {
      event.preventDefault();
      this.toggle();
    },

    toggleKeyEvent: function (event) {
      $.each(this.options.toggle.attachToKeyCodes, $.proxy(function(index, keyCode) {
        if (event.which === keyCode) {
          this.toggleEvent(event);
          return false;
        }
      }, this));
    },

    toggleTouchEvent: function (event) {
      var toggleX = this.toggleElement.offset().left
        , eventX
        , lesser
        , greater;
      if (toggleX) {
        eventX = event.pageX || event.originalEvent.pageX;
        if (this.options.toggle.position === 'left') {
          toggleX+= this.toggleElement.outerWidth();
          lesser = eventX;
          greater = toggleX;
        } else {
          lesser = toggleX;
          greater = eventX;
        }
        if (greater >= lesser) {
          this.toggleEvent(event);
        }
      }
    }

  };

  $.fn.hideShowPassword = function () {
    var options = {};
    $.each(arguments, function (index, value) {
      var newOptions = {};
      if (typeof value === 'object') {
        newOptions = value;
      } else if (shorthandArgs[index]) {
        newOptions[shorthandArgs[index]] = value;
      } else {
        return false;
      }
      $.extend(true, options, newOptions);
    });
    return this.each(function(){
      var $this = $(this)
        , data = $this.data(dataKey);
      if (data) {
        data.update(options);
      } else {
        $this.data(dataKey, new HideShowPassword(this, options));
      }
    });
  };

  $.each({ 'show':true, 'hide':false, 'toggle':'toggle' }, function (verb, showVal) {
    $.fn[verb + 'Password'] = function (innerToggle, options) {
      return this.hideShowPassword(showVal, innerToggle, options);
    };
  });

}, this));

(function (factory) {
	window.lazySizes = factory();
	if (typeof define === 'function' && define.amd) {
		define(function() {
			return window.lazySizes;
		});
	}
}(function () {
	'use strict';

	if(!Date.now || !window.document.getElementsByClassName){return;}

	var lazyloadElems, autosizesElems, lazySizesConfig, globalSizesTimer,
		globalSizesIndex, globalLazyTimer, globalLazyIndex, globalInitialTimer,
		addClass, removeClass, hasClass, isWinloaded;
	var document = window.document;
	var isPreloading = 0;

	var regDummyTags = /^(?:span|div)$/i;
	var regPicture = /^picture$/i;
	var regScript = /^script$/i;
	var regImg = /^img$/i;
	var inViewTreshhold = 10;

	var setImmediate = window.setImmediate || window.setTimeout;
	var scriptUrls = {};
	var addRemoveImgEvents = function(dom, fn, add){
		var action = add ? 'addEventListener' : 'removeEventListener';
		dom[action]('load', fn, false);
		dom[action]('abort', fn, false);
		dom[action]('readystatechange', fn, false);
		dom[action]('error', fn, false);
	};
	var unveilAfterLoad = function(e){
		addRemoveImgEvents(e.target, unveilAfterLoad);
		unveilLazy(e.target, true);
	};
	var triggerEvent = function(elem, name, details){
		var event = document.createEvent('Event');

		event.initEvent(name, true, true);

		event.details = details || {};

		elem.dispatchEvent(event);
		return event;
	};

	if(document.documentElement.classList){
		addClass = function(el, cls){
			el.classList.add(cls);
		};
		removeClass = function(el, cls){
			el.classList.remove(cls);
		};
		hasClass = function(el, cls){
			return el.classList.contains(cls);
		};
	} else {
		addClass = function(ele, cls) {
			if (!hasClass(ele, cls)){
				ele.className += " "+cls;
			}
		};
		removeClass = function(ele, cls) {
			var reg;
			if (hasClass(ele,cls)) {
				reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
				ele.className = ele.className.replace(reg,' ');
			}
		};
		hasClass = function hasClass(ele,cls) {
			return ele.className.match(new RegExp('(\\s|^)'+cls+'(\\s|$)'));
		};
	}

	function updatePolyfill(el, full){
		var imageData;
		if(window.picturefill){
			picturefill({reevaluate: true, reparse: true, elements: [el]});
		} else if(window.respimage && !respimage._.observer){
			if(full){
				imageData = el[respimage._.ns];
				if(imageData){
					imageData[full.srcset ? 'srcset' : 'src'] = undefined;
				}
			}
			respimage({reparse: true, elements: [el]});
		} else if(!window.HTMLPictureElement && window.console && document.readyState == 'complete'){
			console.log('Please use a responsive image polyfill, like respimage or picturefill. https://github.com/aFarkas/respimage');
		}
	}

	var eLlen, resetPreloadingTimer, eLvW, elvH, eLtop, eLleft, eLright, eLbottom, eLnegativeTreshhold;
	var eLnow = Date.now();
	var resetPreloading = function(e){
		isPreloading--;
		clearTimeout(resetPreloadingTimer);
		if(e && e.target){
			addRemoveImgEvents(e.target, resetPreloading);
		}
		if(!e || isPreloading < 0 || !e.target) {
			isPreloading = 0;
		}
	};
	var lazyEvalLazy = (function(){
		var timer, running;
		var unblock = function(){
			running = false;
		};
		var run = function(){
			clearTimeout(timer);
			clearLazyTimer();
			evalLazyElements();
			setTimeout(unblock);
		};
		return {
			debounce: function(){
				clearTimeout(timer);
				clearTimeout(globalInitialTimer);
				running = true;
				timer = setTimeout(run, 66);
			},
			throttled: function(){
				var delay;
				if(!running){
					running = true;
					clearTimeout(timer);
					delay = Date.now() - eLnow;
					if(delay > 300){
						delay = 9;
					} else {
						delay = 99;
					}
					timer = setTimeout(run, delay);
				}
			}
		};
	})();

	var evalLazyElements = function (){
		var rect, autoLoadElem, loadedSomething;
		eLlen = lazyloadElems.length;
		eLnow = Date.now();
		if(eLlen){
			eLvW = window.innerWidth + inViewTreshhold;
			elvH = window.innerHeight + inViewTreshhold;
			eLnegativeTreshhold = inViewTreshhold * -1;

			for(; globalLazyIndex < eLlen; globalLazyIndex++){
				rect = lazyloadElems[globalLazyIndex].getBoundingClientRect();

				if ((eLbottom = rect.bottom) >= eLnegativeTreshhold &&
					(eLtop = rect.top) <= elvH &&
					(eLright = rect.right) >= eLnegativeTreshhold &&
					(eLleft = rect.left) <= eLvW &&
					(eLbottom || eLright || eLleft || eLtop)){
					unveilLazy(lazyloadElems[globalLazyIndex]);
					loadedSomething = true;
				} else  {
					if(globalLazyIndex < eLlen - 1 && Date.now() - eLnow > 9){
						globalLazyIndex++;
						autoLoadElem = false;
						globalLazyTimer = setTimeout(evalLazyElements, 4);
						break;
					}

					if(!loadedSomething && isWinloaded && !autoLoadElem &&
						lazySizesConfig.preloadAfterLoad && isPreloading < 2 &&
						((eLbottom || eLright || eLleft || eLtop) || lazyloadElems[globalLazyIndex].getAttribute(lazySizesConfig.sizesAttr) != 'auto')){
						autoLoadElem = lazyloadElems[globalLazyIndex];
					}
				}
			}

			if(autoLoadElem && !loadedSomething){
				preload(autoLoadElem);
			}
		}
	};

	function preload(elem){
		isPreloading++;
		elem = unveilLazy(elem);
		addRemoveImgEvents(elem, resetPreloading);
		addRemoveImgEvents(elem, resetPreloading, true);
		clearTimeout(resetPreloadingTimer);
		resetPreloadingTimer = setTimeout(resetPreloading, 5000);
	}

	function addScript(dummyEl){
		var elem = document.createElement('script');

		var parent = dummyEl.parentNode;

		dummyEl.removeAttribute(lazySizesConfig.srcAttr);
		parent.insertBefore(elem, dummyEl);
		setImmediate(function(){
			removeClass(dummyEl, lazySizesConfig.lazyClass);
		});

		return elem;
	}

	function clearLazyTimer(){
		globalLazyIndex = 0;
		clearTimeout(globalLazyTimer);
	}

	function unveilLazy(elem, force){
		var sources, i, len, sourceSrcset, sizes, src, srcset, parent;

		var event = triggerEvent(elem, 'lazybeforeunveil', {force: !!force});

		if(!event.defaultPrevented){
			sizes = elem.getAttribute(lazySizesConfig.sizesAttr);
			src = elem.getAttribute(lazySizesConfig.srcAttr);
			srcset = elem.getAttribute(lazySizesConfig.srcsetAttr);
			parent = elem.parentNode;

			if(src || srcset){

				if(regDummyTags.test(elem.nodeName)){
					elem = addScript(elem);
				}

				if(regScript.test(elem.nodeName || '')){
					if(scriptUrls[src]){
						return;
					} else {
						scriptUrls[src] = true;
					}
				} else if(regImg.test(elem.nodeName || '')) {

					//LQIP
					if(!force && !elem.complete && elem.getAttribute('src') && elem.src && !elem.lazyload){
						addRemoveImgEvents(elem, resetPreloading);
						addRemoveImgEvents(elem, resetPreloading, true);
						return;
					}
					if(regPicture.test(parent.nodeName || '')){
						sources = parent.getElementsByTagName('source');
						for(i = 0, len = sources.length; i < len; i++){
							sourceSrcset = sources[i].getAttribute(lazySizesConfig.srcsetAttr);
							if(sourceSrcset){
								sources[i].setAttribute('srcset', sourceSrcset);
							}
						}
					}
				}

				if(sizes){
					if(sizes == 'auto'){
						updateSizes(elem, true);
					} else {
						elem.setAttribute('sizes', sizes);
					}
					elem.removeAttribute(lazySizesConfig.sizesAttr);
					if (!srcset && window.console && elem.getAttribute('srcset')){
						console.log('using lazysizes with a `srcset` attribute is not good. Use `data-srcset` instead');
					}
				}

				if(srcset){
					elem.setAttribute('srcset', srcset);
					elem.removeAttribute(lazySizesConfig.srcsetAttr);
				} else if(src){
					elem.setAttribute('src', src);
					elem.removeAttribute(lazySizesConfig.srcAttr);
				}
			}
		}

		setImmediate(function(){
			removeClass(elem, lazySizesConfig.lazyClass);
			if(sizes == 'auto'){
				addClass(elem, lazySizesConfig.autosizesClass);
			}

			if(srcset || sizes){
				updatePolyfill(elem, {srcset: srcset, src: src});
			}
		});
		return elem;
	}

	var lazyEvalSizes = (function(){
		var timer;
		var run = function(){
			clearTimeout(timer);
			clearSizesTimer();
			evalSizesElements();
		};
		return function(){
			clearTimeout(timer);
			clearTimeout(globalSizesTimer);
			timer = setTimeout(run, 99);
		};
	})();

	var evalSizesElements = function(){
		var checkTime, now, i;
		var len = autosizesElems.length;
		if(len){

			now = Date.now();
			i = globalSizesIndex || 0;
			checkTime = i + 3;

			clearSizesTimer();

			for(; i < len; i++){
				updateSizes(autosizesElems[i]);

				if(i > checkTime && i < len - 1 && Date.now() - now > 9){
					globalSizesIndex = i + 1;

					globalSizesTimer = setTimeout(evalSizesElements, 4);
					break;
				}
			}
		}
	};

	function clearSizesTimer(){
		globalSizesIndex = 0;
		clearTimeout(globalSizesTimer);
	}

	function updateSizes(elem, noPolyfill){
		var parentWidth, elemWidth, width, cbWidth, parent, sources, i, len, event;
		parent = elem.parentNode;

		if(parent){
			parentWidth = parent.offsetWidth;
			elemWidth = elem.offsetWidth;
			width = (elemWidth > parentWidth) ?
				elemWidth :
				parentWidth;

			if(!width && !elem._lazysizesWidth){
				while(parent && parent != document.body && !width){
					width =  parent.offsetWidth;
					parent = parent.parentNode;
				}
			}

			event = triggerEvent(elem, 'lazybeforesizes', {width: width, polyfill: !noPolyfill});

			if(!event.defaultPrevented){
				width = event.details.width;

				if(width && width !== elem._lazysizesWidth && (!lazySizesConfig.onlyLargerSizes || (!elem._lazysizesWidth || elem._lazysizesWidth < width))){
					elem._lazysizesWidth = width;
					width += 'px';
					elem.setAttribute('sizes', width);

					if(regPicture.test(parent.nodeName || '')){
						sources = parent.getElementsByTagName('source');
						for(i = 0, len = sources.length; i < len; i++){
							sources[i].setAttribute('sizes', width);
						}
					}

					if(event.details.polyfill){
						updatePolyfill(elem);
					}
				}
			}
		}
	}

	// bind to all possible events ;-) This might look like a performance disaster, but it isn't.
	// The main check functions are written to run extreme fast without consuming memory.
	var onload = function(){
		inViewTreshhold = 400;
		clearTimeout(globalInitialTimer);

		document.addEventListener('load', lazyEvalLazy.throttled, true);
		isWinloaded = true;
	};
	var onready = function(){
		var element = document.body || document.documentElement;

		if(lazySizesConfig.mutation){
			if(window.MutationObserver){
				new MutationObserver( lazyEvalLazy.throttled ).observe( document.documentElement, {childList: true, subtree: true, attributes: true} );
			} else {
				element.addEventListener( "DOMNodeInserted", lazyEvalLazy.throttled, true);
				document.documentElement.addEventListener( "DOMAttrModified", lazyEvalLazy.throttled, true);
			}
		}

		//:hover
		if(lazySizesConfig.hover){
			document.addEventListener('mouseover', lazyEvalLazy.throttled, true);
		}
		//:focus/active
		document.addEventListener('focus', lazyEvalLazy.throttled, true);
		//:target
		window.addEventListener('hashchange', lazyEvalLazy.throttled, true);

		//:fullscreen
		if(('onmozfullscreenchange' in element)){
			window.addEventListener('mozfullscreenchange', lazyEvalLazy.throttled, true);
		} else if(('onwebkitfullscreenchange' in element)){
			window.addEventListener('webkitfullscreenchange', lazyEvalLazy.throttled, true);
		} else {
			window.addEventListener('fullscreenchange', lazyEvalLazy.throttled, true);
		}

		if(lazySizesConfig.cssanimation){
			document.addEventListener('animationstart', lazyEvalLazy.throttled, true);
			document.addEventListener('transitionstart', lazyEvalLazy.throttled, true);
		}
	};

	setTimeout(function(){
		var prop;
		var lazySizesDefaults = {
			mutation: true,
			hover: true,
			cssanimation: true,
			lazyClass: 'lazyload',
			autosizesClass: 'lazyautosizes',
			srcAttr: 'data-src',
			srcsetAttr: 'data-srcset',
			sizesAttr: 'data-sizes',
			preloadAfterLoad: false,
			onlyLargerSizes: true
		};

		lazySizesConfig = window.lazySizesConfig || {};

		for(prop in lazySizesDefaults){
			if(!(prop in lazySizesConfig)){
				lazySizesConfig[prop] = lazySizesDefaults[prop];
			}
		}

		lazyloadElems = document.getElementsByClassName(lazySizesConfig.lazyClass);
		autosizesElems = document.getElementsByClassName(lazySizesConfig.autosizesClass);

		addEventListener('scroll', lazyEvalLazy.throttled, false);
		(document.body || document.documentElement).addEventListener('scroll', lazyEvalLazy.throttled, true);
		document.addEventListener('touchmove', lazyEvalLazy.throttled, false);

		addEventListener('resize', lazyEvalLazy.debounce, false);
		addEventListener('resize', lazyEvalSizes, false);

		if(/^i|^loade|c/.test(document.readyState)){
			onready();
		} else {
			document.addEventListener('DOMContentLoaded', onready, false);
		}

		if(document.readyState == 'complete'){
			onload();
		} else {
			addEventListener('load', onload, false);
			document.addEventListener('readystatechange', lazyEvalLazy.throttled, false);
		}

		lazyEvalLazy.throttled();

		if('lazySizesConfig' in window){
			window.lazySizesConfig = null;
		}

	}, document.body ? 9 : 99);

	return {
		updateAllSizes: lazyEvalSizes,
		updateAllLazy: lazyEvalLazy.throttled,
		unveilLazy: function(el){
			if(hasClass(el, lazySizesConfig.lazyClass)){
				unveilLazy(el);
			}
		},
		updateSizes: updateSizes,
		updatePolyfill: updatePolyfill
	};
}));

'use strict';
(function ($) {
    $(document).ready(function () {
        if ($('body').hasClass('lt-ie7')) {
            return;
        }
        if (!Modernizr.csstransitions) {
            $(function () {
                $('.dim-in').on('load', function () {
                    $(this).animate({ opacity: '1' }, {
                        queue: false,
                        duration: 500
                    });
                });
            });
        }
    });
}(jQuery));