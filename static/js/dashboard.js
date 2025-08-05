// Trading Dashboard JavaScript

// Global variables
let refreshInterval;
let performanceChart;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
    
    // Auto-refresh data every 30 seconds
    refreshInterval = setInterval(refreshData, 30000);
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Update current time display
function updateCurrentTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    const dateString = now.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
    
    const timeElement = document.getElementById('current-time');
    if (timeElement) {
        timeElement.textContent = `${dateString} ${timeString}`;
    }
}

// Refresh all dashboard data
async function refreshData() {
    try {
        showLoadingState();
        
        // Call refresh API
        const response = await fetch('/api/refresh-data');
        const result = await response.json();
        
        if (result.status === 'success') {
            // Reload the page to update all data
            setTimeout(() => {
                window.location.reload();
            }, 1000);
            
            showNotification('Data refreshed successfully', 'success');
        } else {
            showNotification('Failed to refresh data: ' + result.message, 'error');
        }
    } catch (error) {
        console.error('Error refreshing data:', error);
        showNotification('Error refreshing data', 'error');
    } finally {
        hideLoadingState();
    }
}

// Show loading state
function showLoadingState() {
    const refreshBtn = document.querySelector('button[onclick="refreshData()"]');
    if (refreshBtn) {
        refreshBtn.disabled = true;
        refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Refreshing...';
    }
    
    // Add loading class to main cards
    document.querySelectorAll('.card').forEach(card => {
        card.classList.add('loading');
    });
}

// Hide loading state
function hideLoadingState() {
    const refreshBtn = document.querySelector('button[onclick="refreshData()"]');
    if (refreshBtn) {
        refreshBtn.disabled = false;
        refreshBtn.innerHTML = '<i class="fas fa-sync-alt me-1"></i>Refresh';
    }
    
    // Remove loading class from cards
    document.querySelectorAll('.card').forEach(card => {
        card.classList.remove('loading');
    });
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Format numbers for display
function formatNumber(num, decimals = 2) {
    if (num === null || num === undefined) return '0.00';
    return parseFloat(num).toFixed(decimals);
}

// Format currency
function formatCurrency(amount, decimals = 2) {
    if (amount === null || amount === undefined) return '$0.00';
    return '$' + parseFloat(amount).toFixed(decimals);
}

// Format percentage
function formatPercentage(value, decimals = 1) {
    if (value === null || value === undefined) return '0.0%';
    return parseFloat(value).toFixed(decimals) + '%';
}

// Update container status with real-time data
async function updateContainerStatus() {
    try {
        const response = await fetch('/api/container-status');
        const containers = await response.json();
        
        // Update container status cards if they exist
        containers.forEach(container => {
            const statusElement = document.querySelector(`[data-container="${container.name}"]`);
            if (statusElement) {
                updateContainerCard(statusElement, container);
            }
        });
    } catch (error) {
        console.error('Error updating container status:', error);
    }
}

// Update individual container card
function updateContainerCard(element, containerData) {
    const statusBadge = element.querySelector('.badge');
    if (statusBadge) {
        // Update status badge
        statusBadge.className = 'badge';
        if (containerData.status === 'running') {
            statusBadge.classList.add('bg-success');
            statusBadge.innerHTML = '<i class="fas fa-play me-1"></i>Running';
        } else if (containerData.status === 'exited') {
            statusBadge.classList.add('bg-danger');
            statusBadge.innerHTML = '<i class="fas fa-stop me-1"></i>Stopped';
        } else {
            statusBadge.classList.add('bg-warning');
            statusBadge.innerHTML = `<i class="fas fa-question me-1"></i>${containerData.status}`;
        }
    }
    
    // Update uptime
    const uptimeElement = element.querySelector('.uptime');
    if (uptimeElement) {
        uptimeElement.textContent = containerData.uptime || 'N/A';
    }
}

// Update trading statistics
async function updateTradingStats() {
    try {
        const response = await fetch('/api/trading-stats');
        const stats = await response.json();
        
        // Update Yuva stats
        updateUserStatsCard('yuva', stats.yuva);
        
        // Update Shan stats  
        updateUserStatsCard('shan', stats.shan);
        
        // Update overall stats
        updateOverallStats(stats);
        
    } catch (error) {
        console.error('Error updating trading stats:', error);
    }
}

// Update user statistics card
function updateUserStatsCard(user, stats) {
    const userCard = document.querySelector(`[data-user="${user}"]`);
    if (!userCard) return;
    
    // Update individual stat values
    const statElements = {
        'successful-trades': stats.successful_trades || 0,
        'failed-trades': stats.failed_trades || 0,
        'long-trades': stats.long_trades || 0,
        'short-trades': stats.short_trades || 0,
        'total-pnl': formatCurrency(stats.total_pnl || 0),
        'win-rate': formatPercentage(stats.win_rate || 0)
    };
    
    Object.entries(statElements).forEach(([key, value]) => {
        const element = userCard.querySelector(`[data-stat="${key}"]`);
        if (element) {
            element.textContent = value;
        }
    });
}

// Update overall dashboard statistics
function updateOverallStats(stats) {
    const yuvaStats = stats.yuva || {};
    const shanStats = stats.shan || {};
    
    const totalStats = {
        totalTrades: (yuvaStats.total_trades || 0) + (shanStats.total_trades || 0),
        successfulTrades: (yuvaStats.successful_trades || 0) + (shanStats.successful_trades || 0),
        failedTrades: (yuvaStats.failed_trades || 0) + (shanStats.failed_trades || 0),
        totalPnl: (yuvaStats.total_pnl || 0) + (shanStats.total_pnl || 0)
    };
    
    // Update header stat cards
    const headerStats = document.querySelectorAll('.card h3');
    if (headerStats.length >= 4) {
        headerStats[0].textContent = totalStats.totalTrades;
        headerStats[1].textContent = totalStats.successfulTrades;
        headerStats[2].textContent = totalStats.failedTrades;
        headerStats[3].textContent = formatCurrency(totalStats.totalPnl);
    }
}

// Chart utilities
function createPerformanceChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    
    return new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Trading Performance Comparison',
                    color: '#ffffff'
                },
                legend: {
                    labels: {
                        color: '#ffffff'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#ffffff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#ffffff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });
}

// Utility functions for data processing
function calculateWinRate(successful, total) {
    if (total === 0) return 0;
    return (successful / total) * 100;
}

function calculateProfitFactor(profits, losses) {
    if (losses === 0) return profits > 0 ? Infinity : 0;
    return profits / losses;
}

// Real-time updates using Server-Sent Events (if implemented)
function initializeSSE() {
    if (typeof(EventSource) !== "undefined") {
        const source = new EventSource("/api/stream");
        
        source.onmessage = function(event) {
            const data = JSON.parse(event.data);
            handleRealtimeUpdate(data);
        };
        
        source.onerror = function(event) {
            console.error("SSE connection error:", event);
        };
    }
}

// Handle real-time updates
function handleRealtimeUpdate(data) {
    switch(data.type) {
        case 'container_status':
            updateContainerStatus();
            break;
        case 'trading_stats':
            updateTradingStats();
            break;
        case 'new_trade':
            showNotification(`New trade: ${data.symbol} ${data.side}`, 'info');
            break;
        default:
            console.log('Unknown update type:', data.type);
    }
}

// Export functions for use in other scripts
window.dashboardUtils = {
    refreshData,
    updateContainerStatus,
    updateTradingStats,
    formatNumber,
    formatCurrency,
    formatPercentage,
    showNotification
};
