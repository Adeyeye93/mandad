// ── Scroll reveal ──────────────────────────────────────────────
    const observer = new IntersectionObserver(
      entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
      { threshold: 0.1 }
    );
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    // ── Back to top ────────────────────────────────────────────────
    window.addEventListener('scroll', () => {
      document.getElementById('backTop').classList.toggle('visible', window.scrollY > 300);
    });

    // ── Category filter ────────────────────────────────────────────
    function filterRentals(btn) {
      document.querySelectorAll('.cat-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.dataset.cat;
      const cards = document.querySelectorAll('.rental-card');
      let count = 0;
      cards.forEach(c => {
        const show = cat === 'all' || c.dataset.cat === cat;
        c.style.display = show ? '' : 'none';
        if (show) count++;
      });
      document.getElementById('rentalCount').textContent = `${count} item${count !== 1 ? 's' : ''} available`;
    }

    // ── Pricing tier select ────────────────────────────────────────
    function selectTier(el, groupId, price, unit) {
      document.querySelectorAll(`#${groupId} .rc-price-tier`).forEach(t => t.classList.remove('selected'));
      el.classList.add('selected');
    }

    // ── Delivery option ────────────────────────────────────────────
    function selectDelivery(el) {
      document.querySelectorAll('.delivery-opt').forEach(d => d.classList.remove('selected'));
      el.classList.add('selected');
    }

    // ── Duration option ────────────────────────────────────────────
    function selectDuration(el) {
      document.querySelectorAll('.duration-opt').forEach(d => d.classList.remove('selected'));
      el.classList.add('selected');
    }

    // ── Modal ──────────────────────────────────────────────────────
    function openModal(item) {
      const overlay = document.getElementById('modalOverlay');
      if (item) {
        document.getElementById('modalTitle').textContent = `Rent: ${item.name}`;
        document.getElementById('modalProductName').textContent = item.name;
        document.getElementById('modalProductBrand').textContent = item.brand;
        document.getElementById('modalProductPrice').textContent = item.price;
        document.getElementById('summaryRate').textContent = item.price;
        document.getElementById('summaryTotal').textContent = item.price;
      } else {
        document.getElementById('modalTitle').textContent = 'Request Equipment Rental';
        document.getElementById('modalProductName').textContent = 'Select equipment below or enquire generally';
        document.getElementById('modalProductBrand').textContent = 'Mandad Medical Supply';
        document.getElementById('modalProductPrice').textContent = 'From $60/mo';
      }
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function closeModal() {
      document.getElementById('modalOverlay').classList.remove('open');
      document.body.style.overflow = '';
    }

    function closeModalIfOutside(e) {
      if (e.target === document.getElementById('modalOverlay')) closeModal();
    }

    // ── FAQ toggle ─────────────────────────────────────────────────
    function toggleFaq(item) {
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(f => f.classList.remove('open'));
      if (!isOpen) item.classList.add('open');
    }

    // ── Submit (demo) ──────────────────────────────────────────────
    function submitEnquiry() {
      const btn = document.querySelector('.modal-submit');
      btn.textContent = '✓ Enquiry Submitted — We\'ll call you shortly!';
      btn.style.background = '#10B981';
      btn.style.pointerEvents = 'none';
      setTimeout(() => {
        closeModal();
        btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 2L11 13"/><path d="M22 2L15 22l-4-9-9-4 20-7z"/></svg> Submit Rental Enquiry`;
        btn.style.background = '';
        btn.style.pointerEvents = '';
      }, 2500);
    }

    // ── Close modal on Escape ──────────────────────────────────────
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });