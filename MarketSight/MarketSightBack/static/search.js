const input = document.getElementById('stockSearch')

const autocomplete =  document.querySelector('.autocompleted');




// This will be autocomplete feature

input.addEventListener('input', async() => {



    const query = input.value;



    if (query.length < 1) {

        autocomplete.classList.add('hidden');

        return;

    }

    // Grab our Yahoo query from our views.py

    const response = await fetch(`/api/autocomplete/${query}/`);

    const data = await response.json();



    if (data.result && data.results.length > 0) {

        autocomplete.classList.remove('hidden')

        autocomplete.innerHTML = data.results.map(stock => `

                <div class="p-3 hover:bg-blue-700 cursor-pointer flex justify-between border-b border-blue-800"

                     onclick="window.location.href='/stock/${stock.symbol}/'">

                    <span class="font-bold text-white">${stock.symbol}</span>

                    <span class="text-blue-300 text-sm">${stock.name}</span>

                </div>

            `).join('');

    }

    else {

            resultsDiv.classList.add('hidden');

        }

});