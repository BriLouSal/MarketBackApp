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

            <div 
                class="px-4 py-2 flex justify-between items-center cursor-pointer 
                       hover:bg-blue-800/40 transition"
                onclick="window.location.href='/stock/${stock.symbol}/'">

                <div>
                    <div class="text-white font-semibold text-sm">
                        ${stock.symbol ?? ''}
                    </div>

                    <div class="text-slate-400 text-xs truncate max-w-xs">
                        ${stock.name ?? ''}
                    </div>
                </div>

                <div class="text-slate-300 text-xs">
                    ${stock.exchange ?? ''}
                </div>

            </div>

        `).join('');

    } else {
        autocomplete.classList.add('hidden');
        autocomplete.innerHTML = '';
    }
});
