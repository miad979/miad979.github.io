const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.site-nav');
if (menuButton && navigation) { menuButton.addEventListener('click', () => { const open = menuButton.getAttribute('aria-expanded') === 'true'; menuButton.setAttribute('aria-expanded', String(!open)); navigation.classList.toggle('is-open', !open); }); }
document.querySelectorAll('[data-year]').forEach((node) => { node.textContent = new Date().getFullYear(); });
if ('IntersectionObserver' in window) { const observer = new IntersectionObserver((entries) => { entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); } }); }, { threshold: 0.12 }); document.querySelectorAll('.reveal').forEach((element) => observer.observe(element)); } else { document.querySelectorAll('.reveal').forEach((element) => element.classList.add('is-visible')); }
