document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.createElement('div');
    sidebar.className = 'w-72 bg-gradient-to-b from-indigo-900 to-indigo-800 text-white p-6 shadow-2xl fixed h-full z-20 transition-all duration-300';
    sidebar.innerHTML = `
        <!-- Logo & Branding Section -->
        <div class="flex items-center space-x-4 mb-10 group">
            <div class="p-2 bg-white/10 rounded-xl border border-white/20 shadow-md group-hover:bg-white/20 transition-all duration-300">
                <img src="logo1.png" alt="Cozy Logo" 
                     class="h-16 w-16 object-contain transform group-hover:scale-110 transition-transform duration-300 rounded-lg">
            </div>
            <div>
                <h1 class="text-2xl font-bold tracking-tight">
                    <span class="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-white">
                        Cozy Comfort
                    </span>
                </h1>
                <p class="text-sm font-medium text-white/80 mt-1 flex items-center">
                    <span class="inline-block w-2 h-2 bg-emerald-400 rounded-full mr-2 animate-pulse"></span>
                    <span class="text-white/90">Admin Dashboard</span>
                </p>
            </div>
        </div>

        <!-- Navigation Menu -->
        <nav class="space-y-3 mt-10">
            <a href="systemreports.html" 
               class="flex items-center space-x-4 p-3 rounded-xl hover:bg-white/10 transition-all duration-200 group">
                <div class="w-8 h-8 bg-indigo-700 rounded-lg flex items-center justify-center group-hover:bg-indigo-600 transition-all">
                    <i class="fas fa-chart-bar text-indigo-200 group-hover:text-white"></i>
                </div>
                <span class="font-medium">System Reports</span>
                <i class="fas fa-chevron-right ml-auto text-xs opacity-0 group-hover:opacity-100 transition-all"></i>
            </a>

            <a href="AdminDashboard.html" 
               class="flex items-center space-x-4 p-3 rounded-xl hover:bg-white/10 transition-all duration-200 group">
                <div class="w-8 h-8 bg-indigo-700 rounded-lg flex items-center justify-center group-hover:bg-indigo-600 transition-all">
                    <i class="fas fa-users text-indigo-200 group-hover:text-white"></i>
                </div>
                <span class="font-medium">Manage Users</span>
                <i class="fas fa-chevron-right ml-auto text-xs opacity-0 group-hover:opacity-100 transition-all"></i>
            </a>
        </nav>

        <!-- Logout Button -->
        <div class="absolute bottom-6 left-6 right-6">
            <button id="logoutBtn" 
                    class="w-full flex items-center justify-center space-x-2 bg-white/90 text-indigo-800 py-3 px-4 rounded-xl font-medium hover:bg-white hover:shadow-md transition-all duration-300">
                <i class="fas fa-sign-out-alt"></i>
                <span>Logout</span>
            </button>
        </div>

       
    `;

    // Insert sidebar
    document.body.insertBefore(sidebar, document.body.firstChild);

    // Add margin to main content
    const main = document.querySelector('main');
    if (main) {
        main.classList.add('ml-72');
        main.style.transition = 'margin 0.3s ease';
    }

    // Logout functionality
    document.getElementById('logoutBtn')?.addEventListener('click', function() {
        window.location.href = 'index.html';
    });

    // Add hover effects to all nav items
    const navItems = sidebar.querySelectorAll('nav a');
    navItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.style.transform = 'translateX(5px)';
        });
        item.addEventListener('mouseleave', () => {
            item.style.transform = 'translateX(0)';
        });
    });
});