/* Minimal runtime for .dc.html templates on a static site.
   Renders <template id="dc-template"> with {{holes}}, <sc-for>, <sc-if> and on*="{{fn}}"
   handlers, and re-renders on setState via morphdom (keeps DOM nodes, scroll, inputs). */
(function () {
  var HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;
  var WHOLE = /^\s*\{\{\s*([^}]+?)\s*\}\}\s*$/;

  function lookup(scope, path) {
    path = String(path || '').trim();
    if (path === 'true') return true;
    if (path === 'false') return false;
    if (path === 'null') return null;
    if (/^-?\d+(\.\d+)?$/.test(path)) return Number(path);
    if (/^(['"]).*\1$/.test(path)) return path.slice(1, -1);
    var parts = path.split('.'), v = scope;
    for (var i = 0; i < parts.length; i++) { if (v == null) return undefined; v = v[parts[i]]; }
    return v;
  }
  function holeOf(str) { var m = String(str || '').match(WHOLE); return m ? m[1] : str; }
  function interp(str, scope) { return str.replace(HOLE, function (_, p) { var v = lookup(scope, p); return v == null ? '' : String(v); }); }

  function kids(node, scope, parent, ctx) { for (var c = node.firstChild; c; c = c.nextSibling) renderNode(c, scope, parent, ctx); }

  function renderNode(node, scope, parent, ctx) {
    if (node.nodeType === 3) {
      var t = node.nodeValue;
      parent.appendChild(document.createTextNode(t.indexOf('{{') < 0 ? t : interp(t, scope)));
      return;
    }
    if (node.nodeType !== 1) return;
    var tag = node.localName;
    if (tag === 'sc-for') {
      var list = lookup(scope, holeOf(node.getAttribute('list') || node.getAttribute('dc-a-list'))) || [];
      var as = node.getAttribute('as') || 'item';
      for (var i = 0; i < list.length; i++) { var s = Object.create(scope); s[as] = list[i]; s.$index = i; kids(node, s, parent, ctx); }
      return;
    }
    if (tag === 'sc-if') {
      if (lookup(scope, holeOf(node.getAttribute('value') || node.getAttribute('dc-a-value')))) kids(node, scope, parent, ctx);
      return;
    }
    var el = document.importNode(node, false);
    var attrs = node.attributes;
    for (var a = 0; a < attrs.length; a++) {
      var name = attrs[a].name, v = attrs[a].value;
      if (/^hint-/.test(name)) { el.removeAttribute(name); continue; }
      if (v.indexOf('{{') < 0) continue;
      var m = v.match(WHOLE);
      if (m && /^on/.test(name)) {
        el.removeAttribute(name);
        var fn = lookup(scope, m[1]);
        if (typeof fn === 'function') { var id = 'h' + (ctx.n++); ctx.handlers[id] = fn; el.setAttribute('data-dc-on-' + name.slice(2).toLowerCase(), id); }
      } else if (name.indexOf('dc-a-') === 0) {
        el.removeAttribute(name);
        el.setAttribute(name.slice(5), interp(v, scope));
      } else {
        el.setAttribute(name, interp(v, scope));
      }
    }
    kids(node, scope, el, ctx);
    parent.appendChild(el);
  }

  var comp, app, tpl, ctx, queued = false;

  function build() {
    ctx = { n: 0, handlers: {} };
    var vals = comp.renderVals() || {};
    var frag = document.createDocumentFragment();
    kids(tpl.content, vals, frag, ctx);
    return frag;
  }

  function update() {
    queued = false;
    var next = document.createElement('div');
    next.id = app.id;
    next.appendChild(build());
    window.morphdom(app, next, {
      childrenOnly: true,
      onBeforeElUpdated: function (from, to) {
        if (from.tagName === 'INPUT' || from.tagName === 'TEXTAREA' || from.tagName === 'SELECT') {
          for (var i = 0; i < to.attributes.length; i++) {
            var at = to.attributes[i];
            if (at.name !== 'value' && at.name !== 'checked' && from.getAttribute(at.name) !== at.value) from.setAttribute(at.name, at.value);
          }
          return false;
        }
        return true;
      }
    });
    if (comp.componentDidUpdate) comp.componentDidUpdate();
  }

  window.DCLogic = class DCLogic {
    constructor(props) { this.props = props || {}; this.state = undefined; }
    setState(p) {
      var patch = typeof p === 'function' ? p(this.state || {}, this.props) : p;
      this.state = Object.assign({}, this.state || {}, patch);
      if (!queued) { queued = true; Promise.resolve().then(update); }
    }
    forceUpdate() { if (!queued) { queued = true; Promise.resolve().then(update); } }
  };

  function delegate(type) {
    app.addEventListener(type, function (e) {
      var attr = 'data-dc-on-' + type;
      var el = e.target && e.target.closest ? e.target.closest('[' + attr + ']') : null;
      if (!el || !app.contains(el)) return;
      var fn = ctx.handlers[el.getAttribute(attr)];
      if (!fn) return;
      fn({
        type: type, target: e.target, currentTarget: el, nativeEvent: e,
        preventDefault: function () { e.preventDefault(); },
        stopPropagation: function () { e.stopPropagation(); }
      });
    });
  }

  window.dcMount = function (Component, props) {
    app = document.getElementById('app');
    tpl = document.getElementById('dc-template');
    comp = new Component(props);
    app.appendChild(build());
    ['click', 'submit', 'input', 'change'].forEach(delegate);
    if (comp.componentDidMount) comp.componentDidMount();
  };
})();
