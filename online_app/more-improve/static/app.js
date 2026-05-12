```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Lucide icons
    lucide.createIcons();
    
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('input[required], textarea[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error');
                    
                    // Create error message if not exists
                    if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('error-message')) {
                        const errorMsg = document.createElement('p');
                        errorMsg.className = 'error-message text-accent-pink text-sm mt-1';
                        errorMsg.textContent = 'This field is required';
                        input.parentNode.insertBefore(errorMsg, input.nextSibling);
                    }
                } else {
                    input.classList.remove('error');
                    if (input.nextElementSibling && input.nextElementSibling.classList.contains('error-message')) {
                        input.nextElementSibling.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showToast('Please fill all required fields', 'error');
            }
        });
    });
    
    // API Fetch Example
    async function fetchTasks() {
        try {
            const response = await fetch('/api/tasks');
            if (!response.ok) throw new Error('Network response was not ok');
            const tasks = await response.json();
            return tasks;
        } catch (error) {
            console.error('Error fetching tasks:', error);
            showToast('Failed to load tasks', 'error');
            return [];
        }
    }
    
    // Toast notification function
    window.showToast = function(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) return;
        
        const toast = document.createElement('div');
        toast.className = `toast toast-${type} animate-fade-in-up`;
        toast.innerHTML = `
            <div class="flex items-center">
                <i data-lucide="${type === 'success' ? 'check-circle' : type === 'error' ? 'alert-circle' : 'info'}" class="w-5 h-5 mr-2"></i>
                <span>${message}</span>
            </div>
        `;
        toastContainer.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            toast.classList.add('animate-fade-out');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }
    
    // Initialize any page-specific functionality
    if (document.querySelector('.dashboard-page')) {
        initDashboard();
    }
    
    function initDashboard() {
        // Load tasks and render them
        fetchTasks().then(tasks => {
            if (tasks.length > 0) {
                renderTaskList(tasks);
            }
        });
        
        // Add event listeners for dashboard interactions
        // ...
    }
    
    function renderTaskList(tasks) {
        const container = document.getElementById('tasks-container');
        if (!container) return;
        
        container.innerHTML = tasks.map(task => `
            <div class="task-item glass-dark p-4 rounded-lg mb-3">
                <div class="flex justify-between items-start">
                    <div>
                        <h4 class="font-medium">${task.title}</h4>
                        <p class="text-sm