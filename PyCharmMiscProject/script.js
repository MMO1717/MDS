document.addEventListener('DOMContentLoaded', function() {
    const executeBtn = document.getElementById('executeBtn');
    const resultDiv = document.getElementById('result');
    const darkModeToggle = document.getElementById('darkModeToggle');
    
    // Check for saved dark mode preference
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode === 'enabled') {
        document.body.classList.add('dark-mode');
        darkModeToggle.textContent = '☀️';
    }
    
    executeBtn.addEventListener('click', executeQuery);
    darkModeToggle.addEventListener('click', toggleDarkMode);
    
    async function executeQuery() {
        const host = document.getElementById('host').value;
        const port = document.getElementById('port').value;
        const user = document.getElementById('user').value;
        const password = document.getElementById('password').value;
        const database = document.getElementById('database').value;
        const sqlQuery = document.getElementById('sqlQuery').value;
        
        const connectionInfo = { host, port: parseInt(port), user, password, database };
        
        try {
            const response = await fetch('http://localhost:5000/execute_sql', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    sql_query: sqlQuery,
                    connection_info: connectionInfo
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                resultDiv.className = 'success';
                if (data.data) {
                    // For SELECT queries, display the results as a table
                    resultDiv.innerHTML = '<h3>Query Results:</h3>' + formatResultsAsTable(data.data);
                } else {
                    // For other queries, display the message
                    resultDiv.innerHTML = '<h3>Success:</h3><p>' + data.message + '</p>';
                }
            } else {
                resultDiv.className = 'error';
                resultDiv.innerHTML = '<h3>Error:</h3><p>' + data.message + '</p>';
            }
        } catch (error) {
            resultDiv.className = 'error';
            resultDiv.innerHTML = '<h3>Error:</h3><p>Failed to connect to the server: ' + error.message + '</p>';
        }
    }
    
    function formatResultsAsTable(data) {
        if (!data || data.length === 0) return '<p>No results found.</p>';
        
        let html = '<table border="1" style="width:100%; border-collapse: collapse;">';
        
        // Header row
        const headers = Object.keys(data[0]);
        html += '<tr>';
        headers.forEach(header => {
            html += `<th style="padding: 8px; background-color: #3498db; color: white;">${header}</th>`;
        });
        html += '</tr>';
        
        // Data rows
        data.forEach(row => {
            html += '<tr>';
            headers.forEach(header => {
                html += `<td style="padding: 8px; border: 1px solid #ddd;">${row[header] || ''}</td>`;
            });
            html += '</tr>';
        });
        
        html += '</table>';
        return html;
    }
    
    function toggleDarkMode() {
        const isDarkMode = document.body.classList.toggle('dark-mode');
        const darkModeToggle = document.getElementById('darkModeToggle');
        
        if (isDarkMode) {
            darkModeToggle.textContent = '☀️';
            localStorage.setItem('darkMode', 'enabled');
        } else {
            darkModeToggle.textContent = '🌙';
            localStorage.setItem('darkMode', 'disabled');
        }
    }
});