const API_BASE_URL = 'https://void-v1.onrender.com/api';
let currentWalletData = null;

console.log('🚀 App.js loading...');

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    console.log('✅ Theme initialized:', savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
    console.log('🎨 Theme toggled to:', newTheme);
    if (currentWalletData && typeof window.visualizeNetwork === 'function') {
        window.visualizeNetwork();
    }
}

function updateThemeIcon(theme) {
    const icon = document.querySelector('.theme-icon');
    if (icon) icon.textContent = theme === 'dark' ? '☀️' : '🌙';
}

function isValidWalletFormat(address) {
    const ethPattern = /^0x[a-fA-F0-9]{40}$/;
    const btcPattern = /^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^bc1[a-z0-9]{39,59}$/;
    return ethPattern.test(address) || btcPattern.test(address);
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 DOM loaded');
    initTheme();
    
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
        console.log('✅ Theme toggle attached');
    }
    
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', function() {
            console.log('🔘 ANALYZE BUTTON CLICKED!');
            analyzeWallet();
        });
        console.log('✅ Analyze button listener attached');
    } else {
        console.error('❌ Analyze button NOT FOUND!');
    }
    
    const walletInput = document.getElementById('walletInput');
    if (walletInput) {
        walletInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                console.log('⌨️ Enter key pressed');
                analyzeWallet();
            }
        });
    }
    
    console.log('✅ All event listeners attached');
});

async function analyzeWallet() {
    console.log('🔍 analyzeWallet() called');
    const walletAddress = document.getElementById('walletInput').value.trim();
    console.log('📝 Wallet address:', walletAddress);
    
    if (!walletAddress) {
        console.log('⚠️ Empty address');
        showErrorModal('Empty Address', 'Please enter a wallet address to analyze.');
        return;
    }
    
    if (!isValidWalletFormat(walletAddress)) {
        console.log('❌ Invalid format');
        showErrorModal(
            'Invalid Wallet Address Format',
            `The address you entered is not in a valid format.<br><br>
            Please enter a valid cryptocurrency wallet address:
            <div class="example-box">
                <strong>Ethereum Example:</strong>
                <code>0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1</code>
                <strong style="margin-top:1rem;">Bitcoin Example:</strong>
                <code>1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa</code>
            </div>`
        );
        return;
    }
    
    console.log('✅ Valid format, showing loading...');
    showLoading();
    
    try {
        console.log('📡 Fetching wallet data...');
        const walletData = await fetchWalletData(walletAddress);
        console.log('✅ Got wallet data:', walletData);
        
        console.log('🤖 Classifying wallet...');
        const classification = await classifyWallet(walletData);
        console.log('✅ Got classification:', classification);
        
        console.log('🕸️ Fetching network graph...');
        const networkData = await fetchNetworkGraph(walletAddress);
        console.log('✅ Got network data:', networkData);
        
        currentWalletData = {
            ...walletData,
            classification,
            network: networkData
        };
        
        console.log('📊 Displaying results...');
        displayResults();
    } catch (error) {
        console.error('💥 Error:', error);
        hideLoading();
        showErrorModal('Analysis Error', error.message);
    }
}

async function fetchWalletData(address) {
    const response = await fetch(`${API_BASE_URL}/wallet/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wallet_address: address })
    });
    if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || 'Failed to fetch');
    }
    const data = await response.json();
    return data.wallet_data;
}

async function classifyWallet(walletData) {
    const response = await fetch(`${API_BASE_URL}/wallet/classify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wallet_data: walletData })
    });
    if (!response.ok) throw new Error('Classification failed');
    const data = await response.json();
    return data.classification;
}

async function fetchNetworkGraph(address) {
    const response = await fetch(`${API_BASE_URL}/analysis/network`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wallet_address: address, depth: 2 })
    });
    if (!response.ok) throw new Error('Network fetch failed');
    const data = await response.json();
    return data.network;
}

function showLoading() {
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('loadingSection').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loadingSection').classList.add('hidden');
}

function displayResults() {
    hideLoading();
    displayWalletInfo();
    displayClassification();
    displayRiskAssessment();
    document.getElementById('resultsSection').classList.remove('hidden');
    
    setTimeout(() => {
        console.log('🎨 Creating network graph...');
        if (typeof window.visualizeNetwork === 'function') {
            window.visualizeNetwork();
        } else {
            console.error('❌ visualizeNetwork not found!');
        }
    }, 300);
}

function displayWalletInfo() {
    const info = currentWalletData;
    document.getElementById('walletInfo').innerHTML = `
        <div class="info-item">
            <span class="info-label">Address:</span>
            <span class="info-value">${info.address.substring(0, 20)}...</span>
        </div>
        <div class="info-item">
            <span class="info-label">Blockchain:</span>
            <span class="info-value">${info.blockchain || 'Ethereum'}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Transactions:</span>
            <span class="info-value">${info.transaction_count}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Unique Addresses:</span>
            <span class="info-value">${info.unique_addresses}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Total Volume:</span>
            <span class="info-value">$${info.total_volume.toLocaleString()}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Last Active:</span>
            <span class="info-value">${info.last_active}</span>
        </div>
    `;
}

function displayClassification() {
    const c = currentWalletData.classification;
    const classType = c.classification.toLowerCase();
    document.getElementById('classificationResult').innerHTML = `
        <div class="classification-badge classification-${classType}">${c.classification}</div>
        <div class="info-item">
            <span class="info-label">Confidence:</span>
            <span class="info-value">${(c.confidence * 100).toFixed(1)}%</span>
        </div>
        <div class="probability-bar">
            <div class="probability-label">
                <span>Personal</span><span>${(c.probabilities.personal * 100).toFixed(1)}%</span>
            </div>
            <div class="bar"><div class="bar-fill" style="width: ${c.probabilities.personal * 100}%"></div></div>
        </div>
        <div class="probability-bar">
            <div class="probability-label">
                <span>Exchange</span><span>${(c.probabilities.exchange * 100).toFixed(1)}%</span>
            </div>
            <div class="bar"><div class="bar-fill" style="width: ${c.probabilities.exchange * 100}%"></div></div>
        </div>
        <div class="probability-bar">
            <div class="probability-label">
                <span>Suspicious</span><span>${(c.probabilities.suspicious * 100).toFixed(1)}%</span>
            </div>
            <div class="bar"><div class="bar-fill" style="width: ${c.probabilities.suspicious * 100}%"></div></div>
        </div>
    `;
}

function displayRiskAssessment() {
    const riskScore = currentWalletData.classification.probabilities.suspicious;
    const mixerProb = currentWalletData.mixer_probability;
    const suspiciousFlags = currentWalletData.suspicious_flags;
    const overallRisk = (riskScore * 0.5 + mixerProb * 0.3 + (suspiciousFlags / 50) * 0.2);
    
    document.getElementById('riskAssessment').innerHTML = `
        <div class="risk-score">
            <strong>Overall Risk Score:</strong>
            <div class="risk-meter">
                <div class="risk-indicator" style="left: calc(${overallRisk * 100}% - 20px)"></div>
            </div>
            <strong>${(overallRisk * 100).toFixed(1)}%</strong>
        </div>
        <div class="info-item">
            <span class="info-label">Mixer Probability:</span>
            <span class="info-value">${(mixerProb * 100).toFixed(1)}%</span>
        </div>
        <div class="info-item">
            <span class="info-label">Suspicious Flags:</span>
            <span class="info-value">${suspiciousFlags}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Network Connections:</span>
            <span class="info-value">${currentWalletData.network.total_nodes} nodes, ${currentWalletData.network.total_edges} edges</span>
        </div>
    `;
}

function showErrorModal(title, message) {
    const modal = document.getElementById('errorModal');
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalMessage').innerHTML = message;
    modal.classList.remove('hidden');
    
    document.getElementById('modalCloseBtn').onclick = () => modal.classList.add('hidden');
    modal.onclick = (e) => { if (e.target === modal) modal.classList.add('hidden'); };
}

console.log('✅ app.js loaded completely');
