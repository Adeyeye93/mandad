// Mobile nav toggle — works with the .nav-toggle / .nav-links.mobile-open
// classes added to the CSS. Include this once, on every page.
//
// Required HTML (drop this button into your <nav>, right after .nav-logo
// or before .nav-cta — wherever fits your markup):
//
//   <button class="nav-toggle" aria-label="Menu">
//     <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
//       <path d="M4 6h16M4 12h16M4 18h16"/>
//     </svg>
//   </button>

document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('mobile-open');
    });
    // Close menu when a link is tapped
    links.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => links.classList.remove('mobile-open'));
    });
    // Close menu if clicking outside it
    document.addEventListener('click', (e) => {
      if (!links.contains(e.target) && !toggle.contains(e.target)) {
        links.classList.remove('mobile-open');
      }
    });
  }

  // Products page filter drawer — works with .filter-toggle / .sidebar.mobile-open
  // Required HTML: <button class="filter-toggle">Filters</button> somewhere in
  // .page-header-row, and a .sidebar-overlay div right before </body>.
  const filterToggle = document.querySelector('.filter-toggle');
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.sidebar-overlay');
  if (filterToggle && sidebar) {
    filterToggle.addEventListener('click', () => {
      sidebar.classList.add('mobile-open');
      if (overlay) overlay.classList.add('open');
    });
    if (overlay) {
      overlay.addEventListener('click', () => {
        sidebar.classList.remove('mobile-open');
        overlay.classList.remove('open');
      });
    }
  }
});
