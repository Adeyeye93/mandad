function setTab(el){
      document.querySelectorAll('.enquiry-tab').forEach(t=>t.classList.remove('active'));
      el.classList.add('active');
    }
    function submitForm(){
      document.getElementById('formBody').style.display='none';
      document.getElementById('formSuccess').classList.add('show');
    }
    function resetForm(){
      document.getElementById('formBody').style.display='block';
      document.getElementById('formSuccess').classList.remove('show');
    }
    window.addEventListener('scroll',()=>{
      document.getElementById('backTop').classList.toggle('visible',window.scrollY>300);
    });