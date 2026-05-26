// SQL Query Executor with Dark Mode Support
class SQLQueryExecutor {
    constructor() {
        this.initializeElements();
        this.loadDarkModePreference();
        this.attachEventListeners();
    }

    initializeElements() {
        this.elements = {
            executeBtn: document.getElementById('executeBtn'),
            resultDiv: document.getElementById('result'),
            darkModeToggle: document.getElementById('darkModeToggle'),
            host: document.getElementById('host'),
            port: document.getElementById('port'),
            user: document.getElementById('user'),
            password: document.getElementById('password'),
            database: document.getElementById('database'),
            sqlQuery: document.getElementById('sqlQuery')
        };
    }

    loadDarkModePreference() {
        const savedDarkMode = localStorage.getItem('darkMode');
        if (savedDarkMode === 'enabled') {
            document.body.classList.add('dark-mode');
            this.elements.darkModeToggle.textContent = '☀️';
        }
    }

    attachEventListeners() {
        this.elements.executeBtn.addEventListener('click', () => this.executeQuery());
        this.elements.darkModeToggle.addEventListener('click', () => this.toggleDarkMode());
    }

    async executeQuery() {
        const connectionInfo = {
            host: this.elements.host.value,
            port: parseInt(this.elements.port.value),
            user: this.elements.user.value,
            password: this.elements.password.value,
            database: this.elements.database.value
        };

        const sqlQuery = this.elements.sqlQuery.value;

        // Validate inputs
        if (!this.validateInputs(connectionInfo, sqlQuery)) {
            return;
        }

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
            this.displayResult(data);
        } catch (error) {
            this.displayError(`Failed to connect to the server: ${error.message}`);
        }
    }

    validateInputs(connectionInfo, sqlQuery) {
        if (!sqlQuery.trim()) {
            this.displayError('Please enter a SQL query');
            return false;
        }

        if (!connectionInfo.host || !connectionInfo.user || !connectionInfo.database) {
            this.displayError('Please fill in all required connection fields');
            return false;
        }

        return true;
    }

    displayResult(data) {
        if (data.status === 'success') {
            this.elements.resultDiv.className = 'success';
            if (data.data) {
                // For SELECT queries, display the results as a table
                this.elements.resultDiv.innerHTML = '<h3>Query Results:</h3>' + this.formatResultsAsTable(data.data);
            } else {
                // For other queries, display the message
                this.elements.resultDiv.innerHTML = '<h3>Success:</h3><p>' + data.message + '</p>';
            }
        } else {
            this.displayError(data.message);
        }
    }

    displayError(message) {
        this.elements.resultDiv.className = 'error';
        this.elements.resultDiv.innerHTML = `<h3>Error:</h3><p>${message}</p>`;
    }

    formatResultsAsTable(data) {
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

    toggleDarkMode() {
        const isDarkMode = document.body.classList.toggle('dark-mode');

        if (isDarkMode) {
            this.elements.darkModeToggle.textContent = '☀️';
            localStorage.setItem('darkMode', 'enabled');
        } else {
            this.elements.darkModeToggle.textContent = '🌙';
            localStorage.setItem('darkMode', 'disabled');
        }
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SQLQueryExecutor();
});