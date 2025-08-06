// seller-sidebar.js
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.createElement('div');
    sidebar.className = 'w-64 bg-blue-800 text-white p-4 shadow-lg fixed h-full flex flex-col';
    
    sidebar.innerHTML = `

    <!-- Logo & Branding Section -->
        <div class="flex items-center space-x-4 mb-10 group">
            <div class="p-2 bg-white/10 rounded-xl border border-white/20 shadow-md group-hover:bg-white/20 transition-all duration-300">
                <img src="logo1.png" alt="Cozy Logo" 
                     class="h-13 w-13 object-contain transform group-hover:scale-105 transition-transform duration-200 rounded-lg">
            </div>
            <div>
                <h1 class="text-2xl font-bold tracking-tight">
                    <span class="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-white">
                        Cozy Comfort
                    </span>
                </h1>
                <p class="text-sm font-medium text-white/80 mt-1 flex items-center">
                    <span class="inline-block w-2 h-2 bg-emerald-400 rounded-full mr-2 animate-pulse"></span>
                    <span class="text-white/90">Seller Dashboard</span>
                </p>
            </div>
        </div>

        
        
        <nav class="flex-1 space-y-2">
        <a href="seller-orders.html" 
               class="flex items-center space-x-4 p-3 rounded-xl hover:bg-white/10 transition-all duration-200 group">
                <div class="w-8 h-8 bg-primary-700 rounded-lg flex items-center justify-center group-hover:bg-primary-600 transition-all">
                    <i class="fas fa-box-open text-primary-200 group-hover:text-white"></i>
                </div>
                <span class="font-medium">My Orders</span>
                <i class="fas fa-chevron-right ml-auto text-xs opacity-0 group-hover:opacity-100 transition-all"></i>
            </a>

            <a href="placeorder.html" 
               class="flex items-center space-x-4 p-3 rounded-xl hover:bg-white/10 transition-all duration-200 group">
                <div class="w-8 h-8 bg-primary-700 rounded-lg flex items-center justify-center group-hover:bg-primary-600 transition-all">
                    <i class="fas fa-cart-plus text-primary-200 group-hover:text-white"></i>
                </div>
                <span class="font-medium">Place Order</span>
                <i class="fas fa-chevron-right ml-auto text-xs opacity-0 group-hover:opacity-100 transition-all"></i>
            </a>

            <a href="checkstoke.html" 
               class="flex items-center space-x-4 p-3 rounded-xl hover:bg-white/10 transition-all duration-200 group">
                <div class="w-8 h-8 bg-primary-700 rounded-lg flex items-center justify-center group-hover:bg-primary-600 transition-all">
                    <i class="fas fa-search text-primary-200 group-hover:text-white"></i>
                </div>
                <span class="font-medium">Check Stock</span>
                <i class="fas fa-chevron-right ml-auto text-xs opacity-0 group-hover:opacity-100 transition-all"></i>
            </a>
           
            <a href="seller-notifications.html" 
               class="flex items-center space-x-4 p-3 rounded-xl hover:bg-white/10 transition-all duration-200 group">
                <div class="w-8 h-8 bg-primary-700 rounded-lg flex items-center justify-center group-hover:bg-primary-600 transition-all">
                    <i class="fas fa-bell text-primary-200 group-hover:text-white"></i>
                </div>
                <span class="font-medium">Notifications</span>
                <i class="fas fa-chevron-right ml-auto text-xs opacity-0 group-hover:opacity-100 transition-all"></i>
            </a>
            
            
        </nav>
        
        <!-- Logout Button -->
        <div class="absolute bottom-6 left-6 right-6">
            <button id="logoutBtn" 
                    class="w-full flex items-center justify-center space-x-2 bg-white/90 text-blue-800 py-3 px-4 rounded-xl font-medium hover:bg-white hover:shadow-md transition-all duration-300">
                <i class="fas fa-sign-out-alt"></i>
                <span>Logout</span>
            </button>
        </div>
    `;

    document.body.insertBefore(sidebar, document.body.firstChild);
    
    // Add margin to main content
    const header = document.querySelector('header');
const main = document.querySelector('main');
if (header) {
    header.classList.add('ml-64');
}
if (main) {
    main.classList.add('ml-64');
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