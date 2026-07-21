// ── Item quantities ─────────────────────────────────────────────
    const quantities = { 'item-1': 1, 'item-2': 1, 'item-3': 1 };
    const prices     = { 'item-1': 2299, 'item-2': 1199, 'item-3': 149 };

    function changeItemQty(id, delta){
      quantities[id] = Math.max(1, (quantities[id] || 1) + delta);
      document.getElementById('qty-' + id).textContent = quantities[id];
      updateSummary();
    }

    function removeItem(id){
      const el = document.getElementById(id);
      if(!el) return;
      el.style.opacity = '0';
      el.style.transform = 'translateX(-20px)';
      el.style.transition = 'all .3s ease';
      setTimeout(() => {
        el.remove();
        delete quantities[id];
        delete prices[id];
        updateSummary();
        checkEmpty();
      }, 280);
      showToast('Item removed from quote cart');
    }

    function setType(btn){
      const toggles = btn.parentElement.querySelectorAll('.ci-type-btn');
      toggles.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    }

    function selectDelivery(el){
      document.querySelectorAll('.delivery-opt').forEach(d => d.classList.remove('selected'));
      el.classList.add('selected');
    }

    function checkEmpty(){
      const items = document.querySelectorAll('.cart-item-card');
      const empty = document.getElementById('emptyState');
      const form  = document.getElementById('enquiryForm');
      const count = items.length;
      empty.style.display  = count === 0 ? 'flex' : 'none';
      form.style.display   = count === 0 ? 'none' : 'block';
      document.getElementById('itemCountBadge').textContent = count;
      document.getElementById('cartSubtitle').textContent   = count === 0
        ? 'Your cart is empty'
        : `${count} item${count !== 1 ? 's' : ''} selected · We'll contact you within 2 hours`;
    }

    function updateSummary(){
      let total = 0;
      Object.keys(quantities).forEach(id => {
        if(prices[id]) total += prices[id] * quantities[id];
      });
      const fmt = n => '$' + n.toLocaleString();
      document.getElementById('subtotalVal').textContent = fmt(total);
      document.getElementById('totalVal').textContent    = fmt(total);
    }

    // ── Add suggested item ──────────────────────────────────────────
    let suggestCount = 0;
    function addSuggested(el, name, brand, price){
      el.style.opacity = '.5';
      el.style.pointerEvents = 'none';
      const priceNum = parseInt(price.replace(/\D/g,''));
      suggestCount++;
      const id = 'sugg-' + suggestCount;
      prices[id]     = priceNum;
      quantities[id] = 1;
      // Add a simple card
      const wrap = document.getElementById('cartItemsWrap');
      const div  = document.createElement('div');
      div.className = 'cart-item-card';
      div.id        = id;
      div.style.opacity = '0';
      div.style.transform = 'translateY(10px)';
      div.style.transition = 'all .3s ease';
      div.innerHTML = `
        <div class="ci-img"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 17v-2m3 2v-4m3 4v-6"/></svg></div>
        <div class="ci-body">
          <div class="ci-brand">${brand}</div>
          <div class="ci-name">${name}</div>
          <div class="ci-meta"><span class="ci-tag">Accessory</span></div>
          <div class="ci-bottom">
            <div class="ci-qty">
              <button class="ci-qty-btn" onclick="changeItemQty('${id}',-1)">−</button>
              <span class="ci-qty-num" id="qty-${id}">1</span>
              <button class="ci-qty-btn" onclick="changeItemQty('${id}',1)">+</button>
            </div>
            <div class="ci-price"><div class="ci-price-num">${price}</div></div>
            <span class="ci-remove" onclick="removeItem('${id}')">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a1 1 0 011-1h4a1 1 0 011 1v2"/></svg>
              Remove
            </span>
          </div>
        </div>`;
      wrap.appendChild(div);
      requestAnimationFrame(() => {
        div.style.opacity   = '1';
        div.style.transform = 'translateY(0)';
      });
      checkEmpty();
      updateSummary();
      showToast(name + ' added to quote!');
    }

    // ── Submit ──────────────────────────────────────────────────────
    function submitQuote(){
      const first = document.getElementById('firstName').value.trim();
      const phone = document.getElementById('phone').value.trim();
      const email = document.getElementById('email').value.trim();
      if(!first || !phone || !email){
        showToast('Please fill in your name, phone, and email');
        return;
      }
      // Generate ref number
      const ref = Math.floor(1000 + Math.random() * 8999);
      document.getElementById('refNum').textContent = '2025-' + ref;
      document.getElementById('successOverlay').classList.add('show');
    }

    // ── Toast ───────────────────────────────────────────────────────
    function showToast(msg){
      const t = document.getElementById('toast');
      document.getElementById('toastMsg').textContent = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2800);
    }