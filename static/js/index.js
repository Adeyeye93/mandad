// ── Scroll Reveal ──────────────────────────────────────────────
    const observer = new IntersectionObserver(
      entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
      { threshold: 0.1 }
    );
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    // ── Back to top ────────────────────────────────────────────────
    const backTop = document.getElementById('backTop');
    window.addEventListener('scroll', () => {
      backTop.classList.toggle('visible', window.scrollY > 400);
    });

    // ── Cat bar active ─────────────────────────────────────────────
    document.querySelectorAll('.cat-bar-item').forEach(item => {
      item.addEventListener('click', () => {
        document.querySelectorAll('.cat-bar-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');
      });
    });

    // ── Quote cart counter (demo) ──────────────────────────────────
    document.querySelectorAll('.product-action').forEach(btn => {
      btn.addEventListener('click', function() {
        this.textContent = '✓ Added to Quote';
        this.style.background = 'var(--teal)';
        this.style.color = '#fff';
        setTimeout(() => {
          this.textContent = 'Get a Quote';
          this.style.background = '';
          this.style.color = '';
        }, 2000);
      });
    });