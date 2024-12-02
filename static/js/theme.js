// Select the toggle button
const themeToggle = document.getElementById('theme-toggle');

// Check for saved user preference
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);

// Update the button icon class based on saved theme
themeToggle.className = savedTheme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';

// Add event listener for toggling themes
themeToggle.addEventListener('click', () => {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

  // Apply the new theme and save it
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);

  // Update the button icon class
  themeToggle.className = newTheme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
});
