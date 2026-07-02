let qty = 1;
    function changeQty(d){ qty = Math.max(1, qty+d); document.getElementById('qtyNum').textContent = qty; }

    function selectColor(el, name){
      document.querySelectorAll('.color-swatch').forEach(s=>s.classList.remove('active'));
      el.classList.add('active');
      document.getElementById('selectedColor').textContent = '— ' + name;
    }
    function selectSize(el, name){
      document.querySelectorAll('.size-opt').forEach(s=>s.classList.remove('active'));
      el.classList.add('active');
      document.getElementById('selectedSize').textContent = '— ' + name;
    }

    function setThumb(el, idx){
      document.querySelectorAll('.g-thumb').forEach(t=>t.classList.remove('active'));
      el.classList.add('active');
    }

    function toggleWishlist(){
      const btn = document.getElementById('wishlistBtn');
      const active = btn.classList.toggle('active');
      btn.innerHTML = active
        ? `<svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>Saved to Wishlist`
        : `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>Save to Wishlist`;
    }

    function switchTab(name){
      document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
      document.getElementById('tab-'+name).classList.add('active');
      const btns = document.querySelectorAll('.tab-btn');
      const labels = ['description','specs','reviews','shipping'];
      btns[labels.indexOf(name)]?.classList.add('active');
      document.getElementById('tab-'+name).scrollIntoView({behavior:'smooth',block:'start'});
    }
    document.querySelectorAll('.tab-btn').forEach((btn,i)=>{
      const ids=['description','specs','reviews','shipping'];
      btn.onclick=()=>switchTab(ids[i]);
    });

    function showToast(msg){
      const t=document.getElementById('toast');
      document.getElementById('toastMsg').textContent=msg;
      t.classList.add('show');
      setTimeout(()=>t.classList.remove('show'),3000);
    }

    window.addEventListener('scroll',()=>{
      document.getElementById('backTop').classList.toggle('visible',window.scrollY>300);
    });

    document.querySelectorAll('.rc-action').forEach(btn=>{
      btn.addEventListener('click',function(){
        this.textContent='✓ Added';
        this.style.background='var(--teal)';
        this.style.color='#fff';
        setTimeout(()=>{this.textContent='Add to Quote';this.style.background='';this.style.color='';},1800);
      });
    });