// LinkedIn Sales Pro - JavaScript Application Logic

class LinkedInSalesPro {
    constructor() {
        this.currentSection = 'landing';
        this.currentStep = 1;
        this.campaignData = {};
        this.selectedProspects = new Set();
        this.apiKey = '';
        this.isApiConnected = false;
        
        // Sample data from the JSON
        this.sampleProspects = [
            {
                id: 1,
                name: "Anjali Mehta",
                title: "HR Director",
                company: "TechFlow Solutions",
                location: "Mumbai, India",
                gemini_score: 94,
                recent_activity: "Posted about AI transformation in HR processes",
                talking_points: ["AI in HR", "Digital transformation", "Team scaling", "Remote work policies"],
                profile_insights: "Leading HR digital transformation at 200+ employee tech company. Recently implemented AI-powered hiring tools with 40% efficiency improvement.",
                personalization_opportunities: ["Recent AI adoption", "Mumbai tech ecosystem", "HR automation expertise", "Team growth achievements"],
                linkedin_url: "https://linkedin.com/in/anjali-mehta-hr",
                status: "discovered"
            },
            {
                id: 2,
                name: "Rahul Kumar",
                title: "CTO",
                company: "StartupForge",
                location: "Bangalore, India",
                gemini_score: 91,
                recent_activity: "Shared insights on cloud-native architecture patterns",
                talking_points: ["Cloud migration", "Microservices", "DevOps", "Tech leadership"],
                profile_insights: "Technical visionary building scalable cloud infrastructure. Led successful migration of monolith to microservices, reducing costs by 60%.",
                personalization_opportunities: ["Cloud architecture expertise", "Bangalore startup scene", "Cost optimization focus", "Technical leadership"],
                linkedin_url: "https://linkedin.com/in/rahul-kumar-cto",
                status: "discovered"
            },
            {
                id: 3,
                name: "Priya Sharma",
                title: "VP Marketing",
                company: "GrowthLabs",
                location: "Delhi, India",
                gemini_score: 89,
                recent_activity: "Celebrated 200% growth achievement in Q3 2025",
                talking_points: ["Growth marketing", "Performance metrics", "B2B strategies", "Team leadership"],
                profile_insights: "Growth marketing expert with proven track record. Led team that achieved 200% growth in 8 months using data-driven strategies.",
                personalization_opportunities: ["Recent growth milestone", "B2B marketing expertise", "Delhi market knowledge", "Data-driven approach"],
                linkedin_url: "https://linkedin.com/in/priya-sharma-vp",
                status: "discovered"
            },
            {
                id: 4,
                name: "Arjun Patel",
                title: "Sales Director",
                company: "CloudVenture",
                location: "Pune, India",
                gemini_score: 87,
                recent_activity: "Announced successful expansion to Southeast Asia markets",
                talking_points: ["International expansion", "Sales strategy", "Market development", "Team scaling"],
                profile_insights: "Sales leader driving global expansion. Successfully launched in 3 new markets with 150% revenue increase in international segments.",
                personalization_opportunities: ["Expansion achievement", "International sales", "Pune business hub", "Strategic planning"],
                linkedin_url: "https://linkedin.com/in/arjun-patel-sales",
                status: "discovered"
            },
            {
                id: 5,
                name: "Meera Gupta",
                title: "Head of Marketing",
                company: "InnovateTech",
                location: "Chennai, India",
                gemini_score: 88,
                recent_activity: "Published comprehensive whitepaper on B2B marketing automation trends",
                talking_points: ["Marketing automation", "B2B trends", "Content strategy", "Industry insights"],
                profile_insights: "Marketing thought leader and content creator. Her automation strategies helped reduce customer acquisition costs by 45% while increasing lead quality.",
                personalization_opportunities: ["Thought leadership", "Automation expertise", "Chennai market", "Cost optimization"],
                linkedin_url: "https://linkedin.com/in/meera-gupta-marketing",
                status: "discovered"
            }
        ];

        this.messageTemplates = {
            connection_request: [
                {
                    content: "Hi {{name}}, noticed your recent work on {{recent_topic}} at {{company}}. I work with {{target_role}} helping them {{value_proposition}}. Would love to connect and share insights!",
                    personalization_score: 96,
                    estimated_response_rate: 0.41
                },
                {
                    content: "Hello {{name}}, your insights on {{recent_topic}} at {{company}} caught my attention. I help {{target_role}} optimize their {{focus_area}}. Let's connect!",
                    personalization_score: 93,
                    estimated_response_rate: 0.38
                },
                {
                    content: "Hi {{name}}, saw your post about {{recent_topic}} - completely agree! I've helped similar companies at {{company}} achieve {{specific_benefit}}. Worth connecting?",
                    personalization_score: 91,
                    estimated_response_rate: 0.35
                }
            ]
        };

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadProspects();
        this.initializeCharts();
        this.showToast('Welcome to LinkedIn Sales Pro!', 'Powered by Google Gemini AI', 'success');
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                const section = e.target.dataset.section;
                this.showSection(section);
            });
        });

        // Get started button
        document.getElementById('get-started-btn')?.addEventListener('click', () => {
            this.showSection('campaigns');
        });

        // Campaign wizard - Next/Previous buttons
        document.getElementById('next-step')?.addEventListener('click', () => {
            this.nextWizardStep();
        });

        document.getElementById('prev-step')?.addEventListener('click', () => {
            this.prevWizardStep();
        });

        document.getElementById('launch-campaign')?.addEventListener('click', () => {
            this.launchCampaign();
        });

        // Campaign wizard - Direct step navigation (Fixed bug)
        document.querySelectorAll('.wizard-steps .step').forEach((step, index) => {
            step.addEventListener('click', () => {
                this.goToStep(index + 1);
            });
        });

        // Settings tabs
        document.querySelectorAll('[data-tab]').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.showTab(e.target.dataset.tab);
            });
        });

        // Template tabs
        document.querySelectorAll('.tab-btn').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.showTemplateTab(e.target.dataset.tab);
            });
        });

        // API key management
        document.getElementById('test-api')?.addEventListener('click', () => {
            this.testApiConnection();
        });

        document.getElementById('save-api')?.addEventListener('click', () => {
            this.saveApiConfiguration();
        });

        // Provider selection
        document.querySelectorAll('input[name="provider"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.selectProvider(e.target.value);
            });
        });

        // View toggle
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.toggleView(e.target.dataset.view);
            });
        });

        // Message generation
        document.getElementById('generate-messages')?.addEventListener('click', () => {
            this.generatePersonalizedMessages();
        });

        // Bulk actions
        document.getElementById('bulk-generate')?.addEventListener('click', () => {
            this.bulkGenerateMessages();
        });

        document.getElementById('bulk-export')?.addEventListener('click', () => {
            this.bulkExportProspects();
        });

        // Form updates for campaign summary
        this.setupFormWatchers();
    }

    setupFormWatchers() {
        const fields = ['campaign-name', 'target-industry', 'company-size', 'location', 'brand-voice', 'campaign-goal'];
        fields.forEach(fieldId => {
            const element = document.getElementById(fieldId);
            if (element) {
                element.addEventListener('change', () => {
                    this.updateCampaignSummary();
                });
            }
        });
    }

    showSection(sectionName) {
        // Hide all sections
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });

        // Show target section
        const targetSection = document.getElementById(`${sectionName}-section`);
        if (targetSection) {
            targetSection.classList.add('active');
            targetSection.classList.add('fade-in');
        }

        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        
        const activeLink = document.querySelector(`[data-section="${sectionName}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        this.currentSection = sectionName;

        // Section-specific initialization
        if (sectionName === 'prospects') {
            this.loadProspects();
        } else if (sectionName === 'analytics') {
            setTimeout(() => this.updateCharts(), 100);
        }
    }

    // Campaign Wizard Methods
    goToStep(stepNumber) {
        if (stepNumber >= 1 && stepNumber <= 4) {
            this.currentStep = stepNumber;
            this.updateWizardStep();
        }
    }

    nextWizardStep() {
        if (this.validateCurrentStep()) {
            if (this.currentStep < 4) {
                this.currentStep++;
                this.updateWizardStep();
            }
        }
    }

    prevWizardStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateWizardStep();
        }
    }

    updateWizardStep() {
        // Update step indicators
        document.querySelectorAll('.step').forEach((step, index) => {
            step.classList.toggle('active', index + 1 === this.currentStep);
        });

        // Update step content
        document.querySelectorAll('.step-content').forEach((content, index) => {
            content.classList.toggle('active', index + 1 === this.currentStep);
        });

        // Update buttons
        const prevBtn = document.getElementById('prev-step');
        const nextBtn = document.getElementById('next-step');
        const launchBtn = document.getElementById('launch-campaign');

        if (prevBtn) prevBtn.style.display = this.currentStep > 1 ? 'block' : 'none';
        if (nextBtn) nextBtn.style.display = this.currentStep < 4 ? 'block' : 'none';
        if (launchBtn) launchBtn.style.display = this.currentStep === 4 ? 'block' : 'none';

        // Update campaign summary on step 4
        if (this.currentStep === 4) {
            this.updateCampaignSummary();
        }
    }

    validateCurrentStep() {
        const requiredFields = {
            1: ['campaign-name', 'target-industry', 'company-size', 'location'],
            2: [],  // At least one job role should be selected
            3: ['brand-voice', 'campaign-goal'],
            4: []   // Compliance checkboxes
        };

        const fields = requiredFields[this.currentStep] || [];
        let isValid = true;

        fields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field && !field.value.trim()) {
                field.classList.add('error');
                isValid = false;
                this.showToast('Validation Error', `Please fill in all required fields`, 'error');
            } else if (field) {
                field.classList.remove('error');
            }
        });

        // Special validation for step 2 (job roles)
        if (this.currentStep === 2) {
            const checkedRoles = document.querySelectorAll('input[name="job-roles"]:checked');
            if (checkedRoles.length === 0) {
                this.showToast('Validation Error', 'Please select at least one job role', 'error');
                isValid = false;
            }
        }

        // Special validation for step 4 (compliance)
        if (this.currentStep === 4) {
            const checkedCompliance = document.querySelectorAll('.compliance-checklist input[type="checkbox"]:checked');
            if (checkedCompliance.length < 3) {
                this.showToast('Validation Error', 'Please acknowledge all compliance requirements', 'error');
                isValid = false;
            }
        }

        return isValid;
    }

    updateCampaignSummary() {
        const summaryFields = {
            'summary-name': 'campaign-name',
            'summary-industry': 'target-industry',
            'summary-size': 'company-size',
            'summary-location': 'location',
            'summary-voice': 'brand-voice',
            'summary-goal': 'campaign-goal'
        };

        Object.entries(summaryFields).forEach(([summaryId, fieldId]) => {
            const summaryElement = document.getElementById(summaryId);
            const fieldElement = document.getElementById(fieldId);
            
            if (summaryElement && fieldElement) {
                const value = fieldElement.options ? 
                    fieldElement.options[fieldElement.selectedIndex]?.text : 
                    fieldElement.value;
                summaryElement.textContent = value || '-';
            }
        });
    }

    launchCampaign() {
        this.showLoadingOverlay('Launching campaign with Gemini AI...');
        
        // Collect campaign data
        this.campaignData = {
            name: document.getElementById('campaign-name')?.value,
            industry: document.getElementById('target-industry')?.value,
            companySize: document.getElementById('company-size')?.value,
            location: document.getElementById('location')?.value,
            jobRoles: Array.from(document.querySelectorAll('input[name="job-roles"]:checked')).map(cb => cb.value),
            brandVoice: document.getElementById('brand-voice')?.value,
            goal: document.getElementById('campaign-goal')?.value,
            personalizationLevel: document.getElementById('personalization-level')?.value,
            analysisDepth: document.getElementById('analysis-depth')?.value,
            createdAt: new Date().toISOString()
        };

        setTimeout(() => {
            this.hideLoadingOverlay();
            this.showToast('Campaign Launched!', 'Your campaign is now active and analyzing prospects with Gemini AI', 'success');
            this.showSection('prospects');
        }, 2000);
    }

    // Prospects Methods
    loadProspects() {
        const container = document.getElementById('prospects-container');
        if (!container) return;

        container.innerHTML = '';
        
        this.sampleProspects.forEach(prospect => {
            const prospectCard = this.createProspectCard(prospect);
            container.appendChild(prospectCard);
        });

        this.updateBulkActionsCounter();
    }

    createProspectCard(prospect) {
        const card = document.createElement('div');
        card.className = 'prospect-card';
        card.dataset.prospectId = prospect.id;

        const scoreClass = this.getScoreClass(prospect.gemini_score);

        card.innerHTML = `
            <div class="prospect-header">
                <div class="prospect-info">
                    <h3>${prospect.name}</h3>
                    <div class="prospect-title">${prospect.title}</div>
                    <div class="prospect-company">${prospect.company} • ${prospect.location}</div>
                </div>
                <div class="gemini-score">
                    <div class="score-label">Gemini Score</div>
                    <div class="score-value ${scoreClass}">${prospect.gemini_score}</div>
                </div>
            </div>
            
            <div class="prospect-insights">
                <div class="insight-text">${prospect.profile_insights}</div>
            </div>
            
            <div class="talking-points">
                <div class="points-title">Talking Points:</div>
                <div class="points-list">
                    ${prospect.talking_points.map(point => 
                        `<span class="point-tag">${point}</span>`
                    ).join('')}
                </div>
            </div>
            
            <div class="recent-activity">
                <strong>Recent Activity:</strong> ${prospect.recent_activity}
            </div>
            
            <div class="prospect-actions">
                <button class="btn btn--primary btn--sm" onclick="app.generateMessage(${prospect.id})">Generate Message</button>
                <button class="btn btn--outline btn--sm" onclick="app.viewProfile(${prospect.id})">View Profile</button>
                <label class="checkbox-label">
                    <input type="checkbox" onchange="app.toggleProspectSelection(${prospect.id}, this.checked)">
                    <span>Select</span>
                </label>
            </div>
        `;

        return card;
    }

    getScoreClass(score) {
        if (score >= 90) return 'score-excellent';
        if (score >= 80) return 'score-good';
        return 'score-fair';
    }

    toggleProspectSelection(prospectId, selected) {
        if (selected) {
            this.selectedProspects.add(prospectId);
            document.querySelector(`[data-prospect-id="${prospectId}"]`).classList.add('selected');
        } else {
            this.selectedProspects.delete(prospectId);
            document.querySelector(`[data-prospect-id="${prospectId}"]`).classList.remove('selected');
        }
        this.updateBulkActionsCounter();
    }

    updateBulkActionsCounter() {
        const counter = document.getElementById('selected-count');
        if (counter) {
            counter.textContent = this.selectedProspects.size;
        }
    }

    generateMessage(prospectId) {
        const prospect = this.sampleProspects.find(p => p.id === prospectId);
        if (!prospect) return;

        this.showLoadingOverlay('Generating personalized message with Gemini AI...');

        setTimeout(() => {
            const message = this.createPersonalizedMessage(prospect);
            this.hideLoadingOverlay();
            this.showMessageModal(prospect, message);
        }, 1500);
    }

    createPersonalizedMessage(prospect) {
        const templates = this.messageTemplates.connection_request;
        const template = templates[Math.floor(Math.random() * templates.length)];
        
        let message = template.content
            .replace('{{name}}', prospect.name)
            .replace('{{recent_topic}}', prospect.recent_activity.split(' ').slice(2, 6).join(' '))
            .replace('{{company}}', prospect.company)
            .replace('{{target_role}}', prospect.title.split(' ')[0] + 's')
            .replace('{{value_proposition}}', 'scale their operations with AI automation')
            .replace('{{focus_area}}', prospect.talking_points[0].toLowerCase())
            .replace('{{specific_benefit}}', '40% cost reduction');

        return {
            content: message,
            personalization_score: template.personalization_score,
            estimated_response_rate: template.estimated_response_rate,
            character_count: message.length
        };
    }

    showMessageModal(prospect, message) {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Generated Message for ${prospect.name}</h3>
                    <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">×</button>
                </div>
                <div class="modal-body">
                    <div class="message-stats">
                        <span>Personalization Score: <strong>${message.personalization_score}%</strong></span>
                        <span>Est. Response Rate: <strong>${Math.round(message.estimated_response_rate * 100)}%</strong></span>
                        <span>Characters: <strong>${message.character_count}/300</strong></span>
                    </div>
                    <textarea class="form-control" rows="4">${message.content}</textarea>
                    <div class="gemini-indicator">
                        <span class="gemini-badge">✦ Generated by Gemini AI</span>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn--primary">Copy Message</button>
                    <button class="btn btn--outline" onclick="app.generateMessage(${prospect.id})">Regenerate</button>
                    <button class="btn btn--outline" onclick="this.closest('.modal-overlay').remove()">Close</button>
                </div>
            </div>
        `;

        // Add modal styles
        modal.style.cssText = `
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: rgba(0,0,0,0.5); display: flex; align-items: center; 
            justify-content: center; z-index: 1000;
        `;

        const modalContent = modal.querySelector('.modal-content');
        modalContent.style.cssText = `
            background: var(--color-surface); border-radius: var(--radius-lg); 
            max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto;
            border: 1px solid var(--color-border);
        `;

        document.body.appendChild(modal);
    }

    viewProfile(prospectId) {
        const prospect = this.sampleProspects.find(p => p.id === prospectId);
        if (prospect?.linkedin_url) {
            window.open(prospect.linkedin_url, '_blank');
        }
    }

    // Template Methods
    showTemplateTab(tabName) {
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        document.getElementById(`${tabName}-tab`).classList.add('active');
    }

    generatePersonalizedMessages() {
        const prospectSelect = document.getElementById('template-prospect');
        const prospectId = parseInt(prospectSelect.value);
        
        if (!prospectId) {
            this.showToast('Selection Required', 'Please select a prospect first', 'warning');
            return;
        }

        const prospect = this.sampleProspects.find(p => p.id === prospectId);
        this.showLoadingOverlay('Generating message variations with Gemini AI...');

        setTimeout(() => {
            this.hideLoadingOverlay();
            this.displayMessageVariations(prospect);
        }, 1500);
    }

    displayMessageVariations(prospect) {
        const container = document.getElementById('message-variations');
        if (!container) return;

        const variations = this.messageTemplates.connection_request.map((template, index) => {
            const message = this.createPersonalizedMessage(prospect);
            return {
                ...message,
                title: `Variation ${index + 1}`,
                template: template
            };
        });

        container.innerHTML = variations.map((variation, index) => `
            <div class="message-variation">
                <div class="message-header">
                    <div class="variation-title">${variation.title}</div>
                    <div class="message-stats">
                        <span>Score: ${variation.personalization_score}%</span>
                        <span>Response Rate: ${Math.round(variation.estimated_response_rate * 100)}%</span>
                    </div>
                </div>
                <div class="message-content">${variation.content}</div>
                <div class="message-actions">
                    <button class="btn btn--primary btn--sm" onclick="app.copyToClipboard('${variation.content.replace(/'/g, "\\'")}')">Copy</button>
                    <button class="btn btn--outline btn--sm">Edit</button>
                    <button class="btn btn--outline btn--sm">Use Template</button>
                </div>
            </div>
        `).join('');
    }

    // Analytics Methods
    initializeCharts() {
        this.initResponseChart();
        this.initPerformanceChart();
    }

    initResponseChart() {
        const ctx = document.getElementById('responseChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                datasets: [{
                    label: 'Response Rate %',
                    data: [28, 35, 42, 38, 45, 41, 47],
                    borderColor: '#1FB8CD',
                    backgroundColor: 'rgba(31, 184, 205, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 60,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }

    initPerformanceChart() {
        const ctx = document.getElementById('performanceChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Accepted', 'Pending', 'Declined'],
                datasets: [{
                    data: [42, 35, 23],
                    backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    updateCharts() {
        // This would normally update with real data
        // For demo purposes, we'll just reinitialize
        this.initializeCharts();
    }

    // Settings Methods
    showTab(tabName) {
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        document.getElementById(`${tabName}-tab`).classList.add('active');
    }

    selectProvider(provider) {
        document.querySelectorAll('.provider-option').forEach(option => {
            option.classList.remove('selected');
        });

        const selectedOption = document.querySelector(`input[value="${provider}"]`).closest('.provider-option');
        selectedOption.classList.add('selected');

        if (provider === 'gemini') {
            this.showToast('Excellent Choice!', 'Gemini offers 72x cost savings and superior context understanding', 'success');
        } else {
            this.showToast('Consider Gemini', 'Switch to Gemini for 72x cost savings and better performance', 'warning');
        }
    }

    testApiConnection() {
        const apiKey = document.getElementById('gemini-api-key').value;
        if (!apiKey.trim()) {
            this.showToast('API Key Required', 'Please enter your Gemini API key', 'error');
            return;
        }

        this.showLoadingOverlay('Testing API connection...');

        // Simulate API test
        setTimeout(() => {
            this.hideLoadingOverlay();
            this.isApiConnected = true;
            this.apiKey = apiKey;
            
            const statusElement = document.getElementById('api-status');
            if (statusElement) {
                statusElement.textContent = 'Connected';
                statusElement.classList.add('connected');
            }

            // Show usage section
            const usageSection = document.getElementById('api-usage-section');
            if (usageSection) {
                usageSection.style.display = 'block';
            }

            this.showToast('API Connected!', 'Gemini API connection successful', 'success');
        }, 1500);
    }

    saveApiConfiguration() {
        const apiKey = document.getElementById('gemini-api-key').value;
        if (!apiKey.trim()) {
            this.showToast('API Key Required', 'Please enter your Gemini API key first', 'error');
            return;
        }

        // Save to localStorage for demo purposes
        localStorage.setItem('gemini_api_key', apiKey);
        this.showToast('Configuration Saved', 'Your API settings have been saved securely', 'success');
    }

    // View Methods
    toggleView(viewType) {
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-view="${viewType}"]`).classList.add('active');

        const container = document.getElementById('prospects-container');
        if (container) {
            container.className = viewType === 'list' ? 'prospects-list' : 'prospects-grid';
        }
    }

    // Bulk Actions
    bulkGenerateMessages() {
        if (this.selectedProspects.size === 0) {
            this.showToast('No Selection', 'Please select prospects first', 'warning');
            return;
        }

        this.showLoadingOverlay(`Generating messages for ${this.selectedProspects.size} prospects...`);
        
        setTimeout(() => {
            this.hideLoadingOverlay();
            this.showToast('Messages Generated', `Created personalized messages for ${this.selectedProspects.size} prospects`, 'success');
        }, 2000);
    }

    bulkExportProspects() {
        if (this.selectedProspects.size === 0) {
            this.showToast('No Selection', 'Please select prospects first', 'warning');
            return;
        }

        const selectedData = this.sampleProspects.filter(p => this.selectedProspects.has(p.id));
        const csvContent = this.convertToCSV(selectedData);
        this.downloadCSV(csvContent, 'selected_prospects.csv');
        
        this.showToast('Export Complete', `Exported ${selectedData.length} prospects`, 'success');
    }

    convertToCSV(data) {
        const headers = ['Name', 'Title', 'Company', 'Location', 'Gemini Score', 'Recent Activity'];
        const csvRows = [headers.join(',')];
        
        data.forEach(prospect => {
            const row = [
                prospect.name,
                prospect.title,
                prospect.company,
                prospect.location,
                prospect.gemini_score,
                `"${prospect.recent_activity}"`
            ];
            csvRows.push(row.join(','));
        });
        
        return csvRows.join('\n');
    }

    downloadCSV(content, filename) {
        const blob = new Blob([content], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    }

    // Utility Methods
    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.showToast('Copied!', 'Message copied to clipboard', 'success');
        });
    }

    showLoadingOverlay(message = 'Processing...') {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.querySelector('p').textContent = message;
            overlay.classList.remove('hidden');
        }
    }

    hideLoadingOverlay() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.add('hidden');
        }
    }

    showToast(title, message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        `;

        container.appendChild(toast);

        // Auto-remove after 4 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease-in-out forwards';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 4000);
    }
}

// Initialize the application
const app = new LinkedInSalesPro();

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .error {
        border-color: var(--color-error) !important;
        box-shadow: 0 0 0 2px rgba(var(--color-error-rgb), 0.2) !important;
    }
`;
document.head.appendChild(style);