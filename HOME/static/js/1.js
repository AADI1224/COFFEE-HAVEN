document.addEventListener('contextmenu', function(e) {
    e.preventDefault(); // Disable right-click context menu
});

document.addEventListener('copy', function(e) {
    e.preventDefault(); // Prevent copying
    alert("Copying is disabled on this page."); // Optional: Show an alert
});

const uniqueTabId = localStorage.getItem('uniqueTabId') || Math.random().toString(36).substr(2, 9);
localStorage.setItem('uniqueTabId', uniqueTabId);

// Set a custom cookie for this tab (session isolation)
document.cookie = `tab_session_id=${uniqueTabId}; path=/;`;
