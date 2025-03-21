// Toggles the checked class in the checkbox
function toggleCheckbox(checkbox) {
  checkbox.classList.toggle('checked');
  var input = checkbox.querySelector('input[type="checkbox"]');
  input.checked = !input.checked;
}

// Get current date and time
function getCurrentTime() {
  var now = new Date();
  return now.toLocaleString();
}

// Download table contents
function exportTableToCsv(tableName = 'table') {
  const table = document.querySelector('.table');
  const headerRow = table.querySelector('tr');
  const headers = Array.from(headerRow.querySelectorAll('th'));
  const actionIndex = headers.findIndex((header) => header.textContent.toLowerCase() === 'actions');

  const rows = table.querySelectorAll('tbody tr');
  const csvContent = [headers.filter((_, index) => index !== actionIndex).map((header) => header.textContent).join(',')];

  rows.forEach((row) => {
    const columns = Array.from(row.querySelectorAll('td'));
    const rowContent = columns.filter((_, index) => index !== actionIndex).map((column) => `"${column.textContent.trim()}"`);
    csvContent.push(rowContent.join(','));
  });

  const encodedUri = encodeURI(`data:text/csv;charset=utf-8,${csvContent.join('\n')}`);
  const link = document.createElement('a');
  link.setAttribute('href', encodedUri);
  link.setAttribute('download', `${tableName}.csv`);
  link.click();
}

// Catch HTMX form errors
document.body.addEventListener('htmx:beforeOnLoad', function(evt) {
  if (evt.detail.xhr.status === 422) {
    evt.detail.shouldSwap = true;
    evt.detail.isError = false;
  }
});


/// Check if the client is authenticated
fetch('/auth/authenticated')
  .then(response => response.json())
  .then(data => {
    if (!data.authenticated && window.location.pathname !== '/auth/') {
      window.location.href = '/auth/';
      setTimeout(() => window.location.reload(), 0); // Update the CSRF token
    }
  });