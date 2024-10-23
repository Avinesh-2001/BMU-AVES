// DOM Elements
const elements = {
  entryForm: document.getElementById('entry-form'),
  exitForm: document.getElementById('exit-form'),
  searchForm: document.getElementById('search-form'),
  entryTable: document.getElementById('entry_table'),
  totalIn: document.getElementById('total_in'),
  totalOut: document.getElementById('total_out')
};

// Utility Functions
const formatTime = () => {
  const now = new Date();
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const seconds = now.getSeconds();
  const ampm = hours >= 12 ? 'PM' : 'AM';
  const formattedHours = hours % 12 || 12;
  
  return `${formattedHours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')} ${ampm}`;
};

const showNotification = (message, type = 'success') => {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  
  // Position the notification
  notification.style.position = 'fixed';
  notification.style.top = '20px';
  notification.style.right = '20px';
  notification.style.padding = '1rem';
  notification.style.borderRadius = '8px';
  notification.style.backgroundColor = type === 'success' ? '#4CAF50' : '#f44336';
  notification.style.color = 'white';
  notification.style.zIndex = '1000';
  
  document.body.appendChild(notification);
  
  // Animate notification
  notification.style.animation = 'slideIn 0.3s ease-out, fadeOut 0.3s ease-out 2.7s';
  
  setTimeout(() => notification.remove(), 3000);
};

// Table Management
class TableManager {
  constructor(tableElement) {
    this.table = tableElement;
    this.tbody = this.table.querySelector('tbody');
    this.entries = new Map(); // Store entries by vehicle number
  }

  addEntry(data) {
    const row = document.createElement('tr');
    
    // Add entry data to cells
    Object.values(data).forEach(text => {
      const td = document.createElement('td');
      td.textContent = text;
      row.appendChild(td);
    });
    
    // Animate row entry
    row.style.opacity = '0';
    row.style.transform = 'translateY(20px)';
    
    this.tbody.insertBefore(row, this.tbody.firstChild);
    
    requestAnimationFrame(() => {
      row.style.transition = 'all 0.3s ease-out';
      row.style.opacity = '1';
      row.style.transform = 'translateY(0)';
    });

    // Store entry
    this.entries.set(data.vehicleNo, row);
    
    // Update total entries count
    elements.totalIn.textContent = this.entries.size;
    return row;
  }

  updateExit(vehicleNo, exitTime) {
    const row = this.entries.get(vehicleNo);
    if (row) {
      row.lastElementChild.textContent = exitTime;
      row.style.backgroundColor = '#f0f0f0';
      
      // Animate update
      row.style.animation = 'highlight 1s ease-out';
      
      // Update total exits count
      elements.totalOut.textContent = parseInt(elements.totalOut.textContent || 0) + 1;
    }
  }

  searchEntries(criteria) {
    const rows = this.tbody.getElementsByTagName('tr');
    for (const row of rows) {
      let matches = true;
      
      // Check each criterion
      Object.entries(criteria).forEach(([key, value]) => {
        if (value && !row.children[key].textContent.toLowerCase().includes(value.toLowerCase())) {
          matches = false;
        }
      });
      
      // Show/hide row based on match
      row.style.display = matches ? '' : 'none';
      
      // Animate matching rows
      if (matches) {
        row.style.animation = 'highlight 0.5s ease-out';
      }
    }
  }
}

// Initialize Table Manager
const tableManager = new TableManager(elements.entryTable);

// Form Handlers
const handleEntrySubmit = (event) => {
  event.preventDefault();
  
  const formData = {
    driverName: document.getElementById('in_driver_name').value,
    vehicleNo: document.getElementById('in_vehicle_number').value,
    category: document.getElementById('in_category').value,
    mobileNumber: document.getElementById('in_mobile_number').value,
    entryTime: formatTime(),
    exitTime: ''
  };
  
  // Validate form
  if (!formData.driverName || !formData.vehicleNo || !formData.mobileNumber) {
    showNotification('Please fill in all required fields', 'error');
    return;
  }
  
  tableManager.addEntry(formData);
  showNotification('Entry recorded successfully');
  event.target.reset();
};

const handleExitSubmit = (event) => {
  event.preventDefault();
  
  const vehicleNo = document.getElementById('out_vehicle_number').value;
  
  if (!vehicleNo) {
    showNotification('Please enter vehicle number', 'error');
    return;
  }
  
  tableManager.updateExit(vehicleNo, formatTime());
  showNotification('Exit recorded successfully');
  event.target.reset();
};

const handleSearch = (event) => {
  event.preventDefault();
  
  const searchCriteria = {
    0: document.getElementById('search_driver').value, // driver name
    1: document.getElementById('search_vehicle').value, // vehicle number
    2: document.getElementById('search_category').value, // category
    3: document.getElementById('search_mobile').value // mobile number
  };
  
  tableManager.searchEntries(searchCriteria);
};

// Auto Fill Functionality
const autoFill = (type) => {
  // Simulate auto-fill with last entry data
  const lastEntry = Array.from(tableManager.entries.values()).slice(-1)[0];
  if (lastEntry) {
    const cells = lastEntry.cells;
    document.getElementById(`${type}_driver_name`).value = cells[0].textContent;
    document.getElementById(`${type}_vehicle_number`).value = cells[1].textContent;
    document.getElementById(`${type}_category`).value = cells[2].textContent;
    document.getElementById(`${type}_mobile_number`).value = cells[3].textContent;
  }
};

// Download Functionality (Mock)
const downloadCSV = (period) => {
  showNotification(`Downloading ${period} report...`);
  setTimeout(() => {
    showNotification(`${period} report downloaded successfully`);
  }, 1000);
};

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
  // Form submission listeners
  elements.entryForm.addEventListener('submit', handleEntrySubmit);
  elements.exitForm.addEventListener('submit', handleExitSubmit);
  elements.searchForm.addEventListener('submit', handleSearch);
  
  // Auto-fill buttons
  document.querySelector('.btn-auto[onclick="auto_in_fill()"]')
    .addEventListener('click', () => autoFill('in'));
  document.querySelector('.btn-auto[onclick="auto_out_fill()"]')
    .addEventListener('click', () => autoFill('out'));
  
  // Download buttons
  document.querySelector('[onclick="download_daily_csv()"]')
    .addEventListener('click', () => downloadCSV('daily'));
  document.querySelector('[onclick="download_weekly_csv()"]')
    .addEventListener('click', () => downloadCSV('weekly'));
  document.querySelector('[onclick="download_monthly_csv()"]')
    .addEventListener('click', () => downloadCSV('monthly'));
});

// Add some sample data
setTimeout(() => {
  tableManager.addEntry({
    driverName: 'John Doe',
    vehicleNo: 'KA01AB1234',
    category: 'Faculty',
    mobileNumber: '9876543210',
    entryTime: formatTime(),
    exitTime: ''
  });
}, 1000);