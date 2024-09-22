const searchInput = document.getElementById('search-input');
const clearSearch = document.getElementById('clear-search');
const legislationList = document.getElementById('legislation-list');

// Simulated endpoint for fetching legislation data
function fetchLegislation(region) {
    // This is a mock function. In a real application, you would make an API call here.
    return new Promise((resolve) => {
        setTimeout(() => {
            const legislationData = {
                'California': [
                    'California Environmental Quality Act (CEQA)',
                    'Global Warming Solutions Act of 2006 (AB 32)',
                    'Sustainable Groundwater Management Act'
                ],
                'New York': [
                    'Climate Leadership and Community Protection Act',
                    'Environmental Conservation Law',
                    'Brownfield Cleanup Program'
                ],
                'Texas': [
                    'Texas Emissions Reduction Plan (TERP)',
                    'Texas Clean Air Act',
                    'Texas Solid Waste Disposal Act'
                ]
            };
            resolve(legislationData[region] || []);
        }, 500); // Simulating network delay
    });
}

function displayLegislation(laws) {
    legislationList.innerHTML = '';
    laws.forEach(law => {
        const li = document.createElement('li');
        li.textContent = law;
        legislationList.appendChild(li);
    });
}

searchInput.addEventListener('input', async () => {
    const region = searchInput.value.trim();
    if (region) {
        const laws = await fetchLegislation(region);
        displayLegislation(laws);
    } else {
        legislationList.innerHTML = '';
    }
});

clearSearch.addEventListener('click', () => {
    searchInput.value = '';
    legislationList.innerHTML = '';
});