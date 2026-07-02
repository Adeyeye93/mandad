// ── Calculator ────────────────────────────────────────────────
    function fmt(n){ return '$' + Math.round(n).toLocaleString(); }

    function updateCalc(){
      const price = parseInt(document.getElementById('priceSlider').value);
      const down  = Math.min(parseInt(document.getElementById('downSlider').value), price);
      const [termStr, rateStr] = document.getElementById('planSelect').value.split(',');
      const term  = parseInt(termStr);
      const rate  = parseFloat(rateStr);
      const financed = price - down;
      let monthly, totalCost, interest;
      if(rate === 0){
        monthly   = financed / term;
        totalCost = financed;
        interest  = 0;
      } else {
        const monthlyRate = rate / 100 / 12;
        monthly = financed * (monthlyRate * Math.pow(1+monthlyRate, term)) / (Math.pow(1+monthlyRate, term) - 1);
        totalCost = monthly * term;
        interest  = totalCost - financed;
      }
      document.getElementById('priceDisplay').textContent  = fmt(price);
      document.getElementById('downDisplay').textContent   = fmt(down);
      document.getElementById('monthlyResult').textContent = '$' + Math.ceil(monthly);
      document.getElementById('rPrice').textContent    = fmt(price);
      document.getElementById('rDown').textContent     = fmt(down);
      document.getElementById('rFinanced').textContent = fmt(financed);
      document.getElementById('rTerm').textContent     = term + ' months';
      document.getElementById('rRate').textContent     = rate === 0 ? '0%' : rate + '% APR';
      document.getElementById('rRate').className       = rate === 0 ? 'crr-val green' : 'crr-val';
      document.getElementById('rTotal').textContent    = fmt(totalCost);
      document.getElementById('rInterest').textContent = fmt(interest);
      document.getElementById('rInterest').className   = interest === 0 ? 'crr-val green' : 'crr-val';
      // Cap down slider to price
      document.getElementById('downSlider').max = price;
    }
    updateCalc();

    // ── FAQ ───────────────────────────────────────────────────────
    function toggleFaq(item){
      const open = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(f=>f.classList.remove('open'));
      if(!open) item.classList.add('open');
    }

    // ── Scroll reveal ─────────────────────────────────────────────
    const observer = new IntersectionObserver(
      entries => entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('visible'); }),
      { threshold: 0.1 }
    );
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    // ── Back to top ───────────────────────────────────────────────
    window.addEventListener('scroll', () => {
      document.getElementById('backTop').classList.toggle('visible', window.scrollY > 300);
    });