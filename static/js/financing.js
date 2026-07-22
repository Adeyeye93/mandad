const observer = new IntersectionObserver(
      entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
      { threshold: 0.1 }
    );
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
    window.addEventListener('scroll', () => {
      document.getElementById('backTop').classList.toggle('visible', window.scrollY > 300);
    });
