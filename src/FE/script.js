const searchInput = document.getElementById('search-input');
const clearSearch = document.getElementById('clear-search');
const legislationList = document.getElementById('legislation-list');

// Simulated endpoint for fetching legislation data
async function fetchLegislation(region) {
    try {
        const response = await fetch(`https://green-legislation-nameless-cherry-1408.fly.dev/legislation/${region}`);
        if (!response.ok) {
            throw new Error(`Error fetching legislation: ${response.statusText}`);
        }
        const legislationData = await response.json();
        console.log('Fetched legislation data:', legislationData); // Add this line for debugging
        return legislationData;
    } catch (error) {
        console.error('Error in fetchLegislation:', error);
        return [];
    }
}

function displayLegislation(laws) {
    legislationList.innerHTML = '';
    console.log(laws)
    laws.forEach(law => {
        const li = document.createElement('li');
        li.textContent = law[1] + ' | ' + law[4] + ' | ' + law[5] + ' | ' + law[6] + ' | ' + law[8];

        li.onclick = () => {
            const jsonData = {
                "summary": law[3],
                "description": law[2],
                "index_pn": law[7],
            }
            const encodedData = encodeURIComponent(JSON.stringify(jsonData));
            window.location.href = `https://green-legislation-nameless-cherry-1408.fly.dev/static/tool.html?data=${encodedData}`;
        };
        legislationList.appendChild(li);
    });
}

searchInput.addEventListener('keypress', async (e) => {
    if (e.key === 'Enter') {
        const region = searchInput.value.trim();
        if (region) {
            const laws = await fetchLegislation(region);
            displayLegislation(laws);
        } else {
            legislationList.innerHTML = '';
        }
    }
   
});

clearSearch.addEventListener('click', () => {
    searchInput.value = '';
    legislationList.innerHTML = '';
});