const input = document.getElementById('stockSearch');
const autocomplete = document.querySelector('.autocomplete');

// autocomplete feature
input.addEventListener('input', async () => {

    const query = input.value;

    if (query.length < 1) {
        autocomplete.classList.add('hidden');
        autocomplete.innerHTML = '';
        return;
    }

    const response = await fetch(`/api/autocomplete/${query}/`);
    const data = await response.json();
    console.log(data);

    if (data.results && data.results.length > 0) {

        autocomplete.classList.remove('hidden');

        autocomplete.innerHTML = data.results.map(stock => `
            <div class="p-3 hover:bg-blue-700 cursor-pointer flex justify-between border-b border-blue-800"
                onclick="window.location.href='/stock/${stock.symbol}/'">
                <span class="font-bold text-white">${stock.symbol}</span>
                <span class="text-blue-300 text-sm">${stock.name}</span>
            </div>
        `).join('');

    } else {
        autocomplete.classList.add('hidden');
        autocomplete.innerHTML = '';
    }
});
