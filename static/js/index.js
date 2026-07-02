// ── Slider ─────────────────────────────────────────────────────
    let currentSlide = 0;
    const slides = document.querySelectorAll('.hero-slide');
    const totalSlides = slides.length;
    let autoSlide;

    function showSlide(n) {
      slides.forEach(s => s.classList.remove('active'));
      slides[n].classList.add('active');
      currentSlide = n;
    }
    function nextSlide() {
      showSlide((currentSlide + 1) % totalSlides);
      resetAuto();
    }
    function prevSlide() {
      showSlide((currentSlide - 1 + totalSlides) % totalSlides);
      resetAuto();
    }
    function goSlide(n) {
      showSlide(n);
      resetAuto();
    }
    function resetAuto() {
      clearInterval(autoSlide);
      autoSlide = setInterval(nextSlide, 5000);
    }
    autoSlide = setInterval(nextSlide, 5000);

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