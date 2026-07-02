// ── View toggle ──────────────────────────────────────────────────
    function setView(v) {
      const grid = document.getElementById('productGrid');
      const gBtn = document.getElementById('gridViewBtn');
      const lBtn = document.getElementById('listViewBtn');
      if (v === 'list') {
        grid.classList.add('list-view');
        lBtn.classList.add('active');
        gBtn.classList.remove('active');
      } else {
        grid.classList.remove('list-view');
        gBtn.classList.add('active');
        lBtn.classList.remove('active');
      }
    }

    // ── Category filter ──────────────────────────────────────────────
    function filterCat(el) {
      document.querySelectorAll('.cat-filter-item').forEach(i => i.classList.remove('active'));
      el.classList.add('active');
      const cat = el.dataset.cat;
      const cards = document.querySelectorAll('.product-card');
      let visible = 0;
      cards.forEach(c => {
        if (cat === 'all' || c.dataset.cat === cat) {
          c.style.display = '';
          visible++;
        } else {
          c.style.display = 'none';
        }
      });
      document.getElementById('productCount').textContent = `Showing ${visible} of 84 products`;
    }
    function clearCategory() {
      document.querySelectorAll('.cat-filter-item').forEach(i => i.classList.remove('active'));
      document.querySelector('.cat-filter-item[data-cat="all"]').classList.add('active');
      document.querySelectorAll('.product-card').forEach(c => c.style.display = '');
      document.getElementById('productCount').textContent = `Showing 12 of 84 products`;
    }

    // ── Wishlist ──────────────────────────────────────────────────────
    function toggleWishlist(btn) {
      btn.classList.toggle('active');
    }

    // ── Quote Cart ────────────────────────────────────────────────────
    let cartItems = [];

    function addToCart(btn, name, brand, price) {
      const existing = cartItems.find(i => i.name === name);
      if (existing) { existing.qty++; }
      else { cartItems.push({ name, brand, price, qty: 1 }); }
      renderCart();
      openCart();
      btn.textContent = '✓ Added';
      btn.style.background = '#10B981';
      setTimeout(() => { btn.textContent = 'Add to Quote'; btn.style.background = ''; }, 1500);
    }

    function renderCart() {
      const itemsEl = document.getElementById('cartItems');
      const emptyEl = document.getElementById('cartEmpty');
      const footerEl = document.getElementById('cartFooter');
      const countEl  = document.getElementById('cartCount');
      const headerCountEl = document.getElementById('cartHeaderCount');

      const total = cartItems.reduce((s, i) => s + i.qty, 0);
      countEl.textContent = total;
      headerCountEl.textContent = `${total} item${total !== 1 ? 's' : ''}`;

      if (cartItems.length === 0) {
        emptyEl.style.display = 'flex';
        footerEl.style.display = 'none';
        itemsEl.innerHTML = '';
        itemsEl.appendChild(emptyEl);
        return;
      }
      emptyEl.style.display = 'none';
      footerEl.style.display = 'flex';
      itemsEl.innerHTML = '';

      cartItems.forEach((item, idx) => {
        const div = document.createElement('div');
        div.className = 'cart-item';
        div.innerHTML = `
          <div class="cart-item-img">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 7H4a2 2 0 00-2 2v6a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"/></svg>
          </div>
          <div class="cart-item-info">
            <div class="cart-item-name">${item.name}</div>
            <div class="cart-item-brand">${item.brand}</div>
            <div class="cart-item-qty">
              <button class="qty-btn" onclick="changeQty(${idx}, -1)">−</button>
              <span class="qty-num">${item.qty}</span>
              <button class="qty-btn" onclick="changeQty(${idx}, 1)">+</button>
              <button class="cart-item-remove" onclick="removeItem(${idx})">Remove</button>
            </div>
          </div>`;
        itemsEl.appendChild(div);
      });
    }

    function changeQty(idx, delta) {
      cartItems[idx].qty += delta;
      if (cartItems[idx].qty <= 0) cartItems.splice(idx, 1);
      renderCart();
    }
    function removeItem(idx) {
      cartItems.splice(idx, 1);
      renderCart();
    }

    function openCart() {
      document.getElementById('cartOverlay').classList.add('open');
      document.body.style.overflow = 'hidden';
    }
    function closeCart() {
      document.getElementById('cartOverlay').classList.remove('open');
      document.body.style.overflow = '';
    }
    function closeCartIfOutside(e) {
      if (e.target === document.getElementById('cartOverlay')) closeCart();
    }

    // ── Back to top ──────────────────────────────────────────────────
    window.addEventListener('scroll', () => {
      document.getElementById('backTop').classList.toggle('visible', window.scrollY > 300);
    });

    // ── Price slider ─────────────────────────────────────────────────
    document.querySelector('.price-slider').addEventListener('input', function() {
      document.getElementById('priceMax').value = '$' + Number(this.value).toLocaleString();
    });