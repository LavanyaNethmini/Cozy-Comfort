document.addEventListener('DOMContentLoaded', function() {
    // Create sidebar
    const sidebar = document.createElement('div');
    sidebar.className = 'w-64 bg-primary-800 text-white p-4 shadow-lg flex flex-col h-full';
    
    sidebar.innerHTML = `
        <div class="flex items-center space-x-2 p-4 mb-8">
            <div class="w-10 h-10 bg-white rounded-full flex items-center justify-center text-primary-800 font-bold">D</div>
            <h2 class="text-xl font-bold">Distributor Dashboard</h2>
        </div>
        
        <nav class="space-y-2">
            <a href="#" class="block w-full flex items-center space-x-3 p-3 rounded-lg bg-primary-700">
                <i class="fas fa-file-invoice text-xl"></i>
                <span>Seller Requests</span>
                <span class="ml-auto bg-yellow-500 text-white text-xs px-2 py-1 rounded-full">3 new</span>
            </a>
            <a href="dis-noti.html" class="block w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-primary-700">
                <i class="fas fa-boxes text-xl"></i>
                <span>Notifications</span>
            </a>
            <a href="#" class="block w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-primary-700">
                <i class="fas fa-truck text-xl"></i>
                <span>Logistics</span>
            </a>
            <a href="#" class="block w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-primary-700">
                <i class="fas fa-chart-line text-xl"></i>
                <span>Reports</span>
            </a>
        </nav>
        
        <div class="mt-auto p-4 border-t border-primary-700">
            <button class="w-full bg-white text-primary-800 py-2 px-4 rounded-lg font-medium hover:bg-gray-100 transition-colors flex items-center justify-center space-x-2">
                <i class="fas fa-sign-out-alt"></i>
                <span>Logout</span>
            </button>
        </div>
    `;

    // Insert sidebar properly
    const flexContainer = document.querySelector('.flex.h-screen');
    if (flexContainer) {
        flexContainer.insertBefore(sidebar, flexContainer.firstChild);
    }

    // Adjust main content
    const main = document.querySelector('main');
    if (main) {
        main.classList.remove('mx-auto', 'max-w-7xl'); // Remove these conflicting classes
        main.classList.add('ml-64'); // Add proper left margin
    }
    
    // Highlight current page link
    const currentPage = window.location.pathname.split('/').pop();
    document.querySelectorAll('nav a').forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('bg-primary-600');
            link.classList.remove('hover:bg-primary-700');
        }
    });
});