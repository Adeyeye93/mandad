(function () {
  var KEY = 'mandad_cart';

  function get() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; }
    catch (e) { return []; }
  }

  function save(cart) {
    localStorage.setItem(KEY, JSON.stringify(cart));
    _badge();
    window.dispatchEvent(new CustomEvent('mandad:cart', { detail: cart }));
  }

  function add(id, name, price, qty, type, img) {
    id = +id; qty = +qty || 1;
    var cart = get();
    var found = cart.find(function (i) { return i.id === id && i.type === type; });
    if (found) { found.qty += qty; }
    else { cart.push({ id: id, name: name, price: String(price || ''), qty: qty, type: type || 'purchase', img: img || '' }); }
    save(cart);
    return cart;
  }

  function remove(id) {
    save(get().filter(function (i) { return i.id !== +id; }));
  }

  function update(id, qty) {
    var cart = get();
    var item = cart.find(function (i) { return i.id === +id; });
    if (item) { item.qty = Math.max(1, +qty); save(cart); }
  }

  function clear() { localStorage.removeItem(KEY); _badge(); }

  function count() {
    return get().reduce(function (s, i) { return s + (i.qty || 1); }, 0);
  }

  function _badge() {
    var n = count();
    document.querySelectorAll('.cart-count').forEach(function (el) {
      el.textContent = n > 0 ? n : '';
    });
  }

  document.addEventListener('DOMContentLoaded', _badge);
  window.MandadCart = { get: get, add: add, remove: remove, update: update, save: save, clear: clear, count: count };
})();
